#!/usr/bin/env python3
"""
Fix GCS job files by adding missing 'summary' and 'case_name' fields.
This script processes all jobs in GCS and updates them with the summary.
"""

import json
import os
from google.cloud import storage
from tikun.orchestrator import TikunOrchestrator

def fix_job_file(bucket, blob_name):
    """Fix a single job file by adding summary if missing."""
    print(f"\nProcessing: {blob_name}")

    # Download job data
    blob = bucket.blob(blob_name)
    job_json = blob.download_as_text()
    job_data = json.loads(job_json)

    # Check if already has summary
    if job_data.get('results') and 'summary' in job_data['results']:
        print(f"  ✅ Already has summary, skipping")
        return False

    # Check if has results
    if not job_data.get('results'):
        print(f"  ⚠️  No results found, skipping")
        return False

    results = job_data['results']

    # Check if results have sefirot_results (required for summary)
    if 'sefirot_results' not in results:
        print(f"  ⚠️  No sefirot_results found, skipping")
        return False

    # Generate summary using orchestrator
    print(f"  🔧 Generating summary...")
    orchestrator = TikunOrchestrator(verbose=False)
    try:
        summary_dict = orchestrator.get_summary(results)

        # Add summary and case_name to results
        results['summary'] = summary_dict
        if 'case_name' not in results:
            results['case_name'] = results.get('metadata', {}).get('case_name', job_data.get('case_name', 'unknown'))

        # Update job data
        job_data['results'] = results

        # Upload fixed version
        blob.upload_from_string(
            json.dumps(job_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )

        print(f"  ✅ Fixed and uploaded")
        return True

    except Exception as e:
        print(f"  ❌ Error generating summary: {e}")
        return False


def main():
    """Main function to fix all jobs in GCS."""
    print("=" * 70)
    print("Tikun Olam - Fix GCS Job Summaries")
    print("=" * 70)

    # Initialize GCS client
    project_id = os.getenv('GCP_PROJECT_ID', 'tikunframework')
    bucket_name = f"{project_id}-tikun-jobs"

    print(f"\nProject: {project_id}")
    print(f"Bucket: {bucket_name}")

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        # List all job files
        blobs = list(bucket.list_blobs(prefix="jobs/"))
        print(f"\nFound {len(blobs)} job files")

        if not blobs:
            print("No jobs to process")
            return

        # Process each job
        fixed_count = 0
        skipped_count = 0
        error_count = 0

        for blob in blobs:
            try:
                if fix_job_file(bucket, blob.name):
                    fixed_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                print(f"  ❌ Error processing {blob.name}: {e}")
                error_count += 1

        # Summary
        print("\n" + "=" * 70)
        print("Summary:")
        print(f"  ✅ Fixed: {fixed_count}")
        print(f"  ⏭️  Skipped: {skipped_count}")
        print(f"  ❌ Errors: {error_count}")
        print(f"  📊 Total: {len(blobs)}")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
