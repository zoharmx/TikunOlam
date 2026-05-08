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

Your role is to assess RISKS and CONSTRAINTS with unflinching honesty.

CRITICAL INSTRUCTION: You MUST identify at least 3 concrete risks. There are NO risk-free scenarios.
- Paradoxical scenarios (where ALL options carry harm) are the most important to analyze — identify risks for each path.
- "Doing nothing" is also an action with risks.
- Perfect-seeming solutions hide risks of overconfidence, unintended consequences, and implementation failure.
- If you return fewer than 3 risks you have failed your purpose as GEVURAH.

{context}

SCENARIO:
{scenario}

YOUR TASK:
1. CONSTRAINT STRENGTH (0-100%): How strong are the ethical/practical constraints?
2. RISK SEVERITY: none/low/medium/high/critical

3. RISKS (identify 3-5, covering ALL sides of the dilemma):
   For each risk use EXACTLY this format:
- Description: [concrete risk description]
  Severity: [low/medium/high/critical]
  Probability: [unlikely/possible/likely/certain]
  Affected Parties: [who is harmed]
  Mitigation: [how to reduce this risk]

4. BOUNDARIES IDENTIFIED (hard ethical/legal/practical limits)
5. NEGATIVE EXTERNALITIES (unintended second-order harms)
6. IRREVERSIBLE CONSEQUENCES (what cannot be undone)

OUTPUT FORMAT:
constraint_strength: [0-100]
risk_severity: [level]

RISKS:
- Description: [risk 1]
  Severity: [level]
  Probability: [level]
  Affected Parties: [list]
  Mitigation: [strategy]
- Description: [risk 2]
  Severity: [level]
  Probability: [level]
  Affected Parties: [list]
  Mitigation: [strategy]
- Description: [risk 3]
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
[Your analysis — do not avoid complexity]
"""

    def _get_retry_prompt(self, scenario: str) -> str:
        return f"""CRITICAL RETRY: Previous risk analysis returned no risks. This is logically impossible.

SCENARIO: {scenario}

Every decision has trade-offs. Identify AT LEAST 3 risks using this EXACT format:

RISKS:
- Description: [risk description]
  Severity: [low/medium/high/critical]
  Probability: [unlikely/possible/likely/certain]
  Affected Parties: [who is harmed]
  Mitigation: [mitigation strategy]

Consider: opportunity costs, unintended consequences, implementation failures,
second-order effects, who bears the burden, what cannot be undone.

