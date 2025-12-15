"""
Chochmah (Wisdom) - Wisdom Analysis

Second Sefirah: Analyzes wisdom, patterns, and historical precedents.
Provides deep insight while maintaining epistemic humility.
"""

import re
import json
from typing import Dict, Any, Optional, List
from tikun.sefirot.base import BaseSefirah
from tikun.models.schemas import ChochmahResult, Precedent


class Chochmah(BaseSefirah):
    """
    Chochmah provides wisdom analysis and pattern recognition.

    Functions:
    - Identify patterns and precedents
    - Assess confidence with epistemic humility
    - Extract hidden insights
    - Detect paradoxes
    """

    def get_prompt(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate Chochmah analysis prompt."""
        context = self.format_previous_results(previous_results, ['keter'])

        return f"""You are CHOCHMAH (חכמה - Wisdom), the second Sefirah in the Tikun Olam ethical reasoning architecture.

Your role is to provide WISDOM ANALYSIS through pattern recognition and historical insight.

{context}

SCENARIO:
{scenario}

YOUR TASK:
Analyze this scenario with wisdom and insight:

1. CONFIDENCE ASSESSMENT (0-100%):
   - How confident are you in analyzing this scenario?
   - Consider data availability, complexity, and precedent clarity

2. EPISTEMIC HUMILITY (0-100%):
   - What don't we know?
   - What assumptions might be wrong?
   - What uncertainties remain?
   Higher score = more uncertainty/humility

3. INSIGHT DEPTH (0-100%):
   - How deep are the insights available?
   - Quality of understanding vs surface analysis

4. PATTERNS IDENTIFIED:
   - What recurring patterns appear in this scenario?
   - Historical, psychological, economic, social patterns
   - List at least 3-5 significant patterns

5. HISTORICAL PRECEDENTS:
   For each precedent:
   - Name and year
   - Outcome (success/failure/mixed)
   - Relevance to current scenario
   - Key lessons learned

6. HIDDEN INSIGHTS:
   - What non-obvious insights emerge?
   - Second-order effects
   - Counterintuitive implications

7. PARADOXES IDENTIFIED:
   - What contradictions or tensions exist?
   - Where do competing values collide?

REQUIRED OUTPUT FORMAT:
confidence_level: [0-100]
epistemic_humility_ratio: [0-100]
insight_depth_score: [0-100]

PATTERNS IDENTIFIED:
- [Pattern 1]
- [Pattern 2]
- [Pattern 3]
...

HISTORICAL PRECEDENTS:
[For each precedent:]
- Name: [precedent name]
  Year: [year or range]
  Outcome: [outcome description]
  Relevance: [why it matters]
  Lessons:
    - [Lesson 1]
    - [Lesson 2]

HIDDEN INSIGHTS:
- [Insight 1]
- [Insight 2]
...

PARADOXES:
- [Paradox 1]
- [Paradox 2]
...

WISDOM ANALYSIS:
[Your deep analytical synthesis]

Emphasize quality of insight over quantity. Acknowledge what you don't know.
"""

    def process(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process scenario through Chochmah."""
        self.logger.info("Processing Chochmah (Wisdom Analysis)")

        model = self.config.get_model_for_sefirah("chochmah")
        prompt = self.get_prompt(scenario, previous_results)

        # Use Claude for deeper reasoning
        response = self.call_claude(prompt, model=model)

        result = self._parse_response(response)

        if self.verbose:
            self.logger.info(
                f"Chochmah complete",
                confidence=result['confidence_level'],
                humility=result['epistemic_humility_ratio'],
                precedents=len(result['precedents'])
            )

        return result

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse Chochmah response."""
        try:
            # Extract metrics
            confidence = self._extract_percentage(response, "confidence_level", 70)
            humility = self._extract_percentage(response, "epistemic_humility", 50)
            depth = self._extract_percentage(response, "insight_depth", 70)

            # Extract patterns
            patterns = self.extract_list(response, marker="-", section="PATTERNS IDENTIFIED")

            # Extract precedents
            precedents = self._extract_precedents(response)

            # Extract insights
            insights = self.extract_list(response, marker="-", section="HIDDEN INSIGHTS")

            # Extract paradoxes
            paradoxes = self.extract_list(response, marker="-", section="PARADOXES")

            result_data = {
                "confidence_level": confidence,
                "epistemic_humility_ratio": humility,
                "insight_depth_score": depth,
                "patterns_identified": patterns,
                "precedents": precedents,
                "hidden_insights": insights,
                "paradoxes_identified": paradoxes,
                "raw_wisdom": response
            }

            chochmah_result = ChochmahResult(**result_data)
            return chochmah_result.model_dump()

        except Exception as e:
            self.logger.error("Failed to parse Chochmah response", error=str(e), exc_info=True)
            return {
                "confidence_level": 50,
                "epistemic_humility_ratio": 70,
                "insight_depth_score": 50,
                "patterns_identified": [],
                "precedents": [],
                "hidden_insights": [],
                "paradoxes_identified": [],
                "raw_wisdom": response
            }

    def _extract_percentage(self, text: str, field: str, default: int = 50) -> int:
        """Extract percentage value."""
        value = self.extract_field(text, field, default)
        if isinstance(value, str):
            match = re.search(r'\d+', value)
            value = int(match.group()) if match else default
        return max(0, min(100, value))

    def _extract_precedents(self, response: str) -> List[Dict[str, Any]]:
        """Extract historical precedents."""
        precedents = []

        try:
            section_match = re.search(
                r'HISTORICAL PRECEDENTS:(.+?)(?:HIDDEN INSIGHTS:|PARADOXES:|WISDOM ANALYSIS:|$)',
                response,
                re.DOTALL | re.IGNORECASE
            )

            if not section_match:
                return precedents

            section = section_match.group(1)

            # Split by precedent markers
            precedent_blocks = re.split(r'\n-\s*Name:', section)

            for block in precedent_blocks[1:]:  # Skip first empty split
                try:
                    name_match = re.search(r'^([^\n]+)', block)
                    year_match = re.search(r'Year:\s*([^\n]+)', block)
                    outcome_match = re.search(r'Outcome:\s*([^\n]+)', block)
                    relevance_match = re.search(r'Relevance:\s*([^\n]+)', block)
                    lessons_match = re.search(r'Lessons:(.+?)(?:\n-\s*Name:|$)', block, re.DOTALL)

                    if name_match:
                        name = name_match.group(1).strip()
                        year_str = year_match.group(1).strip() if year_match else None
                        year = None

                        if year_str:
                            year_num_match = re.search(r'\d{4}', year_str)
                            year = int(year_num_match.group()) if year_num_match else None

                        outcome = outcome_match.group(1).strip() if outcome_match else ""
                        relevance = relevance_match.group(1).strip() if relevance_match else ""

                        lessons = []
                        if lessons_match:
                            lessons_text = lessons_match.group(1)
                            lessons = [l.strip() for l in re.findall(r'-\s*([^\n]+)', lessons_text)]

                        precedent = Precedent(
                            name=name,
                            year=year,
                            outcome=outcome,
                            relevance=relevance,
                            lessons=lessons
                        )

                        precedents.append(precedent.model_dump())

                except Exception as e:
                    self.logger.warning(f"Failed to parse precedent block", error=str(e))
                    continue

        except Exception as e:
            self.logger.warning("Failed to extract precedents", error=str(e))

        return precedents
