"""
Configuration management for Tikun Olam
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class TikunConfig(BaseSettings):
    """
    Tikun Olam configuration loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ============================================================================
    # AI API KEYS
    # ============================================================================

    gemini_api_key: str = Field(
        ...,
        description="Google Gemini API Key for Western perspective analysis",
        min_length=1
    )

    # CAMBIO AQUÍ: Ahora es Optional y tiene default=None
    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic Claude API Key (Optional - uses Gemini fallback)"
    )

    deepseek_api_key: Optional[str] = Field(
        default=None,
        description="DeepSeek API Key for Eastern perspective analysis"
    )

    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API Key (Tiferet)"
    )

    grok_api_key: Optional[str] = Field(
        default=None,
        description="xAI Grok API Key (Keter, Malchut)"
    )

    mistral_api_key: Optional[str] = Field(
        default=None,
        description="Mistral AI API Key (Chochmah, Yesod)"
    )

    # ============================================================================
    # GOOGLE CLOUD PLATFORM (for Vertex AI)
    # ============================================================================

    gcp_project_id: str = Field(
        ...,
        description="Google Cloud Project ID for Vertex AI",
        min_length=1
    )

    gcp_location: str = Field(
        default="us-central1",
        description="Google Cloud location/region for Vertex AI"
    )

    # ============================================================================
    # DATADOG OBSERVABILITY
    # ============================================================================

    datadog_api_key: Optional[str] = Field(
        default=None,
        description="Datadog API Key for metrics and monitoring"
    )

    datadog_app_key: Optional[str] = Field(
        default=None,
        description="Datadog Application Key for API access"
    )

    datadog_service_name: str = Field(
        default="tikun-olam",
        description="Service name for Datadog tracing"
    )

    datadog_statsd_host: str = Field(
        default="127.0.0.1",
        description="Datadog StatsD host"
    )

    datadog_statsd_port: int = Field(
        default=8125,
        description="Datadog StatsD port"
    )

    datadog_trace_port: int = Field(
        default=8126,
        description="Datadog trace agent port"
    )

    # ============================================================================
    # ENVIRONMENT & LOGGING
    # ============================================================================

    tikun_env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    output_dir: Path = Field(default=Path("./results"))

    # ============================================================================
    # MODEL CONFIGURATION (Defaults - Vertex AI Models)
    # ============================================================================

    keter_model: str = Field(default="gemini-2.5-pro")
    chochmah_model: str = Field(default="claude-3-5-sonnet-20241022")
    binah_west_model: str = Field(default="gemini-2.5-pro")
    binah_east_model: str = Field(default="deepseek-chat")
    chesed_model: str = Field(default="gemini-2.5-pro")
    gevurah_model: str = Field(default="gemini-2.5-pro")
    tiferet_model: str = Field(default="claude-3-5-sonnet-20241022")
    netzach_model: str = Field(default="gemini-2.5-pro")
    hod_model: str = Field(default="gemini-2.5-pro")
    yesod_model: str = Field(default="claude-3-5-sonnet-20241022")
    malchut_model: str = Field(default="claude-3-5-sonnet-20241022")

    # ============================================================================
    # SETTINGS
    # ============================================================================

    api_timeout: int = Field(default=120)
    max_retries: int = Field(default=3)
    rate_limit_rpm: int = Field(default=60)
    enable_cache: bool = Field(default=True)
    cache_ttl: int = Field(default=3600)
    
    binah_sigma_threshold: float = Field(default=0.15)
    binah_high_divergence_threshold: int = Field(default=40)

    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    api_docs_enabled: bool = Field(default=True)
    cors_origins: str = Field(default="*")

    enable_metrics: bool = Field(default=True)
    metrics_port: int = Field(default=9090)
    enable_tracing: bool = Field(default=False)

    api_auth_token: Optional[str] = Field(default=None)
    strict_validation: bool = Field(default=True)
    max_scenario_length: int = Field(default=50000)

    @field_validator("output_dir")
    @classmethod
    def create_output_dir(cls, v: Path) -> Path:
        v.mkdir(parents=True, exist_ok=True)
        return v

    @field_validator(
        "gemini_api_key",
        "anthropic_api_key",
        "deepseek_api_key",
        "openai_api_key",
        "grok_api_key",
        "mistral_api_key",
        "datadog_api_key",
        "datadog_app_key",
        mode="before"
    )
    @classmethod
    def strip_api_keys(cls, v: Optional[str]) -> Optional[str]:
        """Remove whitespace and newlines from API keys."""
        if v is None:
            return None
        if isinstance(v, str):
            return v.strip()
        return v

    def get_cors_origins_list(self) -> List[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]

    def is_development(self) -> bool:
        return self.tikun_env == "development"

    def get_model_for_sefirah(self, sefirah: str) -> str:
        model_attr = f"{sefirah.lower()}_model"
        return getattr(self, model_attr, "gemini-2.5-pro")

# Global config
_config: Optional[TikunConfig] = None

def get_config(reload: bool = False) -> TikunConfig:
    global _config
    if _config is None or reload:
        _config = TikunConfig()
    return _config