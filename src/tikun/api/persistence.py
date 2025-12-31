"""
Job Persistence Manager

Handles saving and loading jobs from disk or Google Cloud Storage (GCS) to ensure persistence across server restarts.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
from tikun.utils.logging import get_logger
from tikun.config import get_config

logger = get_logger(__name__)

# Constants
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
JOBS_DIR = PROJECT_ROOT / "data" / "jobs"

# Global GCS client
_storage_client = None
_bucket = None

def get_storage_client():
    """Lazy load storage client to avoid import overhead if not used."""
    global _storage_client
    if _storage_client is None:
        try:
            from google.cloud import storage
            _storage_client = storage.Client()
        except ImportError:
            logger.warning("google-cloud-storage not installed. GCS persistence disabled.")
        except Exception as e:
            logger.error(f"Failed to initialize GCS client: {e}")
    return _storage_client

def get_bucket():
    """Get GCS bucket."""
    global _bucket
    if _bucket is None:
        client = get_storage_client()
        if client:
            config = get_config()
            # Try to get bucket name from env var or config, else construct default
            bucket_name = os.getenv("TIKUN_JOBS_BUCKET")
            if not bucket_name:
                project_id = config.gcp_project_id
                bucket_name = f"{project_id}-tikun-jobs"

            try:
                _bucket = client.bucket(bucket_name)
                # Verify bucket exists/access
                if not _bucket.exists():
                    logger.info(f"Bucket {bucket_name} does not exist. Creating...")
                    _bucket.create(location=config.gcp_location)
                logger.info(f"Using GCS bucket: {bucket_name}")
            except Exception as e:
                logger.error(f"Failed to access bucket {bucket_name}: {e}")
                _bucket = None
    return _bucket

def is_cloud_run():
    """Check if running on Cloud Run."""
    return bool(os.getenv("K_SERVICE")) or bool(os.getenv("TIKUN_FORCE_GCS"))

def init_jobs_storage():
    """Initialize jobs storage."""
    if is_cloud_run():
        get_bucket() # Initialize GCS connection
    else:
        # Local storage fallback
        if not JOBS_DIR.exists():
            JOBS_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created local jobs storage directory: {JOBS_DIR}")

def save_job(job_id: str, job_data: Dict[str, Any]):
    """Save job data to storage."""
    try:
        # Try GCS first if in cloud environment
        if is_cloud_run():
            bucket = get_bucket()
            if bucket:
                blob = bucket.blob(f"jobs/{job_id}.json")
                blob.upload_from_string(
                    json.dumps(job_data, default=str),
                    content_type="application/json"
                )
                logger.debug(f"Saved job {job_id} to GCS")
                return

        # Fallback to local
        init_jobs_storage()
        file_path = JOBS_DIR / f"{job_id}.json"

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(job_data, f, indent=2, default=str)

    except Exception as e:
        logger.error(f"Failed to save job {job_id}: {e}")

def load_job(job_id: str) -> Optional[Dict[str, Any]]:
    """Load job data from storage."""
    try:
        # Try GCS first if in cloud environment
        if is_cloud_run():
            bucket = get_bucket()
            if bucket:
                blob = bucket.blob(f"jobs/{job_id}.json")
                if blob.exists():
                    data = blob.download_as_text()
                    return json.loads(data)
                # If not in GCS, maybe check local? (Likely not if on Cloud Run)
                return None

        # Fallback to local
        file_path = JOBS_DIR / f"{job_id}.json"
        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    except Exception as e:
        logger.error(f"Failed to load job {job_id}: {e}")
        return None

def delete_job_file(job_id: str):
    """Delete job file from storage."""
    try:
        if is_cloud_run():
            bucket = get_bucket()
            if bucket:
                blob = bucket.blob(f"jobs/{job_id}.json")
                if blob.exists():
                    blob.delete()
                    return

        # Fallback to local
        file_path = JOBS_DIR / f"{job_id}.json"
        if file_path.exists():
            os.remove(file_path)

    except Exception as e:
        logger.error(f"Failed to delete job file {job_id}: {e}")

def list_all_jobs() -> Dict[str, Dict[str, Any]]:
    """List all jobs from storage."""
    jobs = {}
    try:
        if is_cloud_run():
            bucket = get_bucket()
            if bucket:
                blobs = bucket.list_blobs(prefix="jobs/")
                for blob in blobs:
                    try:
                        data = blob.download_as_text()
                        job_data = json.loads(data)
                        if "id" in job_data:
                            jobs[job_data["id"]] = job_data
                    except Exception as e:
                        logger.error(f"Failed to load job from blob {blob.name}: {e}")
                return jobs

        # Fallback to local
        if not JOBS_DIR.exists():
            return {}

        for file_path in JOBS_DIR.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    job_data = json.load(f)
                    if "id" in job_data:
                        jobs[job_data["id"]] = job_data
            except Exception as e:
                logger.error(f"Failed to load job file {file_path}: {e}")

        return jobs
    except Exception as e:
        logger.error(f"Failed to list jobs: {e}")
        return {}
