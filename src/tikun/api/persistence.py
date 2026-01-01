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
    from google.api_core.exceptions import NotFound, Conflict, Forbidden
    HAS_GCS = True
except ImportError:
    HAS_GCS = False


class JobPersistence:
    """Handles job persistence with automatic GCS/local fallback."""

    def __init__(self):
        # Detect environment
        self.is_cloud_run = os.getenv('K_SERVICE') is not None
        self.use_gcs = self.is_cloud_run and HAS_GCS

        # FAIL FAST in Cloud Run: If we expect GCS but don't have the library, crash.
        if self.is_cloud_run and not HAS_GCS:
            raise RuntimeError("Running in Cloud Run but google-cloud-storage is not installed.")

        if self.use_gcs:
            # Cloud Run with GCS
            self.project_id = os.getenv('GCP_PROJECT_ID', 'tikunframework')
            self.bucket_name = os.getenv('GCS_BUCKET', f"{self.project_id}-tikun-jobs")

            try:
                self.storage_client = storage.Client()
                self.bucket = self._get_or_create_bucket()
                print(f"✅ Using GCS bucket: {self.bucket_name}")
            except Exception as e:
                # CRITICAL: Do NOT fall back to local storage in Cloud Run.
                # If GCS fails, the application is broken and should restart/fail.
                print(f"❌ FATAL GCS Error: {e}")
                raise RuntimeError(f"Failed to initialize GCS persistence: {e}")
        else:
            # Local development
            self._setup_local_storage()

    def _get_or_create_bucket(self):
        """Get existing bucket or create if missing."""
        try:
            return self.storage_client.get_bucket(self.bucket_name)
        except NotFound:
            print(f"Bucket {self.bucket_name} not found. Creating...")
            try:
                return self.storage_client.create_bucket(
                    self.bucket_name,
                    location='us-central1'
                )
            except Conflict:
                # Race condition: someone else created it just now
                print(f"Bucket {self.bucket_name} created concurrently. retrieving...")
                return self.storage_client.get_bucket(self.bucket_name)
            except Forbidden as e:
                # Permission issue trying to create
                 raise RuntimeError(f"Permission denied creating bucket {self.bucket_name}: {e}")
        except Forbidden as e:
             # Permission issue trying to get
             raise RuntimeError(f"Permission denied accessing bucket {self.bucket_name}: {e}")

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
                # Use retry=None to default or set specific retry policy if needed
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
            # In Cloud Run, we might want to raise here too, but for now returning False is handled by API
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
                # Local storage might not be initialized if we never created a job
                if not hasattr(self, 'local_dir') or not self.local_dir.exists():
                    return []

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
