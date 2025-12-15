"""
Data validation utilities for Tikun Olam

Provides input validation, sanitization, and security checks.
"""

import re
from typing import Optional, List, Dict, Any
from tikun.utils.logging import get_logger

logger = get_logger(__name__)

# Patterns for detecting potential security issues
SUSPICIOUS_PATTERNS = [
    r'<script',  # XSS attempts
    r'javascript:',  # JavaScript injection
    r'onerror\s*=',  # Event handler injection
    r'onclick\s*=',  # Event handler injection
    r'\$\{.*\}',  # Template injection
    r'{{.*}}',  # Template injection
    r'\bexec\b',  # Code execution
    r'\beval\b',  # Code evaluation
]

# Geopolitical keywords for BinahSigma activation
GEOPOLITICAL_KEYWORDS = {
    # Nations and blocs
    'china', 'russia', 'usa', 'america', 'europe', 'india', 'japan',
    'nato', 'brics', 'g7', 'g20', 'eu', 'asean',

    # Geopolitical concepts
    'geopolitical', 'sovereignty', 'sanctions', 'alliance', 'treaty',
    'diplomatic', 'territorial', 'border', 'conflict', 'war', 'peace',
    'military', 'defense', 'security', 'nuclear', 'weapon',

    # International organizations
    'un', 'united nations', 'world bank', 'imf', 'wto', 'who',

    # Economic-political
    'trade war', 'embargo', 'tariff', 'globalization', 'nationalism',
    'protectionism', 'hegemony', 'superpower', 'colonialism',

    # Values and systems
    'democracy', 'autocracy', 'communism', 'capitalism', 'socialism',
    'liberty', 'freedom', 'rights', 'justice', 'equality',

    # Specific conflicts
    'taiwan', 'ukraine', 'israel', 'palestine', 'kashmir', 'tibet',
    'south china sea', 'middle east', 'korean peninsula',
}


def validate_scenario(
    scenario: str,
    max_length: int = 50000,
    min_length: int = 50,
    check_suspicious: bool = True
) -> tuple[bool, Optional[str]]:
    """
    Validate scenario text for processing.

    Args:
        scenario: Input scenario text
        max_length: Maximum allowed length
        min_length: Minimum required length
        check_suspicious: If True, check for suspicious patterns

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if empty
    if not scenario or not scenario.strip():
        return False, "Scenario cannot be empty"

    scenario_clean = scenario.strip()

    # Check length
    if len(scenario_clean) < min_length:
        return False, f"Scenario too short (minimum {min_length} characters)"

    if len(scenario_clean) > max_length:
        return False, f"Scenario too long (maximum {max_length} characters)"

    # Check for suspicious patterns
    if check_suspicious:
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, scenario_clean, re.IGNORECASE):
                logger.warning(
                    f"Suspicious pattern detected in scenario",
                    pattern=pattern
                )
                return False, f"Scenario contains potentially unsafe content"

    return True, None


def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize text by removing potentially dangerous content.

    Args:
        text: Input text
        max_length: Optional maximum length to truncate to

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove null bytes
    text = text.replace('\x00', '')

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove control characters (except newlines and tabs)
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')

    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length]
        logger.debug(f"Text truncated to {max_length} characters")

    return text


def detect_geopolitical_content(text: str) -> tuple[bool, float, List[str]]:
    """
    Detect if text contains geopolitical content for BinahSigma activation.

    Args:
        text: Input text to analyze

    Returns:
        Tuple of (has_geopolitical_content, score, matched_keywords)
    """
    text_lower = text.lower()
    matched_keywords = []

    for keyword in GEOPOLITICAL_KEYWORDS:
        if keyword in text_lower:
            matched_keywords.append(keyword)

    # Calculate score based on unique keyword matches
    total_words = len(text.split())
    unique_matches = len(set(matched_keywords))

    # Score is percentage of geopolitical keyword density
    score = (unique_matches / max(total_words / 100, 1))  # per 100 words

    # Consider geopolitical if score > threshold or 3+ keywords
    is_geopolitical = score > 0.15 or unique_matches >= 3

    return is_geopolitical, score, matched_keywords


def validate_api_key(api_key: str, provider: str) -> tuple[bool, Optional[str]]:
    """
    Validate API key format.

    Args:
        api_key: API key to validate
        provider: Provider name (gemini, anthropic, deepseek, openai)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not api_key or not api_key.strip():
        return False, f"{provider} API key cannot be empty"

    api_key = api_key.strip()

    # Basic length checks
    if len(api_key) < 10:
        return False, f"{provider} API key too short"

    if len(api_key) > 500:
        return False, f"{provider} API key too long"

    # Provider-specific validation
    if provider.lower() == "gemini":
        # Gemini keys typically start with "AI"
        if not api_key.startswith("AI"):
            logger.warning(f"Gemini API key has unexpected format")

    elif provider.lower() == "anthropic":
        # Anthropic keys typically start with "sk-ant-"
        if not api_key.startswith("sk-ant-"):
            logger.warning(f"Anthropic API key has unexpected format")

    elif provider.lower() == "openai":
        # OpenAI keys typically start with "sk-"
        if not api_key.startswith("sk-"):
            logger.warning(f"OpenAI API key has unexpected format")

    return True, None


def validate_results(results: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate results dictionary structure.

    Args:
        results: Results dictionary to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check required top-level keys
    required_keys = ['sefirot_results', 'metadata']
    for key in required_keys:
        if key not in results:
            errors.append(f"Missing required key: {key}")

    if 'sefirot_results' in results:
        sefirot_results = results['sefirot_results']

        # Check if it's a dictionary
        if not isinstance(sefirot_results, dict):
            errors.append("sefirot_results must be a dictionary")
        else:
            # Check for expected sefirot
            expected_sefirot = [
                'keter', 'chochmah', 'binah', 'chesed', 'gevurah',
                'tiferet', 'netzach', 'hod', 'yesod', 'malchut'
            ]

            for sefirah in expected_sefirot:
                if sefirah not in sefirot_results:
                    errors.append(f"Missing sefirah: {sefirah}")
                elif isinstance(sefirot_results[sefirah], dict):
                    # Check for error indicator
                    if 'error' in sefirot_results[sefirah]:
                        errors.append(
                            f"{sefirah} has error: {sefirot_results[sefirah]['error']}"
                        )

    if 'metadata' in results:
        metadata = results['metadata']

        if not isinstance(metadata, dict):
            errors.append("metadata must be a dictionary")
        else:
            # Check for required metadata fields
            required_metadata = ['timestamp', 'version', 'case_name']
            for field in required_metadata:
                if field not in metadata:
                    errors.append(f"Missing metadata field: {field}")

    is_valid = len(errors) == 0
    return is_valid, errors


def truncate_for_display(
    text: str,
    max_length: int = 100,
    suffix: str = "..."
) -> str:
    """
    Truncate text for display purposes.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix
