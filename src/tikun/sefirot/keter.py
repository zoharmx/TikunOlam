"""
Keter (Crown) - Scope Definition & Validation

First Sefirah: Validates ethical alignment and detects corruption.
Determines if the scenario is suitable for Tikun analysis.
"""

import re
from typing import Dict, Any, Optional
from tikun.sefirot.base import BaseSefirah
from tikun.models.schemas import KeterResult, Corruption


class Keter(BaseSefirah):
    """
    Keter validates the ethical scope and integrity of a scenario.

    Functions:
    - Assess ethical alignment
    - Detect corruption patterns
    - Validate manifestation worthiness
    - Set threshold for pipeline continuation
    """

    def get_prompt(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate Keter evaluation prompt."""
        return f"""You are KETER (כתר - Crown), the first Sefirah in the Tikun Olam ethical reasoning architecture.

Your role is to perform SCOPE DEFINITION and ETHICAL VALIDATION.

SCENARIO TO EVALUATE:
{scenario}

YOUR TASK:
Evaluate this scenario across the following dimensions:

1. ETHICAL ALIGNMENT (0-100%):
   - Does this scenario align with "Tikun Olam" (repairing the world)?
   - Is the intent constructive rather than destructive?
   - Does it consider collective welfare alongside individual rights?

2. CORRUPTION DETECTION:
   Identify any ethical corruptions present:
   - **Deception**: Intent to mislead or hide consequences
   - **Exploitation**: Using others as means without consent
   - **Harm Maximization**: Primary goal is suffering
   - **Inequity**: Deliberately unfair distribution of benefits/burdens
   - **Irreversibility Without Consent**: Forcing permanent changes

   For each corruption found, assess severity: low, medium, high, critical

3. DIMENSIONAL SCORING (-10 to +10):
   - Justice: Fair distribution of benefits and burdens
   - Compassion: Reduces suffering and promotes wellbeing
   - Wisdom: Based on knowledge and careful consideration
   - Sustainability: Long-term viability and non-harm
   - Dignity: Respects autonomy and worth of all affected

4. MANIFESTATION VALIDATION:
   - Is this proposal worthy of manifestation in the world?
   - Would implementation constitute "repair" (tikkun) or harm?

5. THRESHOLD ASSESSMENT:
   - Does alignment meet minimum threshold (60%) to continue pipeline?

REQUIRED OUTPUT FORMAT:
alignment_percentage: [0-100]
corruption_severity: [none/low/medium/high/critical]
manifestation_valid: [yes/no]
threshold_met: [yes/no]

DIMENSION SCORES:
- Justice: [score]
- Compassion: [score]
- Wisdom: [score]
- Sustainability: [score]
- Dignity: [score]

CORRUPTIONS DETECTED:
[For each corruption:]
- Type: [corruption type]
  Severity: [severity level]
  Description: [brief explanation]
  Examples: [specific examples from scenario]

ANALYSIS:
[Your detailed ethical analysis explaining the scores]

Be rigorous. If you detect genuine harm maximization or critical corruption, state it clearly.
"""

    def process(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process scenario through Keter."""
        self.logger.info("Processing Keter (Scope Definition)")

        # Get model from config
        model = self.config.get_model_for_sefirah("keter")

        # Generate prompt
        prompt = self.get_prompt(scenario, previous_results)

        # Call AI (Gemini by default for Keter)
        response = self.call_gemini(prompt, model=model)

        # Parse response
        result = self._parse_response(response)

        if self.verbose:
            self.logger.info(
                f"Keter complete",
                alignment=result['alignment_percentage'],
                corruption=result['corruption_severity'],
                threshold_met=result['threshold_met']
            )

        return result

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse Keter response into structured format."""
        try:
            # Extract alignment percentage
            alignment = self.extract_field(response, "alignment_percentage", 50)
            if isinstance(alignment, str):
                alignment = int(re.search(r'\d+', alignment).group())
            alignment = max(0, min(100, alignment))

            # Extract corruption severity
            severity_match = re.search(
                r'corruption_severity[:\s]+(none|low|medium|high|critical)',
                response,
                re.IGNORECASE
            )
            corruption_severity = severity_match.group(1).lower() if severity_match else "low"

            # Extract manifestation valid
            manifest_match = re.search(
                r'manifestation_valid[:\s]+(yes|no)',
                response,
                re.IGNORECASE
            )
            manifestation_valid = manifest_match.group(1).lower() == "yes" if manifest_match else alignment >= 60

            # Extract threshold met
            threshold_match = re.search(
                r'threshold_met[:\s]+(yes|no)',
                response,
                re.IGNORECASE
            )
            threshold_met = threshold_match.group(1).lower() == "yes" if threshold_match else alignment >= 60

            # Extract dimension scores
            scores = {}
            dimensions = ["Justice", "Compassion", "Wisdom", "Sustainability", "Dignity"]
            for dim in dimensions:
                score = self.extract_field(response, dim, 0)
                if isinstance(score, str):
                    score_match = re.search(r'[+-]?\d+', score)
                    score = int(score_match.group()) if score_match else 0
                scores[dim] = max(-10, min(10, score))

            # Extract corruptions
            corruptions = self._extract_corruptions(response)

            # Create result
            result_data = {
                "alignment_percentage": alignment,
                "corruption_severity": corruption_severity,
                "manifestation_valid": manifestation_valid,
                "threshold_met": threshold_met,
                "scores": scores,
                "corruptions": corruptions,
                "raw_analysis": response
            }

            # Validate with Pydantic
            keter_result = KeterResult(**result_data)

            return keter_result.model_dump()

        except Exception as e:
            self.logger.error(
                "Failed to parse Keter response",
                error=str(e),
                exc_info=True
            )

            # Return safe defaults
            return {
                "alignment_percentage": 50,
                "corruption_severity": "medium",
                "manifestation_valid": False,
                "threshold_met": False,
                "scores": {},
                "corruptions": [],
                "raw_analysis": response
            }

    def _extract_corruptions(self, response: str) -> list:
        """Extract corruption list from response."""
        corruptions = []

        try:
            # Find CORRUPTIONS DETECTED section
            corruption_section = re.search(
                r'CORRUPTIONS DETECTED:(.+?)(?:ANALYSIS:|$)',
                response,
                re.DOTALL | re.IGNORECASE
            )

            if not corruption_section:
                return corruptions

            section_text = corruption_section.group(1)

            # Pattern to match corruption entries
            corruption_pattern = r'- Type:\s*([^\n]+)\s+Severity:\s*([^\n]+)\s+Description:\s*([^\n]+)(?:\s+Examples:\s*([^\n]+))?'

            matches = re.findall(corruption_pattern, section_text, re.IGNORECASE)

            for match in matches:
                corr_type = match[0].strip()
                severity = match[1].strip().lower()

                # Normalize severity
                if severity not in ["low", "medium", "high", "critical"]:
                    severity = "medium"

                description = match[2].strip()
                examples = [e.strip() for e in match[3].split(",")] if len(match) > 3 and match[3] else []

                corruption = Corruption(
                    type=corr_type,
                    severity=severity,
                    description=description,
                    examples=examples
                )

                corruptions.append(corruption.model_dump())

        except Exception as e:
            self.logger.warning(
                "Failed to extract corruptions",
                error=str(e)
            )

        return corruptions
