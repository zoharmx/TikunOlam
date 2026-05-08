"""
Shared AI client initialization (Singleton pattern)

Gemini se accede vía su endpoint OpenAI-compatible para evitar
dependencias de google-auth/vertexai que rompen en este entorno.

Provider distribution:
  Keter    → Gemini (fallback de Grok)
  Chochmah → Mistral
  Binah    → Gemini (West) + DeepSeek (East)
  Chesed   → Gemini
  Gevurah  → Gemini
  Tiferet  → OpenAI
  Netzach  → Gemini
  Hod      → Gemini
  Yesod    → Mistral
  Malchut  → Gemini (fallback de Grok)
"""

from openai import OpenAI
from typing import Optional
from tikun.config import TikunConfig
from tikun.utils.logging import get_logger

logger = get_logger(__name__)

# Gemini OpenAI-compatible base URL
_GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

_gemini_client:   Optional[OpenAI] = None
_deepseek_client: Optional[OpenAI] = None
_grok_client:     Optional[OpenAI] = None
_mistral_client:  Optional[OpenAI] = None
_openai_client:   Optional[OpenAI] = None


def init_vertex_ai(config: TikunConfig) -> None:
    """Compatibility shim — delegates to get_gemini_client."""
    get_gemini_client(config)


def get_gemini_client(config: TikunConfig) -> OpenAI:
    """Gemini via OpenAI-compatible endpoint (singleton)."""
    global _gemini_client
    if _gemini_client is None:
        logger.info("Initializing Gemini (OpenAI-compat) client...")
        _gemini_client = OpenAI(
            api_key=config.gemini_api_key,
            base_url=_GEMINI_BASE_URL,
        )
        logger.info("Gemini client ready")
    return _gemini_client


def get_deepseek_client(config: TikunConfig) -> OpenAI:
    """DeepSeek client (singleton)."""
    global _deepseek_client
    if _deepseek_client is None:
        if not config.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY not configured")
        logger.info("Initializing DeepSeek client...")
        _deepseek_client = OpenAI(
            api_key=config.deepseek_api_key,
            base_url="https://api.deepseek.com",
        )
        logger.info("DeepSeek client ready")
    return _deepseek_client


def get_grok_client(config: TikunConfig) -> OpenAI:
    """Grok (xAI) client (singleton)."""
    global _grok_client
    if _grok_client is None:
        if not config.grok_api_key:
            raise ValueError("GROK_API_KEY not configured")
        logger.info("Initializing Grok (xAI) client...")
        _grok_client = OpenAI(
            api_key=config.grok_api_key,
            base_url="https://api.x.ai/v1",
        )
        logger.info("Grok client ready")
    return _grok_client


def get_mistral_client(config: TikunConfig) -> OpenAI:
    """Mistral client (singleton)."""
    global _mistral_client
    if _mistral_client is None:
        if not config.mistral_api_key:
            raise ValueError("MISTRAL_API_KEY not configured")
        logger.info("Initializing Mistral client...")
        _mistral_client = OpenAI(
            api_key=config.mistral_api_key,
            base_url="https://api.mistral.ai/v1",
        )
        logger.info("Mistral client ready")
    return _mistral_client


def get_openai_client(config: TikunConfig) -> OpenAI:
    """OpenAI client (singleton)."""
    global _openai_client
    if _openai_client is None:
        if not config.openai_api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        logger.info("Initializing OpenAI client...")
        _openai_client = OpenAI(api_key=config.openai_api_key)
        logger.info("OpenAI client ready")
    return _openai_client


def reset_clients() -> None:
    """Reset all clients (for testing)."""
    global _gemini_client, _deepseek_client, _grok_client, _mistral_client, _openai_client
    _gemini_client = None
    _deepseek_client = None
    _grok_client = None
    _mistral_client = None
    _openai_client = None
    logger.info("AI clients reset")
