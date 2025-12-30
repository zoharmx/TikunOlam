"""
Create Datadog monitors from detection rules for Tikun Olam

This script sets up all alerting monitors defined in detection_rules.py
"""

import os
import sys
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_type import MonitorType
from datadog_api_client.v1.model.monitor_options import MonitorOptions
from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from detection_rules import DETECTION_RULES


def create_monitors():
    """
    Create all Datadog monitors from detection rules

    Returns:
        list: List of created monitor IDs
    """
    # Configure API client
    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = os.getenv("DATADOG_API_KEY")
    configuration.api_key["appKeyAuth"] = os.getenv("DATADOG_APP_KEY")

    # Set Datadog site (get from environment)
    datadog_site = os.getenv("DATADOG_SITE", "datadoghq.com")
    configuration.server_variables["site"] = datadog_site

    if not configuration.api_key["apiKeyAuth"] or not configuration.api_key["appKeyAuth"]:
        print("❌ Error: DATADOG_API_KEY and DATADOG_APP_KEY environment variables must be set")
        return []

    created_monitors = []

    try:
        with ApiClient(configuration) as api_client:
            api_instance = MonitorsApi(api_client)

            for rule in DETECTION_RULES:
                try:
                    print(f"Creating monitor: {rule['name']}...")

                    # Build monitor thresholds
                    thresholds = MonitorThresholds()
                    if 'critical' in rule['threshold']:
                        thresholds.critical = float(rule['threshold']['critical'])
                    if 'warning' in rule['threshold']:
                        thresholds.warning = float(rule['threshold']['warning'])

                    # Build monitor options
                    options = MonitorOptions(
                        thresholds=thresholds,
                        notify_audit=True,
                        notify_no_data=rule.get('notify_no_data', False),
                        include_tags=True,
                        require_full_window=rule.get('require_full_window', False),
                        evaluation_delay=rule.get('evaluation_delay', 300)
                    )

                    # Create monitor
                    body = Monitor(
                        name=rule["name"],
                        type=MonitorType.METRIC_ALERT,
                        query=rule["query"],
                        message=rule["message"],
                        tags=rule["tags"],
                        priority=rule.get("priority", 3),
                        options=options
                    )

                    response = api_instance.create_monitor(body=body)

                    print(f"  ✅ Created: {rule['name']} (ID: {response.id})")
                    created_monitors.append({
                        'name': rule['name'],
                        'id': response.id,
                        'priority': rule['priority']
                    })

                except Exception as e:
                    print(f"  ❌ Failed to create {rule['name']}: {str(e)}")
                    continue

    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return created_monitors

    return created_monitors


if __name__ == "__main__":
    print("🚀 Creating Datadog monitors for Tikun Olam...")
    print()

    monitors = create_monitors()

    print()
    print("="*80)
    print(f"SUMMARY: Created {len(monitors)}/{len(DETECTION_RULES)} monitors")
    print("="*80)

    if monitors:
        print()
        print("Critical Monitors:")
        for monitor in monitors:
            if monitor['priority'] == 1:
                print(f"  🚨 {monitor['name']} (ID: {monitor['id']})")

        print()
        print("Warning Monitors:")
        for monitor in monitors:
            if monitor['priority'] == 2:
                print(f"  ⚠️  {monitor['name']} (ID: {monitor['id']})")

        print()
        print("Info Monitors:")
        for monitor in monitors:
            if monitor['priority'] == 3:
                print(f"  ℹ️  {monitor['name']} (ID: {monitor['id']})")

        print()
        print("View all monitors: https://app.datadoghq.com/monitors/manage")
    else:
        print()
        print("No monitors were created. Please check:")
        print("- DATADOG_API_KEY is set correctly")
        print("- DATADOG_APP_KEY is set correctly")
        print("- Datadog account has monitor creation permissions")
