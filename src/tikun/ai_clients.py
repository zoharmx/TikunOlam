"""
Shared AI client initialization (Singleton pattern)

This module ensures AI clients are initialized only once and shared
across all Sefirot to eliminate redundant initialization overhead.
"""

import vertexai
from openai import OpenAI
from typing import Optional
from tikun.config import TikunConfig
from tikun.utils.logging import get_logger

logger = get_logger(__name__)

# Global flags to track initialization
_vertex_initialized = False
_deepseek_client: Optional[OpenAI] = None


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


def reset_clients() -> None:
    """Reset all clients (for testing purposes)."""
    global _vertex_initialized, _deepseek_client
    _vertex_initialized = False
    _deepseek_client = None
    logger.info("AI clients reset")
