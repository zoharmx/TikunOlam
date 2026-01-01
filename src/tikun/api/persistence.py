"""
Job persistence module for Tikun Olam API.

Automatically uses Google Cloud Storage in Cloud Run,
falls back to local files in development.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Try to import Google Cloud Storage
try:
    from google.cloud import storage
    HAS_GCS = True
except ImportError:
    HAS_GCS = False


class JobPersistence:
    """Handles job persistence with automatic GCS/local fallback."""

    def __init__(self):
        # Detect environment
        self.is_cloud_run = os.getenv('K_SERVICE') is not None

        # FAIL FAST: Cloud Run REQUIRES Google Cloud Storage
        if self.is_cloud_run and not HAS_GCS:
            raise RuntimeError(
                "❌ FATAL: Running in Cloud Run but google-cloud-storage is not installed. "
                "Add 'google-cloud-storage>=2.10.0' to requirements.txt"
            )

        self.use_gcs = self.is_cloud_run and HAS_GCS

        if self.use_gcs:
            # Cloud Run with GCS
            self.project_id = os.getenv('GCP_PROJECT_ID', 'tikunframework')
            self.bucket_name = os.getenv('GCS_BUCKET', f"{self.project_id}-tikun-jobs")
            self.storage_client = storage.Client()

            try:
                self.bucket = self.storage_client.bucket(self.bucket_name)
                # Check if bucket exists
                if not self.bucket.exists():
                    try:
                        # Try to create bucket
                        self.bucket = self.storage_client.create_bucket(
                            self.bucket_name,
                            location='us-central1'
                        )
                        print(f"✅ Created GCS bucket: {self.bucket_name}")
                    except Exception as create_error:
                        # If error 409 (already exists), use existing bucket
                        if "409" in str(create_error) or "already own it" in str(create_error):
                            self.bucket = self.storage_client.bucket(self.bucket_name)
                            print(f"✅ Using existing GCS bucket: {self.bucket_name}")
                        else:
                            raise  # Re-raise other errors
                else:
                    print(f"✅ Using GCS bucket: {self.bucket_name}")
            except Exception as e:
                # FAIL FAST in production - never silently fall back to local storage
                if self.is_cloud_run:
                    error_msg = f"❌ FATAL: GCS bucket initialization failed in Cloud Run: {e}"
                    print(error_msg)
                    raise RuntimeError(error_msg) from e
                else:
                    # Only allow fallback in local development
                    print(f"⚠️ GCS bucket error in development: {e}. Falling back to local storage.")
                    self.use_gcs = False
                    self._setup_local_storage()
        else:
            # Local development
            self._setup_local_storage()

    def _setup_local_storage(self):
        """Setup local file storage."""
        self.local_dir = Path("data/jobs")
        self.local_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Using local storage: {self.local_dir.absolute()}")

    def _get_blob_name(self, job_id: str) -> str:
        """Get GCS blob name for job."""
        return f"jobs/{job_id}.json"

    def _get_local_path(self, job_id: str) -> Path:
        """Get local file path for job."""
        return self.local_dir / f"{job_id}.json"

    def save_job(self, job_id: str, job_data: Dict[str, Any]) -> bool:
        """
        Save job to storage.

        Args:
            job_id: Unique job identifier
            job_data: Job data to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Add timestamp
            job_data['updated_at'] = datetime.utcnow().isoformat()

            # Serialize
            job_json = json.dumps(job_data, indent=2, ensure_ascii=False)

            if self.use_gcs:
                # Save to GCS
                blob = self.bucket.blob(self._get_blob_name(job_id))
                blob.upload_from_string(
                    job_json,
                    content_type='application/json'
                )
            else:
                # Save to local file
                path = self._get_local_path(job_id)
                path.write_text(job_json, encoding='utf-8')

            return True

        except Exception as e:
            print(f"❌ Error saving job {job_id}: {e}")
            return False

    def load_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Load job from storage.

        Args:
            job_id: Unique job identifier

        Returns:
            Job data dict, or None if not found
        """
        try:
            if self.use_gcs:
                # Load from GCS
                blob = self.bucket.blob(self._get_blob_name(job_id))
                if not blob.exists():
                    return None

                job_json = blob.download_as_text()
            else:
                # Load from local file
                path = self._get_local_path(job_id)
                if not path.exists():
                    return None

                job_json = path.read_text(encoding='utf-8')

            return json.loads(job_json)

        except Exception as e:
            print(f"❌ Error loading job {job_id}: {e}")
            return None

    def delete_job(self, job_id: str) -> bool:
        """
        Delete job from storage.

        Args:
            job_id: Unique job identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.use_gcs:
                # Delete from GCS
                blob = self.bucket.blob(self._get_blob_name(job_id))
                if blob.exists():
                    blob.delete()
            else:
                # Delete from local file
                path = self._get_local_path(job_id)
                if path.exists():
                    path.unlink()

            return True

        except Exception as e:
            print(f"❌ Error deleting job {job_id}: {e}")
            return False

    def list_jobs(self, limit: int = 100) -> List[str]:
        """
        List all job IDs.

        Args:
            limit: Maximum number of jobs to return

        Returns:
            List of job IDs
        """
        try:
            if self.use_gcs:
                # List from GCS
                blobs = self.bucket.list_blobs(prefix="jobs/", max_results=limit)
                job_ids = []
                for blob in blobs:
                    # Extract job_id from "jobs/{job_id}.json"
                    filename = blob.name.split('/')[-1]
                    if filename.endswith('.json'):
                        job_id = filename[:-5]  # Remove .json
                        job_ids.append(job_id)
                return job_ids
            else:
                # List from local files
                job_files = list(self.local_dir.glob("*.json"))
                return [f.stem for f in job_files[:limit]]

        except Exception as e:
            print(f"❌ Error listing jobs: {e}")
            return []

    def job_exists(self, job_id: str) -> bool:
        """
        Check if job exists in storage.

        Args:
            job_id: Unique job identifier

        Returns:
            True if exists, False otherwise
        """
        if self.use_gcs:
            blob = self.bucket.blob(self._get_blob_name(job_id))
            return blob.exists()
        else:
            path = self._get_local_path(job_id)
            return path.exists()


# Global instance
_persistence = None


def get_persistence() -> JobPersistence:
    """Get or create global persistence instance."""
    global _persistence
    if _persistence is None:
        _persistence = JobPersistence()
    return _persistence
