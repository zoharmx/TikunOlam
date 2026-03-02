"""
Shared AI client initialization (Singleton pattern)

This module ensures AI clients are initialized only once and shared
across all Sefirot to eliminate redundant initialization overhead.

Provider distribution (Feb 2026):
  Keter    → Grok (xAI)
  Chochmah → Mistral
  Binah    → VertexAI (West) + DeepSeek (East)
  Chesed   → VertexAI
  Gevurah  → VertexAI
  Tiferet  → OpenAI
  Netzach  → DeepSeek
  Hod      → VertexAI
  Yesod    → Mistral
  Malchut  → Grok (xAI)
  Fallback → VertexAI
"""

import vertexai
from openai import OpenAI
from typing import Optional
from tikun.config import TikunConfig
from tikun.utils.logging import get_logger

logger = get_logger(__name__)

# Global flags / singleton clients
_vertex_initialized = False
_deepseek_client: Optional[OpenAI] = None
_grok_client: Optional[OpenAI] = None
_mistral_client: Optional[OpenAI] = None
_openai_client: Optional[OpenAI] = None


def init_vertex_ai(config: TikunConfig) -> None:
    """
    Initialize Vertex AI (Google Gemini) once globally.

    Subsequent calls are no-ops.

    Args:
        config: Tikun configuration
    """
    global _vertex_initialized

    if _vertex_initialized:
        logger.debug("Vertex AI already initialized, skipping")
        return

    try:
        logger.info("Initializing Vertex AI (first time)...")
        vertexai.init(
            project=config.gcp_project_id,
            location=config.gcp_location
        )
        _vertex_initialized = True
        logger.info(f"Vertex AI initialized successfully",
                   project=config.gcp_project_id,
                   location=config.gcp_location)
    except Exception as e:
        logger.error(f"Failed to initialize Vertex AI", error=str(e), exc_info=True)
        raise


def get_deepseek_client(config: TikunConfig) -> OpenAI:
    """
    Get shared DeepSeek client (singleton).

    Args:
        config: Tikun configuration

    Returns:
        OpenAI client configured for DeepSeek
    """
    global _deepseek_client

    if _deepseek_client is None:
        logger.info("Initializing DeepSeek client (first time)...")
        _deepseek_client = OpenAI(
            api_key=config.deepseek_api_key,
            base_url="https://api.deepseek.com"
        )
        logger.info("DeepSeek client initialized successfully")

    return _deepseek_client


def get_grok_client(config: TikunConfig) -> OpenAI:
    """
    Get shared Grok (xAI) client (singleton).
    Used by: Keter, Malchut
    """
    global _grok_client

    if _grok_client is None:
        if not config.grok_api_key:
            raise ValueError("GROK_API_KEY not configured")
        logger.info("Initializing Grok (xAI) client (first time)...")
        _grok_client = OpenAI(
            api_key=config.grok_api_key,
            base_url="https://api.x.ai/v1"
        )
        logger.info("Grok client initialized successfully")

    return _grok_client


def get_mistral_client(config: TikunConfig) -> OpenAI:
    """
    Get shared Mistral client (singleton).
    Used by: Chochmah, Yesod
    """
    global _mistral_client

    if _mistral_client is None:
        if not config.mistral_api_key:
            raise ValueError("MISTRAL_API_KEY not configured")
        logger.info("Initializing Mistral client (first time)...")
        _mistral_client = OpenAI(
            api_key=config.mistral_api_key,
            base_url="https://api.mistral.ai/v1"
        )
        logger.info("Mistral client initialized successfully")

    return _mistral_client


def get_openai_client(config: TikunConfig) -> OpenAI:
    """
    Get shared OpenAI client (singleton).
    Used by: Tiferet
    """
    global _openai_client

    if _openai_client is None:
        if not config.openai_api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        logger.info("Initializing OpenAI client (first time)...")
        _openai_client = OpenAI(api_key=config.openai_api_key)
        logger.info("OpenAI client initialized successfully")

    return _openai_client


def reset_clients() -> None:
    """Reset all clients (for testing purposes)."""
    global _vertex_initialized, _deepseek_client, _grok_client, _mistral_client, _openai_client
    _vertex_initialized = False
    _deepseek_client = None
    _grok_client = None
    _mistral_client = None
    _openai_client = None
    logger.info("AI clients reset")
