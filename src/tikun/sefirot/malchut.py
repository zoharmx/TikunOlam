"""
Malchut (Kingdom) - Manifestation & Decision

Tenth and final Sefirah: Makes the final manifestation decision
and provides implementation guidance.
"""

import re
from typing import Dict, Any, Optional
from tikun.sefirot.base import BaseSefirah
from tikun.models.schemas import MalchutResult


class Malchut(BaseSefirah):
    """
    Malchut is the final manifestation point.

    Takes Yesod's integration and converts it into actionable decision.
    This is where abstract reasoning becomes concrete action.
    """

    def get_prompt(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> str:
        context = self.format_previous_results(previous_results, ['yesod'])

        # Extract Yesod recommendation
        yesod_recommendation = "CONDITIONAL_GO"
        if previous_results and 'yesod' in previous_results:
            yesod_data = previous_results['yesod']
            if 'go_no_go_recommendation' in yesod_data:
                yesod_recommendation = yesod_data['go_no_go_recommendation'].get('decision', 'CONDITIONAL_GO')

        return f"""You are MALCHUT (מלכות - Kingdom), the tenth and final Sefirah in the Tikun Olam ethical reasoning architecture.

Your role is MANIFESTATION - converting analysis into action.

YESOD RECOMMENDATION: {yesod_recommendation}

{context}

SCENARIO:
{scenario}

YOUR TASK:
Make the final manifestation decision:

1. MANIFESTATION QUALITY: poor/acceptable/good/excellent
   - How well can this be manifested in reality?

2. FINAL DECISION: GO / NO_GO / CONDITIONAL_GO
   - GO: Proceed with implementation
   - NO_GO: Do not implement
   - CONDITIONAL_GO: Proceed only if conditions met

3. CONFIDENCE: low/medium/high/very_high
   - How confident in this decision?

4. DECISION RATIONALE:
   - Clear explanation of why this decision
   - Reference to Sefirot analysis

5. IMPLEMENTATION STEPS (if GO or CONDITIONAL_GO):
   - Concrete, actionable steps
   - Ordered sequence
   - 5-10 steps

6. CONDITIONS (if CONDITIONAL_GO):
   - Must be met before proceeding
   - Specific and verifiable

7. SUCCESS METRICS:
   - How to measure success
   - Key performance indicators
   - 3-5 metrics

8. MONITORING REQUIREMENTS:
   - What to track during implementation
   - Warning signs
   - Course correction triggers

9. FINAL SUMMARY:
   - Comprehensive final assessment
   - This is the last word

OUTPUT FORMAT:
manifestation_quality: [quality]
decision: [GO/NO_GO/CONDITIONAL_GO]
confidence: [level]

DECISION RATIONALE:
[Detailed explanation drawing on all Sefirot]

IMPLEMENTATION STEPS:
1. [Step 1]
2. [Step 2]
...

CONDITIONS (if CONDITIONAL_GO):
- [Condition 1]
- [Condition 2]
...

SUCCESS METRICS:
- [Metric 1]
- [Metric 2]
...

MONITORING REQUIREMENTS:
- [Requirement 1]
- [Requirement 2]
...

FINAL SUMMARY:
[Your conclusive assessment - this is the definitive word on whether and how to manifest this proposal]
"""

    def process(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process final manifestation decision."""
        self.logger.info("Processing Malchut (Manifestation)")

        # Malchut uses Claude for final decision
        model = self.config.get_model_for_sefirah("malchut")
        prompt = self.get_prompt(scenario, previous_results)

        response = self.call_claude(prompt, model=model)

        result = self._parse_response(response)

        if self.verbose:
            self.logger.info(
                f"Malchut complete - FINAL DECISION",
                decision=result['decision'],
                confidence=result['confidence'],
                quality=result['manifestation_quality']
            )

        return result

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse Malchut response."""
        try:
            # Extract quality
            quality_match = re.search(r'manifestation_quality[:\s]+(poor|acceptable|good|excellent)', response, re.IGNORECASE)
            quality = quality_match.group(1).lower() if quality_match else "acceptable"

            # Extract decision
            decision_match = re.search(r'decision[:\s]+(GO|NO_GO|CONDITIONAL_GO)', response, re.IGNORECASE)
            decision = decision_match.group(1).upper().replace(' ', '_') if decision_match else "CONDITIONAL_GO"

            # Extract confidence
            conf_match = re.search(r'confidence[:\s]+(low|medium|high|very_high)', response, re.IGNORECASE)
            confidence = conf_match.group(1).lower() if conf_match else "medium"

            # Extract rationale
            rat_match = re.search(r'DECISION RATIONALE:(.+?)(?:IMPLEMENTATION STEPS:|CONDITIONS:|SUCCESS METRICS:|$)', response, re.DOTALL | re.IGNORECASE)
            rationale = rat_match.group(1).strip() if rat_match else ""

            # Extract implementation steps
            steps = []
            steps_match = re.search(r'IMPLEMENTATION STEPS:(.+?)(?:CONDITIONS:|SUCCESS METRICS:|MONITORING REQUIREMENTS:|$)', response, re.DOTALL | re.IGNORECASE)
            if steps_match:
                steps_text = steps_match.group(1)
                # Find numbered steps
                steps = [s.strip() for s in re.findall(r'\d+\.\s*([^\n]+)', steps_text)]

            # Extract conditions
            conditions = []
            cond_match = re.search(r'CONDITIONS.*?:(.+?)(?:SUCCESS METRICS:|MONITORING REQUIREMENTS:|FINAL SUMMARY:|$)', response, re.DOTALL | re.IGNORECASE)
            if cond_match:
                conditions = [c.strip() for c in re.findall(r'-\s*([^\n]+)', cond_match.group(1))]

            # Extract success metrics
            metrics = []
            metrics_match = re.search(r'SUCCESS METRICS:(.+?)(?:MONITORING REQUIREMENTS:|FINAL SUMMARY:|$)', response, re.DOTALL | re.IGNORECASE)
            if metrics_match:
                metrics = [m.strip() for m in re.findall(r'-\s*([^\n]+)', metrics_match.group(1))]

            # Extract monitoring requirements
            monitoring = []
            mon_match = re.search(r'MONITORING REQUIREMENTS:(.+?)(?:FINAL SUMMARY:|$)', response, re.DOTALL | re.IGNORECASE)
            if mon_match:
                monitoring = [m.strip() for m in re.findall(r'-\s*([^\n]+)', mon_match.group(1))]

            # Extract final summary
            summary_match = re.search(r'FINAL SUMMARY:(.+?)$', response, re.DOTALL | re.IGNORECASE)
            summary = summary_match.group(1).strip() if summary_match else ""

            result_data = {
                "manifestation_quality": quality,
                "decision": decision,
                "confidence": confidence,
                "decision_rationale": rationale,
                "implementation_steps": steps,
                "conditions": conditions,
                "success_metrics": metrics,
                "monitoring_requirements": monitoring,
                "final_summary": summary
            }

            return MalchutResult(**result_data).model_dump()

        except Exception as e:
            self.logger.error("Failed to parse Malchut response", error=str(e), exc_info=True)
            return {
                "manifestation_quality": "acceptable",
                "decision": "CONDITIONAL_GO",
                "confidence": "medium",
                "decision_rationale": "Analysis incomplete",
                "implementation_steps": [],
                "conditions": ["Complete full analysis before proceeding"],
                "success_metrics": [],
                "monitoring_requirements": [],
                "final_summary": response
            }
