"""
Base class for all Sefirot

Provides common functionality for API calls, error handling,
retry logic, and logging.
"""

import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryError
)

# AI API clients — Gemini via OpenAI-compatible endpoint (no google-auth needed)
from openai import OpenAI, APIStatusError as OpenAIStatusError

from tikun.config import TikunConfig
from tikun.utils.logging import get_logger, PerformanceLogger

# Datadog observability
try:
    from ddtrace import tracer
    from monitoring.datadog_config import (
        emit_timing,
        emit_counter,
        add_span_tags,
        set_span_error
    )
    DATADOG_AVAILABLE = True
except ImportError:
    DATADOG_AVAILABLE = False
    tracer = None


class BaseSefirah(ABC):
    """
    Abstract base class for all Sefirot.

    Provides common functionality for:
    - AI API integration (Gemini, Claude, DeepSeek)
    - Prompt engineering
    - Error handling
    - Retry logic
    - Performance tracking
    """

    def __init__(self, config: TikunConfig, verbose: bool = False):
        """
        Initialize Sefirah.

        Args:
            config: Tikun configuration
            verbose: If True, enable verbose logging
        """
        self.config = config
        self.verbose = verbose
        self.logger = get_logger(self.__class__.__name__)

        # Initialize AI clients
        self._init_ai_clients()

    def _init_ai_clients(self) -> None:
        """Initialize AI API clients (multi-provider)."""
        from tikun.ai_clients import (
            get_gemini_client,
            get_deepseek_client,
            get_grok_client,
            get_mistral_client,
            get_openai_client,
        )
        # Gemini client is used inside call_gemini() directly

        # Gemini — primary fallback for all Sefirot (OpenAI-compatible endpoint)
        try:
            self.gemini_client = get_gemini_client(self.config)
            self.gemini_available = True
            self.logger.debug("Gemini client ready (OpenAI-compat)")
        except Exception as e:
            self.gemini_client = None
            self.gemini_available = False
            self.logger.error("Failed to initialize Gemini client", error=str(e))
            raise

        # Claude — disabled
        self.claude_client = None
        self.claude_available = False

        # DeepSeek — Binah East
        try:
            self.deepseek_client = get_deepseek_client(self.config)
            self.deepseek_available = True
            self.logger.debug("DeepSeek client ready")
        except Exception as e:
            self.deepseek_client = None
            self.deepseek_available = False
            self.logger.warning("DeepSeek unavailable", error=str(e))

        # Grok (xAI) — Keter, Malchut
        try:
            self.grok_client = get_grok_client(self.config)
            self.grok_available = True
            self.logger.debug("Grok (xAI) client ready")
        except Exception as e:
            self.grok_client = None
            self.grok_available = False
            self.logger.warning("Grok unavailable, will fallback to Gemini", error=str(e))

        # Mistral — Chochmah, Yesod
        try:
            self.mistral_client = get_mistral_client(self.config)
            self.mistral_available = True
            self.logger.debug("Mistral client ready")
        except Exception as e:
            self.mistral_client = None
            self.mistral_available = False
            self.logger.warning("Mistral unavailable, will fallback to Gemini", error=str(e))

        # OpenAI — Tiferet
        try:
            self.openai_client = get_openai_client(self.config)
            self.openai_available = True
            self.logger.debug("OpenAI client ready")
        except Exception as e:
            self.openai_client = None
            self.openai_available = False
            self.logger.warning("OpenAI unavailable, will fallback to Gemini", error=str(e))

    @abstractmethod
    def process(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process scenario through this Sefirah.

        Args:
            scenario: Input scenario text
            previous_results: Results from previous Sefirot

        Returns:
            Dictionary with processing results
        """
        pass

    @abstractmethod
    def get_prompt(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate prompt for this Sefirah.

        Args:
            scenario: Input scenario text
            previous_results: Results from previous Sefirot

        Returns:
            Formatted prompt string
        """
        pass

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def call_gemini(
        self,
        prompt: str,
        model: str = "gemini-2.0-flash",
        temperature: float = 0.7
    ) -> str:
        """
        Call Gemini via OpenAI-compatible endpoint with retry logic.

        Args:
            prompt: Prompt text
            model: Gemini model name
            temperature: Temperature for generation

        Returns:
            Response text
        """
        try:
            self.logger.debug(f"Calling Gemini (OpenAI-compat)", model=model)

            response = self.gemini_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=8192,
            )

            result = response.choices[0].message.content
            self.logger.debug(f"Gemini response received", length=len(result))
            return result

        except Exception as e:
            self.logger.error(
                f"Gemini API call failed",
                model=model,
                error=str(e),
                exc_info=True
            )
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def call_claude(
        self,
        prompt: str,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.7
    ) -> str:
        """
        Call Anthropic Claude API with retry logic.
        Falls back to Gemini if Claude is not available.

        Args:
            prompt: Prompt text
            model: Model identifier
            temperature: Temperature for generation

        Returns:
            Response text
        """
        if not self.claude_available or self.claude_client is None:
            self.logger.warning("Claude not available, using Gemini fallback")
            return self.call_gemini(prompt, model="gemini-2.0-flash", temperature=temperature)

        try:
            self.logger.debug(f"Calling Claude", model=model)

            response = self.claude_client.messages.create(
                model=model,
                max_tokens=8192,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response.content[0].text
            self.logger.debug(f"Claude response received", length=len(result))

            return result

        except Exception as e:
            self.logger.error(
                f"Claude API call failed, trying Vertex AI Gemini fallback",
                model=model,
                error=str(e)
            )
            # Fallback to Gemini on error
            return self.call_gemini(prompt, model="gemini-2.0-flash", temperature=temperature)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def call_deepseek(
        self,
        prompt: str,
        model: str = "deepseek-chat",
        temperature: float = 0.7
    ) -> str:
        """
        Call DeepSeek API with retry logic.

        Args:
            prompt: Prompt text
            model: Model identifier
            temperature: Temperature for generation

        Returns:
            Response text
        """
        try:
            self.logger.debug(f"Calling DeepSeek", model=model)

            response = self.deepseek_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=8192,
            )

            result = response.choices[0].message.content
            self.logger.debug(f"DeepSeek response received", length=len(result))
            return result

        except OpenAIStatusError as e:
            # 402 = saldo insuficiente — error permanente, NO reintentar
            if e.status_code == 402:
                self.logger.warning(
                    "DeepSeek 402 Insufficient Balance — fallback a VertexAI (no se reintenta)",
                    model=model
                )
                return self.call_gemini(prompt, model="gemini-2.0-flash", temperature=temperature)
            # Otros errores HTTP (429, 5xx) → el decorador @retry los reintenta
            self.logger.error(f"DeepSeek HTTP error {e.status_code}", model=model, error=str(e))
            raise

        except Exception as e:
            self.logger.error(
                f"DeepSeek API call failed",
                model=model,
                error=str(e),
                exc_info=True
            )
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def call_grok(
        self,
        prompt: str,
        model: str = "grok-3",
        temperature: float = 0.7
    ) -> str:
        """
        Call xAI Grok API (OpenAI-compatible).
        Fallback: VertexAI Gemini.
        Used by: Keter, Malchut
        """
        if not self.grok_available or self.grok_client is None:
            self.logger.warning("Grok unavailable, using VertexAI fallback")
            return self.call_gemini(prompt, model="gemini-2.0-flash", temperature=temperature)

        try:
            self.logger.debug(f"Calling Grok (xAI)", model=model)
            response = self.grok_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=8192,
            )
            result = response.choices[0].message.content
            self.logger.debug(f"Grok response received", length=len(result))
            return result

        except Exception as e:
            self.logger.error(
                f"Grok API call failed, falling back to VertexAI",
                model=model,
                error=str(e)
            )
            return self.call_gemini(prompt, model="gemini-2.0-flash", temperature=temperature)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def call_mistral(
        self,
        prompt: str,
        model: str = "mistral-large-latest",
        temperature: float = 0.7
    ) -> str:
        """
        Call Mistral AI API (OpenAI-compatible).
        Fallback: VertexAI Gemini.
        Used by: Chochmah, Yesod
        """
        if not self.mistral_available or self.mistral_client is None:
            self.logger.warning("Mistral unavailable, using VertexAI fallback")
            return self.call_gemini(prompt, model="gemini-2.0-flash", temperature=temperature)

        try:
            self.logger.debug(f"Calling Mistral", model=model)
            response = self.mistral_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=8192,
            )
            result = response.choices[0].message.content
            self.logger.debug(f"Mistral response received", length=len(result))
            return result

        except Exception as e:
            self.logger.error(
                f"Mistral API call failed, falling back to VertexAI",
                model=model,
                error=str(e)
            )
            return self.call_gemini(prompt, model="gemini-2.0-flash", temperature=temperature)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def call_openai(
        self,
        prompt: str,
        model: str = "gpt-4o",
        temperature: float = 0.7
    ) -> str:
        """
        Call OpenAI API.
        Fallback: VertexAI Gemini.
        Used by: Tiferet
        """
        if not self.openai_available or self.openai_client is None:
            self.logger.warning("OpenAI unavailable, using VertexAI fallback")
            return self.call_gemini(prompt, model="gemini-2.0-flash", temperature=temperature)

        try:
            self.logger.debug(f"Calling OpenAI", model=model)
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=8192,
            )
            result = response.choices[0].message.content
            self.logger.debug(f"OpenAI response received", length=len(result))
            return result

        except Exception as e:
            self.logger.error(
                f"OpenAI API call failed, falling back to VertexAI",
                model=model,
                error=str(e)
            )
            return self.call_gemini(prompt, model="gemini-2.0-flash", temperature=temperature)

    def safe_process(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Safely process scenario with error handling and Datadog instrumentation.

        Args:
            scenario: Input scenario text
            previous_results: Results from previous Sefirot

        Returns:
            Dictionary with results or error information
        """
        sefirah_name = self.__class__.__name__.lower()
        start_time = time.time()

        # Create Datadog span if available
        span = None
        if DATADOG_AVAILABLE and tracer:
            span = tracer.trace(
                f"sefira.{sefirah_name}",
                service=f"tikun-{sefirah_name}",
                resource=sefirah_name
            )

        try:
            with PerformanceLogger(self.logger, f"{sefirah_name}_processing"):
                result = self.process(scenario, previous_results)

            # Emit success metrics
            duration_ms = (time.time() - start_time) * 1000
            if DATADOG_AVAILABLE:
                emit_timing(f"{sefirah_name}.execution_time", duration_ms)
                emit_counter(f"{sefirah_name}.analysis_success", tags=['status:success'])

                if span:
                    add_span_tags({
                        'sefirah': sefirah_name,
                        'status': 'success',
                        'duration_ms': duration_ms
                    })

            return result

        except RetryError as e:
            self.logger.error(
                f"{sefirah_name} failed after retries",
                error=str(e),
                exc_info=True
            )

            # Emit error metrics
            if DATADOG_AVAILABLE:
                emit_counter(f"{sefirah_name}.analysis_error", tags=['status:error', 'error_type:retry'])
                if span:
                    set_span_error(e)

            return {
                "error": f"Failed after retries: {str(e)}",
                "status": "failed"
            }

        except Exception as e:
            self.logger.error(
                f"{sefirah_name} processing error",
                error=str(e),
                exc_info=True
            )

            # Emit error metrics
            if DATADOG_AVAILABLE:
                emit_counter(f"{sefirah_name}.analysis_error", tags=['status:error', f'error_type:{type(e).__name__}'])
                if span:
                    set_span_error(e)

            return {
                "error": str(e),
                "status": "failed"
            }

        finally:
            # Finish span
            if span:
                span.finish()

    def extract_field(
        self,
        text: str,
        field_name: str,
        default: Any = None
    ) -> Any:
        """
        Extract structured field from AI response.

        Args:
            text: Response text
            field_name: Field to extract (e.g., "alignment_percentage")
            default: Default value if extraction fails

        Returns:
            Extracted value or default
        """
        try:
            # Simple extraction patterns
            import re

            # Try to find "field_name: value" pattern
            pattern = rf"{field_name}[:\s]+([^\n]+)"
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                value = match.group(1).strip()

                # Try to parse as number
                try:
                    if '.' in value:
                        return float(value)
                    return int(value)
                except ValueError:
                    return value

            return default

        except Exception as e:
            self.logger.warning(
                f"Failed to extract field",
                field=field_name,
                error=str(e)
            )
            return default

    def extract_list(
        self,
        text: str,
        marker: str = "-",
        section: Optional[str] = None
    ) -> List[str]:
        """
        Extract list items from AI response.

        Args:
            text: Response text
            marker: List item marker (-, *, •)
            section: Optional section header to extract from

        Returns:
            List of extracted items
        """
        try:
            lines = text.split('\n')
            items = []

            in_section = section is None

            for line in lines:
                line = line.strip()

                # Check if we're entering the desired section
                if section and section.lower() in line.lower():
                    in_section = True
                    continue

                # Check if we're leaving the section
                if in_section and section and line and not line.startswith(marker):
                    if line.isupper() or line.endswith(':'):
                        break

                # Extract list items
                if in_section and line.startswith(marker):
                    item = line[len(marker):].strip()
                    if item:
                        items.append(item)

            return items

        except Exception as e:
            self.logger.warning(
                f"Failed to extract list",
                marker=marker,
                section=section,
                error=str(e)
            )
            return []

    def _strip_markdown(self, text: str) -> str:
        """
        Strip markdown formatting so regex parsers work regardless of AI provider.

        Mistral and Grok often return bold markers (**field:** value) or
        headers (## SECTION) that break plain-text regex patterns.
        """
        import re
        # Remove bold/italic markers: **text** or *text*
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'(?<!\*)\*(?!\*)', '', text)
        # Remove markdown headers: ## Header
        text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
        # Remove inline code: `value`
        text = re.sub(r'`([^`]+)`', r'\1', text)
        return text

    def format_previous_results(
        self,
        previous_results: Optional[Dict[str, Any]] = None,
        sefirot_to_include: Optional[List[str]] = None
    ) -> str:
        """
        Format previous Sefirot results for inclusion in prompt.

        Args:
            previous_results: Results dictionary
            sefirot_to_include: List of Sefirot names to include (default: all)

        Returns:
            Formatted string
        """
        if not previous_results:
            return ""

        lines = ["PREVIOUS SEFIROT RESULTS:", "=" * 80, ""]

        for sefirah, result in previous_results.items():
            if sefirot_to_include and sefirah not in sefirot_to_include:
                continue

            if isinstance(result, dict) and 'error' not in result:
                lines.append(f"{sefirah.upper()}:")
                lines.append("-" * 40)

                # Add key metrics
                for key, value in result.items():
                    if key in ['raw_analysis', 'raw_wisdom', 'raw_understanding']:
                        continue  # Skip raw text fields

                    if isinstance(value, (str, int, float, bool)):
                        lines.append(f"  {key}: {value}")

                lines.append("")

        return "\n".join(lines)
