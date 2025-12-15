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
        description="OpenAI API Key (optional fallback)"
    )

    # ============================================================================
    # ENVIRONMENT & LOGGING
    # ============================================================================

    tikun_env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    output_dir: Path = Field(default=Path("./results"))

    # ============================================================================
    # MODEL CONFIGURATION (Defaults)
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

    def get_cors_origins_list(self) -> List[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]

    def is_development(self) -> bool:
        return self.tikun_env == "development"

    def get_model_for_sefirah(self, sefirah: str) -> str:
        model_attr = f"{sefirah.lower()}_model"
        return getattr(self, model_attr, "gemini-2.0-flash-exp")

# Global config
_config: Optional[TikunConfig] = None

def get_config(reload: bool = False) -> TikunConfig:
    global _config
    if _config is None or reload:
        _config = TikunConfig()
    return _config