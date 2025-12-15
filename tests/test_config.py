"""
Tests for configuration management
"""

import pytest
from tikun.config import TikunConfig, get_config
from pydantic import ValidationError


def test_config_defaults(test_config):
    """Test default configuration values."""
    config = get_config()

    assert config.tikun_env == "development"
    assert config.log_level == "DEBUG"
    assert config.api_timeout == 120
    assert config.max_retries == 3


def test_config_validation():
    """Test configuration validation."""
    # Invalid log level
    with pytest.raises(ValidationError):
        TikunConfig(
            gemini_api_key="test",
            anthropic_api_key="test",
            deepseek_api_key="test",
            log_level="INVALID"
        )

    # Invalid environment
    with pytest.raises(ValidationError):
        TikunConfig(
            gemini_api_key="test",
            anthropic_api_key="test",
            deepseek_api_key="test",
            tikun_env="invalid_env"
        )


def test_config_model_selection(test_config):
    """Test model selection for Sefirot."""
    config = get_config()

    assert config.get_model_for_sefirah("keter") == "gemini-2.0-flash-exp"
    assert config.get_model_for_sefirah("chochmah") == "claude-3-5-sonnet-20241022"
    assert config.get_model_for_sefirah("binah_west") == "gemini-2.0-flash-exp"


def test_config_environment_checks(test_config):
    """Test environment check methods."""
    config = get_config()

    assert config.is_development() is True
    assert config.is_production() is False


def test_config_to_dict(test_config):
    """Test configuration export to dict."""
    config = get_config()
    config_dict = config.to_dict()

    # Should exclude sensitive keys
    assert "gemini_api_key" not in config_dict
    assert "anthropic_api_key" not in config_dict

    # Should include non-sensitive keys
    assert "tikun_env" in config_dict
    assert "log_level" in config_dict
