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

# AI API clients
import google.generativeai as genai
from anthropic import Anthropic
from openai import OpenAI

from tikun.config import TikunConfig
from tikun.utils.logging import get_logger, PerformanceLogger


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
        """Initialize AI API clients."""
        try:
            # Gemini (always required)
            genai.configure(api_key=self.config.gemini_api_key)
            self.logger.debug("Gemini client configured")

            # Claude (Anthropic) - optional, fallback to Gemini if not available
            try:
                if self.config.anthropic_api_key and self.config.anthropic_api_key not in ['placeholder', 'placeholder_no_usado', 'your_anthropic_api_key_here']:
                    self.claude_client = Anthropic(api_key=self.config.anthropic_api_key)
                    self.claude_available = True
                    self.logger.debug("Claude client configured")
                else:
                    self.claude_client = None
                    self.claude_available = False
                    self.logger.warning("Claude API key not configured - will use Gemini fallback")
            except Exception as e:
                self.claude_client = None
                self.claude_available = False
                self.logger.warning(f"Claude client initialization failed - using Gemini fallback: {str(e)}")

            # DeepSeek (OpenAI-compatible)
            self.deepseek_client = OpenAI(
                api_key=self.config.deepseek_api_key,
                base_url="https://api.deepseek.com"
            )
            self.logger.debug("DeepSeek client configured")

        except Exception as e:
            self.logger.error(
                f"Failed to initialize AI clients",
                error=str(e),
                exc_info=True
            )
            raise

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
        model: str = "gemini-2.0-flash-exp",
        temperature: float = 0.7
    ) -> str:
        """
        Call Google Gemini API with retry logic.

        Args:
            prompt: Prompt text
            model: Model identifier
            temperature: Temperature for generation

        Returns:
            Response text
        """
        try:
            self.logger.debug(f"Calling Gemini", model=model)

            gemini_model = genai.GenerativeModel(model)

            response = gemini_model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=8192,
                )
            )

            result = response.text
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
        # Fallback to Gemini if Claude not available
        if not self.claude_available or self.claude_client is None:
            self.logger.warning(f"Claude not available, using Gemini fallback for this call")
            return self.call_gemini(prompt, model="gemini-2.0-flash-exp", temperature=temperature)

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
                f"Claude API call failed, trying Gemini fallback",
                model=model,
                error=str(e)
            )
            # Fallback to Gemini on error
            return self.call_gemini(prompt, model="gemini-2.0-flash-exp", temperature=temperature)

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
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=8192,
            )

            result = response.choices[0].message.content
            self.logger.debug(f"DeepSeek response received", length=len(result))

            return result

        except Exception as e:
            self.logger.error(
                f"DeepSeek API call failed",
                model=model,
                error=str(e),
                exc_info=True
            )
            raise

    def safe_process(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Safely process scenario with error handling.

        Args:
            scenario: Input scenario text
            previous_results: Results from previous Sefirot

        Returns:
            Dictionary with results or error information
        """
        sefirah_name = self.__class__.__name__.lower()

        try:
            with PerformanceLogger(self.logger, f"{sefirah_name}_processing"):
                result = self.process(scenario, previous_results)

            return result

        except RetryError as e:
            self.logger.error(
                f"{sefirah_name} failed after retries",
                error=str(e),
                exc_info=True
            )
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
            return {
                "error": str(e),
                "status": "failed"
            }

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
