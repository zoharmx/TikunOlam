"""
Hod (Splendor) - Communication Design

Eighth Sefirah: Designs communication strategies for different stakeholders.
"""

import re
from typing import Dict, Any, Optional
from tikun.sefirot.base import BaseSefirah
from tikun.models.schemas import HodResult, CommunicationChannel


class Hod(BaseSefirah):
    """Hod designs communication and messaging strategies."""

    def get_prompt(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> str:
        context = self.format_previous_results(previous_results, ['netzach'])

        return f"""You are HOD (הוד - Splendor), the eighth Sefirah in the Tikun Olam ethical reasoning architecture.

Your role is COMMUNICATION DESIGN.

{context}

SCENARIO:
{scenario}

YOUR TASK:
Design communication strategies:

1. CLARITY SCORE (0-100%): How clear can messaging be?
2. COMMUNICATION QUALITY: poor/acceptable/good/excellent

3. COMMUNICATION CHANNELS (list 3-5):
   For each audience:
   - Audience: who
   - Key Messages: what to communicate
   - Tone: how to communicate
   - Medium: channels to use

4. STAKEHOLDER MESSAGING:
   Specific messages for different groups

5. TRANSPARENCY REQUIREMENTS:
   What must be disclosed

OUTPUT FORMAT:
clarity_score: [0-100]
communication_quality: [quality]

COMMUNICATION CHANNELS:
- Audience: [audience name]
  Key Messages: [message 1], [message 2]
  Tone: [tone description]
  Medium: [medium 1], [medium 2]

STAKEHOLDER MESSAGING:
[Group 1]: [specific message]

TRANSPARENCY REQUIREMENTS:
- [requirement 1]

COMMUNICATION ANALYSIS:
[Analysis]
"""

    def process(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info("Processing Hod (Communication)")
        model = self.config.get_model_for_sefirah("hod")
        prompt = self.get_prompt(scenario, previous_results)
        response = self.call_gemini(prompt, model=model)
        return self._parse_response(response)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            clarity = self._extract_percentage(response, "clarity_score", 70)

            quality_match = re.search(r'communication_quality[:\s]+(poor|acceptable|good|excellent)', response, re.IGNORECASE)
            quality = quality_match.group(1).lower() if quality_match else "acceptable"

            channels = self._extract_channels(response)

            stakeholder_messaging = {}
            msg_section = re.search(r'STAKEHOLDER MESSAGING:(.+?)(?:TRANSPARENCY REQUIREMENTS:|COMMUNICATION ANALYSIS:|$)', response, re.DOTALL | re.IGNORECASE)
            if msg_section:
                for line in msg_section.group(1).split('\n'):
                    if ':' in line:
                        parts = line.split(':', 1)
                        stakeholder_messaging[parts[0].strip()] = parts[1].strip()

            transparency = self.extract_list(response, section="TRANSPARENCY REQUIREMENTS")

            result_data = {
                "clarity_score": clarity,
                "communication_quality": quality,
                "channels": channels,
                "stakeholder_messaging": stakeholder_messaging,
                "transparency_requirements": transparency,
                "raw_communication": response
            }

            return HodResult(**result_data).model_dump()

        except Exception as e:
            self.logger.error("Failed to parse Hod response", error=str(e))
            return {
                "clarity_score": 50,
                "communication_quality": "acceptable",
                "channels": [],
                "stakeholder_messaging": {},
                "transparency_requirements": [],
                "raw_communication": response
            }

    def _extract_percentage(self, text: str, field: str, default: int = 50) -> int:
        value = self.extract_field(text, field, default)
        if isinstance(value, str):
            match = re.search(r'\d+', value)
            value = int(match.group()) if match else default
        return max(0, min(100, value))

    def _extract_channels(self, response: str) -> list:
        channels = []
        try:
            section = re.search(r'COMMUNICATION CHANNELS:(.+?)(?:STAKEHOLDER MESSAGING:|$)', response, re.DOTALL | re.IGNORECASE)
            if section:
                blocks = re.split(r'\n-\s*Audience:', section.group(1))
                for block in blocks[1:]:
                    aud_match = re.search(r'^([^\n]+)', block)
                    msg_match = re.search(r'Key Messages:\s*([^\n]+)', block)
                    tone_match = re.search(r'Tone:\s*([^\n]+)', block)
                    med_match = re.search(r'Medium:\s*([^\n]+)', block)

                    if aud_match:
                        channel = CommunicationChannel(
                            audience=aud_match.group(1).strip(),
                            key_messages=[m.strip() for m in msg_match.group(1).split(",")] if msg_match else [],
                            tone=tone_match.group(1).strip() if tone_match else "professional",
                            medium=[m.strip() for m in med_match.group(1).split(",")] if med_match else []
                        )
                        channels.append(channel.model_dump())
        except Exception as e:
            self.logger.warning("Failed to extract channels", error=str(e))
        return channels
