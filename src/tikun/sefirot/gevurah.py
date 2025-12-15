"""
Gevurah (Strength) - Risk Assessment

Fifth Sefirah: Identifies risks, constraints, and potential harms.
"""

import re
from typing import Dict, Any, Optional
from tikun.sefirot.base import BaseSefirah
from tikun.models.schemas import GevurahResult, Risk


class Gevurah(BaseSefirah):
    """Gevurah evaluates risks and establishes boundaries."""

    def get_prompt(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> str:
        context = self.format_previous_results(previous_results, ['keter', 'chesed'])

        return f"""You are GEVURAH (גבורה - Strength), the fifth Sefirah in the Tikun Olam ethical reasoning architecture.

Your role is to assess RISKS and CONSTRAINTS.

{context}

SCENARIO:
{scenario}

YOUR TASK:
1. CONSTRAINT STRENGTH (0-100%): How strong are the constraints/limitations?
2. RISK SEVERITY: none/low/medium/high/critical

3. RISKS (list 3-5):
   For each:
   - Description
   - Severity: low/medium/high/critical
   - Probability: unlikely/possible/likely/certain
   - Affected Parties: who is harmed
   - Mitigation: how to reduce risk

4. BOUNDARIES IDENTIFIED (what limits exist)
5. NEGATIVE EXTERNALITIES (unintended harms)
6. IRREVERSIBLE CONSEQUENCES (cannot be undone)

OUTPUT FORMAT:
constraint_strength: [0-100]
risk_severity: [level]

RISKS:
- Description: [risk]
  Severity: [level]
  Probability: [level]
  Affected Parties: [list]
  Mitigation: [strategy]

BOUNDARIES:
- [boundary 1]

NEGATIVE EXTERNALITIES:
- [externality 1]

IRREVERSIBLE CONSEQUENCES:
- [consequence 1]

RISK ANALYSIS:
[Your analysis]
"""

    def process(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info("Processing Gevurah (Risk)")
        model = self.config.get_model_for_sefirah("gevurah")
        prompt = self.get_prompt(scenario, previous_results)
        response = self.call_gemini(prompt, model=model)
        return self._parse_response(response)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            constraint = self._extract_percentage(response, "constraint_strength", 50)

            severity_match = re.search(r'risk_severity[:\s]+(none|low|medium|high|critical)', response, re.IGNORECASE)
            severity = severity_match.group(1).lower() if severity_match else "medium"

            risks = self._extract_risks(response)
            boundaries = self.extract_list(response, section="BOUNDARIES")
            neg_extern = self.extract_list(response, section="NEGATIVE EXTERNALITIES")
            irreversible = self.extract_list(response, section="IRREVERSIBLE CONSEQUENCES")

            result_data = {
                "constraint_strength": constraint,
                "risk_severity": severity,
                "risks": risks,
                "boundaries_identified": boundaries,
                "negative_externalities": neg_extern,
                "irreversible_consequences": irreversible,
                "raw_risk": response
            }

            return GevurahResult(**result_data).model_dump()

        except Exception as e:
            self.logger.error("Failed to parse Gevurah response", error=str(e))
            return {
                "constraint_strength": 50,
                "risk_severity": "medium",
                "risks": [],
                "boundaries_identified": [],
                "negative_externalities": [],
                "irreversible_consequences": [],
                "raw_risk": response
            }

    def _extract_percentage(self, text: str, field: str, default: int = 50) -> int:
        value = self.extract_field(text, field, default)
        if isinstance(value, str):
            match = re.search(r'\d+', value)
            value = int(match.group()) if match else default
        return max(0, min(100, value))

    def _extract_risks(self, response: str) -> list:
        risks = []
        try:
            section = re.search(r'RISKS:(.+?)(?:BOUNDARIES:|NEGATIVE EXTERNALITIES:|$)', response, re.DOTALL | re.IGNORECASE)
            if section:
                blocks = re.split(r'\n-\s*Description:', section.group(1))
                for block in blocks[1:]:
                    desc_match = re.search(r'^([^\n]+)', block)
                    sev_match = re.search(r'Severity:\s*(\w+)', block, re.IGNORECASE)
                    prob_match = re.search(r'Probability:\s*(\w+)', block, re.IGNORECASE)
                    affected_match = re.search(r'Affected Parties:\s*([^\n]+)', block)
                    mitig_match = re.search(r'Mitigation:\s*([^\n]+)', block)

                    if desc_match:
                        risk = Risk(
                            description=desc_match.group(1).strip(),
                            severity=sev_match.group(1).lower() if sev_match else "medium",
                            probability=prob_match.group(1).lower() if prob_match else "possible",
                            affected_parties=[a.strip() for a in affected_match.group(1).split(",")] if affected_match else [],
                            mitigation=mitig_match.group(1).strip() if mitig_match else None
                        )
                        risks.append(risk.model_dump())
        except Exception as e:
            self.logger.warning("Failed to extract risks", error=str(e))
        return risks
