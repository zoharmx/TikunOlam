"""
Upload Datadog dashboard configuration for Tikun Olam

This script creates the Tikun Olam Ethical AI Observatory dashboard in Datadog.
"""

import json
import os
import sys
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def upload_dashboard():
    """
    Upload Tikun Olam dashboard to Datadog

    Returns:
        str: Dashboard URL if successful, None otherwise
    """
    # Configure API client
    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = os.getenv("DATADOG_API_KEY")
    configuration.api_key["appKeyAuth"] = os.getenv("DATADOG_APP_KEY")

    # Set Datadog site (get from environment)
    datadog_site = os.getenv("DATADOG_SITE", "datadoghq.com")
    configuration.server_variables["site"] = datadog_site

    print(f"Using Datadog site: {datadog_site}")
    print(f"API Key: {configuration.api_key['apiKeyAuth'][:10]}...")

    if not configuration.api_key["apiKeyAuth"] or not configuration.api_key["appKeyAuth"]:
        print("❌ Error: DATADOG_API_KEY and DATADOG_APP_KEY environment variables must be set")
        return None

    try:
        with ApiClient(configuration) as api_client:
            api_instance = DashboardsApi(api_client)

            # Load dashboard JSON
            dashboard_path = os.path.join(os.path.dirname(__file__), 'datadog_dashboard.json')
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                dashboard_json = json.load(f)

            # Create dashboard
            body = Dashboard(**dashboard_json)

            response = api_instance.create_dashboard(body=body)

            print(f"✅ Dashboard created successfully!")
            print(f"📊 Dashboard URL: {response.url}")
            print(f"🆔 Dashboard ID: {response.id}")

            return response.url

    except Exception as e:
        print(f"❌ Failed to create dashboard: {str(e)}")
        return None


if __name__ == "__main__":
    print("🚀 Uploading Tikun Olam dashboard to Datadog...")
    print()

    dashboard_url = upload_dashboard()

    if dashboard_url:
        print()
        print("="*80)
        print("NEXT STEPS:")
        print("="*80)
        print("1. Open dashboard in your browser")
        print("2. Customize widgets as needed")
        print("3. Set up detection rules with create_monitors.py")
        print("4. Add dashboard URL to frontend .env file")
        print()
    else:
        print()
        print("Dashboard upload failed. Please check:")
        print("- DATADOG_API_KEY is set correctly")
        print("- DATADOG_APP_KEY is set correctly")
        print("- Datadog account has dashboard creation permissions")