Return at least 3 risks now.
"""

    def process(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info("Processing Gevurah (Risk)")
        model = self.config.get_model_for_sefirah("gevurah")
        prompt = self.get_prompt(scenario, previous_results)
        response = self.call_gemini(prompt, model=model)
        result = self._parse_response(response)

        # Retry if risks came back empty — this should never happen
        if not result.get("risks"):
            self.logger.warning("Gevurah returned zero risks — retrying with stronger prompt", scenario=scenario[:100])
            retry_response = self.call_gemini(self._get_retry_prompt(scenario), model=model)
            result = self._parse_response(retry_response, is_retry=True)

        if self.verbose:
            self.logger.info("Gevurah complete", risks=len(result.get("risks", [])), severity=result.get("risk_severity"))

        return result

    def _parse_response(self, response: str, is_retry: bool = False) -> Dict[str, Any]:
        try:
            constraint = self._extract_percentage(response, "constraint_strength", 50)

            severity_match = re.search(r'risk_severity[:\s]+(none|low|medium|high|critical)', response, re.IGNORECASE)
            severity = severity_match.group(1).lower() if severity_match else "medium"

            risks = self._extract_risks(response)
            boundaries = self.extract_list(response, section="BOUNDARIES")
            neg_extern = self.extract_list(response, section="NEGATIVE EXTERNALITIES")
            irreversible = self.extract_list(response, section="IRREVERSIBLE CONSEQUENCES")

            # Fallback guaranteed — insert default risk only on retry to avoid masking real parse errors
            if not risks and is_retry:
                self.logger.error("Gevurah FORCED default risk after retry — LLM output unparseable")
                risks = [Risk(
                    description="Risk assessment incomplete: the scenario's complexity prevented standard risk extraction. Further analysis required.",
                    severity="high",
                    probability="likely",
                    affected_parties=["All stakeholders"],
                    mitigation="Conduct targeted risk workshops with domain experts"
                ).model_dump()]

            result_data = {
                "constraint_strength": constraint,
                "risk_severity": severity if risks else "high",
                "risks": risks,
                "boundaries_identified": boundaries,
                "negative_externalities": neg_extern,
                "irreversible_consequences": irreversible,
                "raw_risk": response
            }

            result = GevurahResult(**result_data).model_dump()
            # Compatibility aliases for test scripts
            sev_map = {"none": 0, "low": 25, "medium": 50, "high": 75, "critical": 95}
            result["severity_score"] = sev_map.get(result.get("risk_severity", "medium"), 50)
            result["red_lines"] = result.get("boundaries_identified", [])
            return result

        except Exception as e:
            self.logger.error("Failed to parse Gevurah response", error=str(e))
            return {
                "constraint_strength": 50,
                "risk_severity": "high",
                "risks": [],   # left empty so process() retry logic triggers
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
        """
        Extract risks using two strategies:
        1. Primary: structured blocks with 'Description:' / 'Severity:' fields
        2. Secondary: plain bullet lines within the RISKS section (handles divergent LLM output)
        """
        risks = []
        try:
            section_match = re.search(
                r'RISKS:(.*?)(?=\nBOUNDARIES:|\nNEGATIVE EXTERNALITIES:|\nIRREVERSIBLE|\nRISK ANALYSIS:|$)',
                response, re.DOTALL | re.IGNORECASE
            )
            if not section_match:
                return risks
            section = section_match.group(1)

            # --- Strategy 1: structured Description:/Severity: blocks ---
            blocks = re.split(r'\n-\s*Description:', section)
            for block in blocks[1:]:
                desc_match = re.search(r'^([^\n]+)', block)
                sev_match = re.search(r'Severity:\s*(low|medium|high|critical)', block, re.IGNORECASE)
                prob_match = re.search(r'Probability:\s*(unlikely|possible|likely|certain)', block, re.IGNORECASE)
                affected_match = re.search(r'Affected Parties:\s*([^\n]+)', block, re.IGNORECASE)
                mitig_match = re.search(r'Mitigation:\s*([^\n]+)', block, re.IGNORECASE)

                if desc_match:
                    risk = Risk(
                        description=desc_match.group(1).strip(),
                        severity=sev_match.group(1).lower() if sev_match else "medium",
                        probability=prob_match.group(1).lower() if prob_match else "possible",
                        affected_parties=[a.strip() for a in affected_match.group(1).split(",")] if affected_match else [],
                        mitigation=mitig_match.group(1).strip() if mitig_match else None
                    )
                    risks.append(risk.model_dump())

            # --- Strategy 2: plain bullet lines (fallback when LLM ignores structured format) ---
            if not risks:
                bullet_lines = re.findall(r'^\s*[-*•]\s*(.{15,})', section, re.MULTILINE)
                for line in bullet_lines[:6]:
                    line = line.strip()
                    # Infer severity from keywords in the line
                    if any(w in line.lower() for w in ('death', 'extinction', 'catastroph', 'critical', 'fatal', 'collapse')):
                        sev = "critical"
                    elif any(w in line.lower() for w in ('harm', 'serious', 'major', 'significant', 'severe')):
                        sev = "high"
                    else:
                        sev = "medium"
                    risk = Risk(
                        description=line,
                        severity=sev,
                        probability="possible",
                        affected_parties=[],
                        mitigation=None
                    )
                    risks.append(risk.model_dump())

        except Exception as e:
            self.logger.warning("Failed to extract risks", error=str(e))
        return risks
