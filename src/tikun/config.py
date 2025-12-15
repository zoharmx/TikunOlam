"""
Configuration management for Tikun Olam

Handles environment variables, API keys, and system configuration
with secure defaults and validation.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class TikunConfig(BaseSettings):
    """
    Tikun Olam configuration loaded from environment variables.

    All API keys and sensitive data should be stored in .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ============================================================================
    # AI API KEYS (Required)
    # ============================================================================

    gemini_api_key: str = Field(
        ...,
        description="Google Gemini API Key for Western perspective analysis",
        min_length=1
    )

    anthropic_api_key: str = Field(
        ...,
        description="Anthropic Claude API Key for synthesis and advanced reasoning",
        min_length=1
    )

    deepseek_api_key: str = Field(
        ...,
        description="DeepSeek API Key for Eastern perspective analysis",
        min_length=1
    )

    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API Key (optional fallback)"
    )

    # ============================================================================
    # ENVIRONMENT
    # ============================================================================

    tikun_env: str = Field(
        default="development",
        description="Environment: development, staging, or production"
    )

    log_level: str = Field(
        default="INFO",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )

    output_dir: Path = Field(
        default=Path("./results"),
        description="Directory for output files"
    )

    # ============================================================================
    # MODEL CONFIGURATION
    # ============================================================================

    keter_model: str = Field(default="gemini-2.0-flash-exp")
    chochmah_model: str = Field(default="claude-3-5-sonnet-20241022")
    binah_west_model: str = Field(default="gemini-2.0-flash-exp")
    binah_east_model: str = Field(default="deepseek-chat")
    chesed_model: str = Field(default="gemini-2.0-flash-exp")
    gevurah_model: str = Field(default="gemini-2.0-flash-exp")
    tiferet_model: str = Field(default="claude-3-5-sonnet-20241022")
    netzach_model: str = Field(default="gemini-2.0-flash-exp")
    hod_model: str = Field(default="gemini-2.0-flash-exp")
    yesod_model: str = Field(default="claude-3-5-sonnet-20241022")
    malchut_model: str = Field(default="claude-3-5-sonnet-20241022")

    # ============================================================================
    # PERFORMANCE & LIMITS
    # ============================================================================

    api_timeout: int = Field(
        default=120,
        ge=10,
        le=600,
        description="API request timeout in seconds"
    )

    max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum retries for failed API calls"
    )

    rate_limit_rpm: int = Field(
        default=60,
        ge=1,
        le=1000,
        description="Rate limit in requests per minute"
    )

    enable_cache: bool = Field(
        default=True,
        description="Enable response caching"
    )

    cache_ttl: int = Field(
        default=3600,
        ge=0,
        description="Cache TTL in seconds"
    )

    # ============================================================================
    # BINAHSIGMA CONFIGURATION
    # ============================================================================

    binah_sigma_threshold: float = Field(
        default=0.15,
        ge=0.0,
        le=1.0,
        description="BinahSigma activation threshold (% geopolitical keywords)"
    )

    binah_high_divergence_threshold: int = Field(
        default=40,
        ge=0,
        le=100,
        description="Minimum bias delta for 'high divergence' (%)"
    )

    # ============================================================================
    # API SERVER
    # ============================================================================

    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000, ge=1, le=65535)
    api_docs_enabled: bool = Field(default=True)
    cors_origins: str = Field(default="http://localhost:3000,http://localhost:8080")

    # ============================================================================
    # MONITORING & TELEMETRY
    # ============================================================================

    enable_metrics: bool = Field(default=True)
    metrics_port: int = Field(default=9090, ge=1, le=65535)
    enable_tracing: bool = Field(default=False)

    # ============================================================================
    # SECURITY
    # ============================================================================

    api_auth_token: Optional[str] = Field(default=None)
    strict_validation: bool = Field(default=True)
    max_scenario_length: int = Field(
        default=50000,
        ge=1000,
        le=500000,
        description="Maximum scenario text length in characters"
    )

    # ============================================================================
    # VALIDATORS
    # ============================================================================

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the standard levels."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v

    @field_validator("tikun_env")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment is one of the supported values."""
        valid_envs = ["development", "staging", "production"]
        v = v.lower()
        if v not in valid_envs:
            raise ValueError(f"tikun_env must be one of {valid_envs}")
        return v

    @field_validator("output_dir")
    @classmethod
    def create_output_dir(cls, v: Path) -> Path:
        """Ensure output directory exists."""
        v.mkdir(parents=True, exist_ok=True)
        return v

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def get_cors_origins_list(self) -> list[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.tikun_env == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.tikun_env == "development"

    def get_model_for_sefirah(self, sefirah: str) -> str:
        """
        Get the configured model for a specific Sefirah.

        Args:
            sefirah: Name of the Sefirah (lowercase)

        Returns:
            Model identifier string
        """
        model_attr = f"{sefirah.lower()}_model"
        return getattr(self, model_attr, "gemini-2.0-flash-exp")

    def to_dict(self) -> Dict[str, Any]:
        """
        Export configuration as dictionary (excluding sensitive keys).

        Returns:
            Dictionary with non-sensitive configuration values
        """
        sensitive_keys = {
            "gemini_api_key",
            "anthropic_api_key",
            "deepseek_api_key",
            "openai_api_key",
            "api_auth_token",
        }

        return {
            k: v for k, v in self.model_dump().items()
            if k not in sensitive_keys
        }


# Global configuration instance (lazy loaded)
_config: Optional[TikunConfig] = None


def get_config(reload: bool = False) -> TikunConfig:
    """
    Get or create the global Tikun configuration.

    Args:
        reload: If True, reload configuration from environment

    Returns:
        TikunConfig instance
    """
    global _config

    if _config is None or reload:
        _config = TikunConfig()

    return _config


def set_config(config: TikunConfig) -> None:
    """
    Set the global Tikun configuration.

    Args:
        config: TikunConfig instance to use globally
    """
    global _config
    _config = config
