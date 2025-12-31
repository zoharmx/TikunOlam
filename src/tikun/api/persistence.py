"""
Job Persistence Manager

Handles saving and loading jobs from disk to ensure persistence across server restarts.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
from tikun.utils.logging import get_logger

logger = get_logger(__name__)

# Define absolute path relative to project root
# Assuming this file is in src/tikun/api/persistence.py
# Project root is ../../../
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
JOBS_DIR = PROJECT_ROOT / "data" / "jobs"

def init_jobs_storage():
    """Initialize jobs storage directory."""
    if not JOBS_DIR.exists():
        JOBS_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created jobs storage directory: {JOBS_DIR}")

def save_job(job_id: str, job_data: Dict[str, Any]):
    """Save job data to disk."""
    try:
        init_jobs_storage()
        file_path = JOBS_DIR / f"{job_id}.json"

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(job_data, f, indent=2, default=str)

    except Exception as e:
        logger.error(f"Failed to save job {job_id}: {e}")

def load_job(job_id: str) -> Optional[Dict[str, Any]]:
    """Load job data from disk."""
    try:
        file_path = JOBS_DIR / f"{job_id}.json"
        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    except Exception as e:
        logger.error(f"Failed to load job {job_id}: {e}")
        return None

def delete_job_file(job_id: str):
    """Delete job file."""
    try:
        file_path = JOBS_DIR / f"{job_id}.json"
        if file_path.exists():
            os.remove(file_path)

    except Exception as e:
        logger.error(f"Failed to delete job file {job_id}: {e}")

def list_all_jobs() -> Dict[str, Dict[str, Any]]:
    """List all jobs from disk."""
    jobs = {}
    try:
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
