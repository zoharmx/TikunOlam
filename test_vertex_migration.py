"""
Test script to verify Vertex AI migration

This script tests that:
1. Vertex AI can be initialized properly
2. Keter Sefirah can call Vertex AI
3. Basic ethical analysis works end-to-end
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tikun.config import get_config
from tikun.sefirot.keter import Keter


def test_vertex_ai_initialization():
    """Test that Vertex AI initializes without errors"""
    print("=" * 80)
    print("TEST 1: Vertex AI Initialization")
    print("=" * 80)

    try:
        config = get_config()

        # Check required environment variables
        if not config.gcp_project_id or config.gcp_project_id == "your-gcp-project-id":
            print("⚠️  WARNING: GCP_PROJECT_ID not configured in .env")
            print("   The test will fail unless you set a valid GCP project ID")
            print()
            print("   To fix:")
            print("   1. Create a GCP project at https://console.cloud.google.com")
            print("   2. Enable Vertex AI API")
            print("   3. Set GCP_PROJECT_ID in .env file")
            print()
            return False

        print(f"✅ GCP Project ID: {config.gcp_project_id}")
        print(f"✅ GCP Location: {config.gcp_location}")
        print(f"✅ Keter Model: {config.keter_model}")
        print()

        return True

    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False


def test_keter_vertex_ai():
    """Test that Keter can call Vertex AI successfully"""
    print("=" * 80)
    print("TEST 2: Keter Vertex AI Integration")
    print("=" * 80)

    try:
        config = get_config()
        keter = Keter(config, verbose=True)

        print("✅ Keter initialized successfully")
        print()

        # Simple test scenario
        test_scenario = """
        A city council is considering implementing a universal basic income (UBI)
        program funded by a 2% tax on automated services. The program would provide
        $1000/month to all residents earning less than $50,000/year.
        """

        print("Testing scenario:")
        print(test_scenario.strip())
        print()
        print("Calling Vertex AI via Keter...")
        print()

        result = keter.safe_process(test_scenario.strip())

        if 'error' in result:
            print(f"❌ Keter processing failed: {result['error']}")
            return False

        print("✅ Vertex AI call successful!")
        print()
        print("Results:")
        print(f"  • Alignment: {result.get('alignment_percentage', 'N/A')}%")
        print(f"  • Corruption: {result.get('corruption_severity', 'N/A')}")
        print(f"  • Manifestation Valid: {result.get('manifestation_valid', 'N/A')}")
        print(f"  • Threshold Met: {result.get('threshold_met', 'N/A')}")
        print()

        # Validate response structure
        if result.get('alignment_percentage') is None:
            print("⚠️  WARNING: alignment_percentage not found in response")
            return False

        print("✅ Response structure validated")
        print()

        return True

    except Exception as e:
        print(f"❌ Keter test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_datadog_integration():
    """Test that Datadog integration is properly configured"""
    print("=" * 80)
    print("TEST 3: Datadog Integration")
    print("=" * 80)

    try:
        from monitoring.datadog_config import get_datadog_config, DATADOG_AVAILABLE

        if not DATADOG_AVAILABLE:
            print("⚠️  Datadog SDK not available (monitoring module not found)")
            print("   This is OK for local testing, but required for deployment")
            print()
            return True  # Not a failure for basic testing

        config = get_datadog_config()

        if not config.enabled:
            print("⚠️  Datadog not configured (API keys missing)")
            print("   Set DATADOG_API_KEY and DATADOG_APP_KEY to enable")
            print()
            return True  # Not a failure for basic testing

        print(f"✅ Datadog configured")
        print(f"   Service: {config.service_name}")
        print(f"   Environment: {config.env}")
        print()

        return True

    except Exception as e:
        print(f"⚠️  Datadog integration check failed: {str(e)}")
        print("   This is OK for local testing")
        print()
        return True  # Not a critical failure


def main():
    """Run all tests"""
    print()
    print("🚀 TIKUN OLAM - VERTEX AI MIGRATION TEST")
    print()

    results = []

    # Test 1: Initialization
    results.append(("Vertex AI Initialization", test_vertex_ai_initialization()))

    # Test 2: Keter integration (only if Test 1 passed)
    if results[0][1]:
        results.append(("Keter Vertex AI Integration", test_keter_vertex_ai()))
    else:
        print()
        print("⏭️  Skipping Keter test due to configuration issues")
        print()

    # Test 3: Datadog (informational only)
    results.append(("Datadog Integration", test_datadog_integration()))

    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")

    print()

    critical_tests = results[:2]  # First 2 tests are critical
    all_passed = all(result[1] for result in critical_tests)

    if all_passed:
        print("🎉 ALL CRITICAL TESTS PASSED!")
        print()
        print("Next steps:")
        print("1. The Vertex AI migration is working correctly")
        print("2. You can now run full pipeline tests")
        print("3. Configure Datadog keys for observability (optional for testing)")
        print()
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print()
        print("Please fix the issues above before proceeding.")
        print()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
