"""
Netzach (Victory) - Strategy Formation

Seventh Sefirah: Develops strategic approaches for implementation.
"""

import re
from typing import Dict, Any, Optional
from tikun.sefirot.base import BaseSefirah
from tikun.models.schemas import NetzachResult, Strategy


class Netzach(BaseSefirah):
    """Netzach forms implementation strategies."""

    def get_prompt(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> str:
        context = self.format_previous_results(previous_results, ['tiferet'])

        return f"""You are NETZACH (נצח - Victory), the seventh Sefirah in the Tikun Olam ethical reasoning architecture.

Your role is STRATEGY FORMATION.

{context}

SCENARIO:
{scenario}

YOUR TASK:
Develop strategic approaches:

1. PERSISTENCE SCORE (0-100%): How sustainable is implementation?
2. STRATEGIC CLARITY: unclear/developing/clear/compelling

3. STRATEGIES (list 3-5):
   For each:
   - Name
   - Description
   - Priority: low/medium/high/critical
   - Timeline: when to implement
   - Resources Required

4. CRITICAL SUCCESS FACTORS (what must go right)
5. POTENTIAL OBSTACLES (what could block success)
6. LONG-TERM VISION (ultimate goal)

OUTPUT FORMAT:
persistence_score: [0-100]
strategic_clarity: [level]

STRATEGIES:
- Name: [strategy name]
  Description: [description]
  Priority: [level]
  Timeline: [timeframe]
  Resources: [resource 1], [resource 2]

CRITICAL SUCCESS FACTORS:
- [factor 1]

POTENTIAL OBSTACLES:
- [obstacle 1]

LONG-TERM VISION:
[Vision statement]

STRATEGY ANALYSIS:
[Analysis]
"""

    def process(self, scenario: str, previous_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info("Processing Netzach (Strategy)")
        model = self.config.get_model_for_sefirah("netzach")
        prompt = self.get_prompt(scenario, previous_results)
        response = self.call_gemini(prompt, model=model)
        return self._parse_response(response)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            persistence = self._extract_percentage(response, "persistence_score", 60)

            clarity_match = re.search(r'strategic_clarity[:\s]+(unclear|developing|clear|compelling)', response, re.IGNORECASE)
            clarity = clarity_match.group(1).lower() if clarity_match else "developing"

            strategies = self._extract_strategies(response)
            success_factors = self.extract_list(response, section="CRITICAL SUCCESS FACTORS")
            obstacles = self.extract_list(response, section="POTENTIAL OBSTACLES")

            vision_match = re.search(r'LONG-TERM VISION:(.+?)(?:STRATEGY ANALYSIS:|$)', response, re.DOTALL | re.IGNORECASE)
            vision = vision_match.group(1).strip() if vision_match else ""

            result_data = {
                "persistence_score": persistence,
                "strategic_clarity": clarity,
                "strategies": strategies,
                "critical_success_factors": success_factors,
                "potential_obstacles": obstacles,
                "long_term_vision": vision,
                "raw_strategy": response
            }

            return NetzachResult(**result_data).model_dump()

        except Exception as e:
            self.logger.error("Failed to parse Netzach response", error=str(e))
            return {
                "persistence_score": 50,
                "strategic_clarity": "developing",
                "strategies": [],
                "critical_success_factors": [],
                "potential_obstacles": [],
                "long_term_vision": "",
                "raw_strategy": response
            }

    def _extract_percentage(self, text: str, field: str, default: int = 50) -> int:
        value = self.extract_field(text, field, default)
        if isinstance(value, str):
            match = re.search(r'\d+', value)
            value = int(match.group()) if match else default
        return max(0, min(100, value))

    def _extract_strategies(self, response: str) -> list:
        strategies = []
        try:
            section = re.search(r'STRATEGIES:(.+?)(?:CRITICAL SUCCESS FACTORS:|$)', response, re.DOTALL | re.IGNORECASE)
            if section:
                blocks = re.split(r'\n-\s*Name:', section.group(1))
                for block in blocks[1:]:
                    name_match = re.search(r'^([^\n]+)', block)
                    desc_match = re.search(r'Description:\s*([^\n]+)', block)
                    priority_match = re.search(r'Priority:\s*(\w+)', block, re.IGNORECASE)
                    timeline_match = re.search(r'Timeline:\s*([^\n]+)', block)
                    resources_match = re.search(r'Resources:\s*([^\n]+)', block)

                    if name_match:
                        strategy = Strategy(
                            name=name_match.group(1).strip(),
                            description=desc_match.group(1).strip() if desc_match else "",
                            priority=priority_match.group(1).lower() if priority_match else "medium",
                            timeline=timeline_match.group(1).strip() if timeline_match else None,
                            resources_required=[r.strip() for r in resources_match.group(1).split(",")] if resources_match else []
                        )
                        strategies.append(strategy.model_dump())
        except Exception as e:
            self.logger.warning("Failed to extract strategies", error=str(e))
        return strategies
