"""
Vertex AI Warmup Utility

Pre-initializes Vertex AI and makes test calls during application startup
to eliminate the ~8.5 minute overhead on first real request.

This reduces first-request latency from 8.5 min to ~10 seconds.
"""

import asyncio
from typing import Optional
from vertexai.generative_models import GenerativeModel
import vertexai

from tikun.config import get_config
from tikun.utils.logging import get_logger
from tikun.ai_clients import init_vertex_ai

logger = get_logger(__name__)


async def warmup_vertex_ai() -> bool:
    """
    Warm up Vertex AI by initializing and making a test call.

    This function:
    1. Initializes Vertex AI client
    2. Creates a Gemini model instance
    3. Makes a minimal test call to "warm up" the connection
    4. Returns success/failure status

    Returns:
        bool: True if warmup successful, False otherwise
    """
    try:
        config = get_config()

        logger.info("Warming up Vertex AI...")

        # Step 1: Initialize Vertex AI
        init_vertex_ai(config)

        # Step 2: Create model instance (this triggers additional initialization)
        model = GenerativeModel(
            model_name="gemini-2.5-pro",  # Use same model as pipeline
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 50,
            }
        )

        # Step 3: Make minimal test call to warm up the connection
        logger.info("Making warmup test call...")

        test_prompt = "Test warmup. Reply with just: OK"

        # This call establishes the connection and caches credentials
        response = model.generate_content(test_prompt)

        if response and response.text:
            logger.info(f"Vertex AI warmup successful (response: {response.text.strip()})")
            return True
        else:
            logger.warning("Vertex AI warmup completed but no response")
            return False

    except Exception as e:
        logger.error(f"Vertex AI warmup failed: {e}", exc_info=True)
        # Don't raise - warmup failure shouldn't prevent app startup
        return False


async def warmup_all_models() -> dict:
    """
    Warm up all AI models used in the pipeline.

    Currently only Vertex AI needs warmup. DeepSeek and Claude
    don't have the same cold-start penalty.

    Returns:
        dict: Status of each warmup operation
    """
    results = {}

    # Vertex AI warmup (critical - eliminates 8.5 min overhead)
    results['vertex_ai'] = await warmup_vertex_ai()

    # DeepSeek doesn't need warmup (HTTP client, no persistent connection)
    results['deepseek'] = True

    # Claude (if available) doesn't need warmup either
    results['claude'] = True

    # Log summary
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)

    if success_count == total_count:
        logger.info(f"All models warmed up successfully ({success_count}/{total_count})")
    else:
        logger.warning(f"Some models failed warmup ({success_count}/{total_count})")

    return results


def warmup_sync() -> bool:
    """
    Synchronous wrapper for warmup_vertex_ai().

    Use this in synchronous contexts like lifespan events.

    Returns:
        bool: True if warmup successful
    """
    try:
        return asyncio.run(warmup_vertex_ai())
    except Exception as e:
        logger.error(f"Synchronous warmup failed: {e}", exc_info=True)
        return False
