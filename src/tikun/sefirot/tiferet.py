"""
Tiferet (Beauty) - Synthesis & Balance

Sixth Sefirah: Synthesizes Chesed and Gevurah, creates harmony and balance.
"""

import re
from typing import Dict, Any, Optional
from tikun.sefirot.base import BaseSefirah
from tikun.models.schemas import TiferetResult


class Tiferet(BaseSefirah):
    """Tiferet creates synthesis and balance between opportunity and risk."""

    def get_prompt(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> str:
        context = self.format_previous_results(previous_results, ['chesed', 'gevurah'])

        return f"""You are TIFERET (תפארת - Beauty), the sixth Sefirah in the Tikun Olam ethical reasoning architecture.

Your role is to create SYNTHESIS and BALANCE.

{context}

SCENARIO:
{scenario}

YOUR TASK:
Balance Chesed (opportunity/expansion) and Gevurah (risk/constraint):

1. HARMONY SCORE (0-100%): How harmonious is the overall proposal?
2. BALANCE QUALITY: poor/acceptable/good/excellent

3. SYNTHESIS STATEMENT:
   - Integrate opportunities and risks
   - Create coherent vision

4. CHESED-GEVURAH BALANCE:
   - Are opportunities and risks balanced?
   - Is expansion matched by appropriate constraint?

5. KEY TRADEOFFS:
   - What must be sacrificed for what gain?
   - Necessary compromises

6. RECOMMENDED APPROACH:
   - Path that balances both

OUTPUT FORMAT:
harmony_score: [0-100]
balance_quality: [quality]

SYNTHESIS STATEMENT:
[Your integrated vision]

CHESED-GEVURAH BALANCE:
[Analysis of balance]

KEY TRADEOFFS:
- [Tradeoff 1]

RECOMMENDED APPROACH:
[Your recommendation]

SYNTHESIS ANALYSIS:
[Detailed analysis]
"""

    def process(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info("Processing Tiferet (Synthesis)")
        model = self.config.get_model_for_sefirah("tiferet")
        prompt = self.get_prompt(scenario, previous_results)
        response = self.call_claude(prompt, model=model)
        return self._parse_response(response)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            harmony = self._extract_percentage(response, "harmony_score", 65)

            quality_match = re.search(r'balance_quality[:\s]+(poor|acceptable|good|excellent)', response, re.IGNORECASE)
            quality = quality_match.group(1).lower() if quality_match else "acceptable"

            synthesis_match = re.search(r'SYNTHESIS STATEMENT:(.+?)(?:CHESED-GEVURAH BALANCE:|KEY TRADEOFFS:|$)', response, re.DOTALL | re.IGNORECASE)
            synthesis = synthesis_match.group(1).strip() if synthesis_match else ""

            balance_match = re.search(r'CHESED-GEVURAH BALANCE:(.+?)(?:KEY TRADEOFFS:|RECOMMENDED APPROACH:|$)', response, re.DOTALL | re.IGNORECASE)
            balance = balance_match.group(1).strip() if balance_match else ""

            tradeoffs = self.extract_list(response, section="KEY TRADEOFFS")

            approach_match = re.search(r'RECOMMENDED APPROACH:(.+?)(?:SYNTHESIS ANALYSIS:|$)', response, re.DOTALL | re.IGNORECASE)
            approach = approach_match.group(1).strip() if approach_match else ""

            result_data = {
                "harmony_score": harmony,
                "balance_quality": quality,
                "synthesis_statement": synthesis,
                "chesed_gevurah_balance": balance,
                "key_tradeoffs": tradeoffs,
                "recommended_approach": approach,
                "raw_synthesis": response
            }

            return TiferetResult(**result_data).model_dump()

        except Exception as e:
            self.logger.error("Failed to parse Tiferet response", error=str(e))
            return {
                "harmony_score": 50,
                "balance_quality": "acceptable",
                "synthesis_statement": "",
                "chesed_gevurah_balance": "",
                "key_tradeoffs": [],
                "recommended_approach": "",
                "raw_synthesis": response
            }

    def _extract_percentage(self, text: str, field: str, default: int = 50) -> int:
        value = self.extract_field(text, field, default)
        if isinstance(value, str):
            match = re.search(r'\d+', value)
            value = int(match.group()) if match else default
        return max(0, min(100, value))
