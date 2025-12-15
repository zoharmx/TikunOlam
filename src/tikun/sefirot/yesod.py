"""
Yesod (Foundation) - Integration & Coherence

Ninth Sefirah: Integrates all previous Sefirot and checks coherence.
Makes GO/NO-GO recommendation.
"""

import re
from typing import Dict, Any, Optional
from tikun.sefirot.base import BaseSefirah
from tikun.models.schemas import YesodResult, Gap


class Yesod(BaseSefirah):
    """
    Yesod integrates all Sefirot and validates coherence.

    This is the critical integration point before final manifestation.
    """

    def get_prompt(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> str:
        context = self.format_previous_results(previous_results)

        return f"""You are YESOD (יסוד - Foundation), the ninth Sefirah in the Tikun Olam ethical reasoning architecture.

Your role is INTEGRATION and COHERENCE VALIDATION.

You have received results from all previous Sefirot (Keter through Hod).

{context}

SCENARIO:
{scenario}

YOUR TASK:
Integrate and validate coherence across all Sefirot:

1. READINESS SCORE (0-100%): How ready for manifestation?
2. INTEGRATION QUALITY: poor/acceptable/good/excellent
3. FOUNDATION STRENGTH: weak/moderate/strong/robust
4. YESOD QUALITY: poor/acceptable/good/exceptional

5. COHERENCE ANALYSIS:
   Check alignment between Sefirot:
   - Keter alignment vs final synthesis
   - Chochmah wisdom vs Netzach strategy
   - Binah understanding vs Hod communication
   - Chesed opportunity vs Gevurah risk (balance)
   - Overall coherence status: aligned/partial/conflicting

6. GAPS IDENTIFIED:
   What's missing or inconsistent?
   For each gap:
   - Gap description
   - Severity: minor/moderate/significant/critical
   - Which Sefirah
   - Recommendation to address

7. GO/NO-GO RECOMMENDATION:
   - Decision: GO / NO_GO / CONDITIONAL_GO
   - Confidence: low/medium/high/very_high
   - Rationale: why this recommendation
   - Conditions (if CONDITIONAL_GO): what must be met

8. INTEGRATION SUMMARY:
   Overall assessment of the analysis

OUTPUT FORMAT:
readiness_score: [0-100]
integration_quality: [quality]
foundation_strength: [strength]
yesod_quality: [quality]

SEFIROT ALIGNMENT:
- Keter-Synthesis: [aligned/partial/conflicting] - [explanation]
- Wisdom-Strategy: [status] - [explanation]
- Understanding-Communication: [status] - [explanation]
- Opportunity-Risk Balance: [status] - [explanation]

OVERALL COHERENCE:
Status: [aligned/partial/conflicting]
Details: [explanation]

GAPS IDENTIFIED:
- Gap: [description]
  Severity: [level]
  Sefirah: [sefirah name]
  Recommendation: [how to address]

GO/NO-GO RECOMMENDATION:
Decision: [GO/NO_GO/CONDITIONAL_GO]
Confidence: [level]
Rationale: [explanation]
Conditions (if applicable):
- [Condition 1]
- [Condition 2]

INTEGRATION SUMMARY:
[Your comprehensive summary]
"""

    def process(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process Yesod integration."""
        self.logger.info("Processing Yesod (Integration)")

        # Yesod uses Claude for sophisticated integration
        model = self.config.get_model_for_sefirah("yesod")
        prompt = self.get_prompt(scenario, previous_results)

        response = self.call_claude(prompt, model=model)

        result = self._parse_response(response)

        if self.verbose:
            self.logger.info(
                f"Yesod complete",
                readiness=result['readiness_score'],
                decision=result['go_no_go_recommendation'].get('decision', 'UNKNOWN'),
                gaps=len(result['gaps_identified'])
            )

        return result

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse Yesod response."""
        try:
            # Extract metrics
            readiness = self._extract_percentage(response, "readiness_score", 60)

            integration_match = re.search(r'integration_quality[:\s]+(poor|acceptable|good|excellent)', response, re.IGNORECASE)
            integration = integration_match.group(1).lower() if integration_match else "acceptable"

            foundation_match = re.search(r'foundation_strength[:\s]+(weak|moderate|strong|robust)', response, re.IGNORECASE)
            foundation = foundation_match.group(1).lower() if foundation_match else "moderate"

            yesod_match = re.search(r'yesod_quality[:\s]+(poor|acceptable|good|exceptional)', response, re.IGNORECASE)
            yesod_quality = yesod_match.group(1).lower() if yesod_match else "acceptable"

            # Extract coherence analysis
            sefirot_alignment = self._extract_alignment(response)
            overall_coherence = self._extract_overall_coherence(response)

            # Extract gaps
            gaps = self._extract_gaps(response)

            # Extract GO/NO-GO recommendation
            recommendation = self._extract_recommendation(response)

            # Extract integration summary
            summary_match = re.search(r'INTEGRATION SUMMARY:(.+?)$', response, re.DOTALL | re.IGNORECASE)
            summary = summary_match.group(1).strip() if summary_match else ""

            result_data = {
                "readiness_score": readiness,
                "integration_quality": integration,
                "foundation_strength": foundation,
                "yesod_quality": yesod_quality,
                "sefirot_alignment": sefirot_alignment,
                "overall_coherence": overall_coherence,
                "gaps_identified": gaps,
                "go_no_go_recommendation": recommendation,
                "integration_summary": summary
            }

            return YesodResult(**result_data).model_dump()

        except Exception as e:
            self.logger.error("Failed to parse Yesod response", error=str(e), exc_info=True)
            return {
                "readiness_score": 50,
                "integration_quality": "acceptable",
                "foundation_strength": "moderate",
                "yesod_quality": "acceptable",
                "sefirot_alignment": {},
                "overall_coherence": {"status": "partial", "details": "Analysis incomplete"},
                "gaps_identified": [],
                "go_no_go_recommendation": {
                    "decision": "CONDITIONAL_GO",
                    "confidence": "medium",
                    "rationale": "Analysis incomplete, proceeding with caution",
                    "conditions": ["Complete missing analysis"]
                },
                "integration_summary": response
            }

    def _extract_percentage(self, text: str, field: str, default: int = 50) -> int:
        value = self.extract_field(text, field, default)
        if isinstance(value, str):
            match = re.search(r'\d+', value)
            value = int(match.group()) if match else default
        return max(0, min(100, value))

    def _extract_alignment(self, response: str) -> dict:
        """Extract sefirot alignment analysis."""
        alignment = {}
        try:
            section = re.search(r'SEFIROT ALIGNMENT:(.+?)(?:OVERALL COHERENCE:|GAPS IDENTIFIED:|$)', response, re.DOTALL | re.IGNORECASE)
            if section:
                lines = section.group(1).split('\n')
                for line in lines:
                    if '-' in line and ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            key = parts[0].strip().replace('- ', '')
                            value = parts[1].strip()
                            alignment[key] = value
        except Exception as e:
            self.logger.warning("Failed to extract alignment", error=str(e))
        return alignment

    def _extract_overall_coherence(self, response: str) -> dict:
        """Extract overall coherence assessment."""
        try:
            section = re.search(r'OVERALL COHERENCE:(.+?)(?:GAPS IDENTIFIED:|GO/NO-GO RECOMMENDATION:|$)', response, re.DOTALL | re.IGNORECASE)
            if section:
                text = section.group(1)
                status_match = re.search(r'Status:\s*(\w+)', text, re.IGNORECASE)
                details_match = re.search(r'Details:\s*([^\n]+)', text, re.IGNORECASE)

                return {
                    "status": status_match.group(1).lower() if status_match else "partial",
                    "details": details_match.group(1).strip() if details_match else ""
                }
        except Exception as e:
            self.logger.warning("Failed to extract coherence", error=str(e))

        return {"status": "partial", "details": ""}

    def _extract_gaps(self, response: str) -> list:
        """Extract identified gaps."""
        gaps = []
        try:
            section = re.search(r'GAPS IDENTIFIED:(.+?)(?:GO/NO-GO RECOMMENDATION:|INTEGRATION SUMMARY:|$)', response, re.DOTALL | re.IGNORECASE)
            if section:
                blocks = re.split(r'\n-\s*Gap:', section.group(1))
                for block in blocks[1:]:
                    gap_match = re.search(r'^([^\n]+)', block)
                    sev_match = re.search(r'Severity:\s*(\w+)', block, re.IGNORECASE)
                    sef_match = re.search(r'Sefirah:\s*([^\n]+)', block, re.IGNORECASE)
                    rec_match = re.search(r'Recommendation:\s*([^\n]+)', block, re.IGNORECASE)

                    if gap_match:
                        gap = Gap(
                            gap=gap_match.group(1).strip(),
                            severity=sev_match.group(1).lower() if sev_match else "moderate",
                            sefirah=sef_match.group(1).strip() if sef_match else "unknown",
                            recommendation=rec_match.group(1).strip() if rec_match else ""
                        )
                        gaps.append(gap.model_dump())
        except Exception as e:
            self.logger.warning("Failed to extract gaps", error=str(e))
        return gaps

    def _extract_recommendation(self, response: str) -> dict:
        """Extract GO/NO-GO recommendation."""
        try:
            section = re.search(r'GO/NO-GO RECOMMENDATION:(.+?)(?:INTEGRATION SUMMARY:|$)', response, re.DOTALL | re.IGNORECASE)
            if section:
                text = section.group(1)

                decision_match = re.search(r'Decision:\s*(GO|NO_GO|CONDITIONAL_GO)', text, re.IGNORECASE)
                decision = decision_match.group(1).upper().replace(' ', '_') if decision_match else "CONDITIONAL_GO"

                conf_match = re.search(r'Confidence:\s*(\w+)', text, re.IGNORECASE)
                confidence = conf_match.group(1).lower() if conf_match else "medium"

                rat_match = re.search(r'Rationale:\s*([^\n]+)', text, re.IGNORECASE)
                rationale = rat_match.group(1).strip() if rat_match else ""

                # Extract conditions
                conditions = []
                cond_match = re.search(r'Conditions.*?:(.+?)(?:INTEGRATION SUMMARY:|$)', text, re.DOTALL | re.IGNORECASE)
                if cond_match:
                    conditions = [c.strip() for c in re.findall(r'-\s*([^\n]+)', cond_match.group(1))]

                return {
                    "decision": decision,
                    "confidence": confidence,
                    "rationale": rationale,
                    "conditions": conditions
                }
        except Exception as e:
            self.logger.warning("Failed to extract recommendation", error=str(e))

        return {
            "decision": "CONDITIONAL_GO",
            "confidence": "medium",
            "rationale": "Default recommendation",
            "conditions": []
        }
