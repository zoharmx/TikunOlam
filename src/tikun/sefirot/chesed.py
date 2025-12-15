"""
Chesed (Kindness) - Opportunity Evaluation

Fourth Sefirah: Identifies opportunities, benefits, and positive potential.
"""

import re
from typing import Dict, Any, Optional
from tikun.sefirot.base import BaseSefirah
from tikun.models.schemas import ChesedResult, Opportunity


class Chesed(BaseSefirah):
    """Chesed evaluates expansion potential and opportunities."""

    def get_prompt(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> str:
        context = self.format_previous_results(previous_results, ['keter', 'chochmah', 'binah'])

        return f"""You are CHESED (חסד - Kindness), the fourth Sefirah in the Tikun Olam ethical reasoning architecture.

Your role is to identify OPPORTUNITIES and POSITIVE POTENTIAL.

{context}

SCENARIO:
{scenario}

YOUR TASK:
1. EXPANSION POTENTIAL (0-100%): How much positive growth is possible?
2. GENEROSITY SCORE (0-100%): How generous/beneficial is this proposal?

3. OPPORTUNITIES (list 3-5):
   For each:
   - Description
   - Potential Impact: low/medium/high/transformative
   - Beneficiaries: who benefits
   - Confidence: 0-100%

4. LONG-TERM BENEFITS (list 3-5)
5. POSITIVE EXTERNALITIES (unintended benefits)

OUTPUT FORMAT:
expansion_potential: [0-100]
generosity_score: [0-100]

OPPORTUNITIES:
- Description: [opportunity]
  Impact: [level]
  Beneficiaries: [list]
  Confidence: [0-100]

LONG-TERM BENEFITS:
- [benefit 1]

POSITIVE EXTERNALITIES:
- [externality 1]

OPPORTUNITY ANALYSIS:
[Your analysis]
"""

    def process(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info("Processing Chesed (Opportunity)")
        model = self.config.get_model_for_sefirah("chesed")
        prompt = self.get_prompt(scenario, previous_results)
        response = self.call_gemini(prompt, model=model)
        return self._parse_response(response)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            expansion = self._extract_percentage(response, "expansion_potential", 60)
            generosity = self._extract_percentage(response, "generosity_score", 60)

            opportunities = self._extract_opportunities(response)
            benefits = self.extract_list(response, section="LONG-TERM BENEFITS")
            externalities = self.extract_list(response, section="POSITIVE EXTERNALITIES")

            result_data = {
                "expansion_potential": expansion,
                "generosity_score": generosity,
                "opportunities": opportunities,
                "long_term_benefits": benefits,
                "positive_externalities": externalities,
                "raw_opportunity": response
            }

            return ChesedResult(**result_data).model_dump()

        except Exception as e:
            self.logger.error("Failed to parse Chesed response", error=str(e))
            return {
                "expansion_potential": 50,
                "generosity_score": 50,
                "opportunities": [],
                "long_term_benefits": [],
                "positive_externalities": [],
                "raw_opportunity": response
            }

    def _extract_percentage(self, text: str, field: str, default: int = 50) -> int:
        value = self.extract_field(text, field, default)
        if isinstance(value, str):
            match = re.search(r'\d+', value)
            value = int(match.group()) if match else default
        return max(0, min(100, value))

    def _extract_opportunities(self, response: str) -> list:
        opportunities = []
        try:
            section = re.search(r'OPPORTUNITIES:(.+?)(?:LONG-TERM BENEFITS:|$)', response, re.DOTALL | re.IGNORECASE)
            if section:
                blocks = re.split(r'\n-\s*Description:', section.group(1))
                for block in blocks[1:]:
                    desc_match = re.search(r'^([^\n]+)', block)
                    impact_match = re.search(r'Impact:\s*(\w+)', block, re.IGNORECASE)
                    benef_match = re.search(r'Beneficiaries:\s*([^\n]+)', block)
                    conf_match = re.search(r'Confidence:\s*(\d+)', block)

                    if desc_match:
                        opp = Opportunity(
                            description=desc_match.group(1).strip(),
                            potential_impact=impact_match.group(1).lower() if impact_match else "medium",
                            beneficiaries=[b.strip() for b in benef_match.group(1).split(",")] if benef_match else [],
                            confidence=int(conf_match.group(1)) if conf_match else 70
                        )
                        opportunities.append(opp.model_dump())
        except Exception as e:
            self.logger.warning("Failed to extract opportunities", error=str(e))
        return opportunities
