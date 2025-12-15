"""
Pytest configuration and fixtures
"""

import pytest
import os
from pathlib import Path
from tikun.config import TikunConfig, set_config


@pytest.fixture(scope="session")
def test_config():
    """Create test configuration."""
    # Set test environment variables
    os.environ["TIKUN_ENV"] = "development"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["OUTPUT_DIR"] = str(Path(__file__).parent / "test_results")

    # Use mock API keys for testing (these won't make real API calls in unit tests)
    os.environ["GEMINI_API_KEY"] = "test_gemini_key"
    os.environ["ANTHROPIC_API_KEY"] = "test_anthropic_key"
    os.environ["DEEPSEEK_API_KEY"] = "test_deepseek_key"

    config = TikunConfig()
    set_config(config)

    return config


@pytest.fixture
def sample_scenario():
    """Sample scenario for testing."""
    return """
PROPOSAL: Implement a community garden project in an urban neighborhood

GOAL: Improve food security and community cohesion

CONTEXT:
- Urban neighborhood with limited green space
- High food insecurity rates (25% of residents)
- Diverse community (various ethnicities, income levels)
- City owns vacant lot suitable for conversion

STAKEHOLDERS:
- Local residents (500 households)
- City government
- Community organizations
- Local businesses

EXPECTED BENEFITS:
- Increased access to fresh produce
- Community building and social cohesion
- Educational opportunities (gardening, nutrition)
- Environmental benefits (green space, biodiversity)

POTENTIAL CONCERNS:
- Maintenance and sustainability
- Equitable access and participation
- Water usage and costs
- Liability and insurance
"""


@pytest.fixture
def geopolitical_scenario():
    """Geopolitical scenario that should trigger BinahSigma."""
    return """
PROPOSAL: UN-mandated peacekeeping mission in disputed territory

CONTEXT:
- Border conflict between two nations
- China and Russia oppose intervention
- USA and NATO support intervention
- Civilian population at risk
- Historical tensions dating back decades

GEOPOLITICAL DIMENSIONS:
- Sovereignty concerns vs humanitarian intervention
- Great power rivalry (USA/China/Russia)
- Regional stability implications
- International law interpretation differences

STAKEHOLDERS:
- Civilian population (2 million)
- Both nations involved
- UN Security Council permanent members
- Regional neighbors
- International humanitarian organizations
"""
