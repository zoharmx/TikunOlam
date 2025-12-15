"""
Tests for validation utilities
"""

import pytest
from tikun.utils.validation import (
    validate_scenario,
    sanitize_text,
    detect_geopolitical_content,
    validate_api_key,
    truncate_for_display
)


def test_validate_scenario_success():
    """Test successful scenario validation."""
    scenario = "This is a valid scenario with sufficient length for testing purposes."

    is_valid, error = validate_scenario(scenario, min_length=10, max_length=1000)

    assert is_valid is True
    assert error is None


def test_validate_scenario_too_short():
    """Test scenario too short."""
    scenario = "Short"

    is_valid, error = validate_scenario(scenario, min_length=50)

    assert is_valid is False
    assert "too short" in error.lower()


def test_validate_scenario_too_long():
    """Test scenario too long."""
    scenario = "x" * 60000

    is_valid, error = validate_scenario(scenario, max_length=50000)

    assert is_valid is False
    assert "too long" in error.lower()


def test_validate_scenario_suspicious_content():
    """Test detection of suspicious patterns."""
    suspicious_scenarios = [
        "<script>alert('xss')</script>",
        "javascript:void(0)",
        "onerror=alert(1)",
    ]

    for scenario in suspicious_scenarios:
        is_valid, error = validate_scenario(scenario, min_length=10)
        assert is_valid is False, f"Should detect suspicious content: {scenario}"


def test_sanitize_text():
    """Test text sanitization."""
    dirty_text = "Hello  \x00  World\n\nMultiple   spaces"
    clean_text = sanitize_text(dirty_text)

    assert "\x00" not in clean_text
    assert "  " not in clean_text or clean_text.count("  ") < dirty_text.count("  ")


def test_sanitize_text_truncation():
    """Test text truncation."""
    long_text = "x" * 1000
    truncated = sanitize_text(long_text, max_length=100)

    assert len(truncated) <= 100


def test_detect_geopolitical_content():
    """Test geopolitical content detection."""
    geo_text = "The China-USA trade war affects NATO and BRICS alliances"

    is_geo, score, keywords = detect_geopolitical_content(geo_text)

    assert is_geo is True
    assert score > 0
    assert len(keywords) >= 3
    assert "china" in keywords
    assert "usa" in keywords or "america" in keywords


def test_detect_non_geopolitical():
    """Test non-geopolitical content."""
    normal_text = "The community garden project will benefit local residents"

    is_geo, score, keywords = detect_geopolitical_content(normal_text)

    assert is_geo is False
    assert score < 0.15


def test_validate_api_key():
    """Test API key validation."""
    # Valid Gemini key format
    is_valid, error = validate_api_key("AIzaSyBxxxxxxxxxxxxxxxxxxx", "gemini")
    assert is_valid is True

    # Valid Anthropic key format
    is_valid, error = validate_api_key("sk-ant-xxxxxxxxxxxxxxxxxx", "anthropic")
    assert is_valid is True

    # Empty key
    is_valid, error = validate_api_key("", "gemini")
    assert is_valid is False
    assert "cannot be empty" in error.lower()

    # Too short
    is_valid, error = validate_api_key("short", "gemini")
    assert is_valid is False
    assert "too short" in error.lower()


def test_truncate_for_display():
    """Test display truncation."""
    long_text = "x" * 200

    truncated = truncate_for_display(long_text, max_length=50)

    assert len(truncated) <= 53  # 50 + "..."
    assert truncated.endswith("...")


    short_text = "Short text"
    not_truncated = truncate_for_display(short_text, max_length=50)

    assert not_truncated == short_text
