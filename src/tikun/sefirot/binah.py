"""
Binah (Understanding) - Value Bias Detection / BinahSigma

Third Sefirah: Deep contextual understanding and multi-civilizational bias detection.
BinahSigma mode compares Western vs Eastern AI perspectives to expose blind spots.
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from tikun.sefirot.base import BaseSefirah
from tikun.models.schemas import BinahResult, BinahSigmaAnalysis
from tikun.utils.validation import detect_geopolitical_content


class Binah(BaseSefirah):
    """
    Binah provides deep contextual understanding and bias detection.

    Modes:
    - Simple: Standard contextual analysis
    - Sigma: Multi-civilizational bias detection (Western vs Eastern AI)

    BinahSigma is activated for geopolitical scenarios.
    """

    def get_prompt(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate Binah analysis prompt.

        Note: Binah uses different prompts for simple vs sigma mode.
        This method returns the simple mode prompt as default.
        """
        return self._get_simple_prompt(scenario, previous_results)

    def process(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process scenario through Binah."""
        self.logger.info("Processing Binah (Understanding)")

        # Detect if scenario is geopolitical
        is_geopolitical, geo_score, keywords = detect_geopolitical_content(scenario)

        if is_geopolitical and geo_score >= self.config.binah_sigma_threshold:
            self.logger.info(
                f"BinahSigma activated",
                score=geo_score,
                keywords_matched=len(keywords)
            )
            return self._process_sigma(scenario, previous_results)
        else:
            self.logger.info("BinahSigma not activated, using simple mode")
            return self._process_simple(scenario, previous_results)

    def _process_simple(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Simple contextual analysis mode."""
        model = self.config.get_model_for_sefirah("binah_west")
        prompt = self._get_simple_prompt(scenario, previous_results)

        response = self.call_gemini(prompt, model=model)
        result = self._parse_simple_response(response)

        if self.verbose:
            self.logger.info(
                f"Binah (simple) complete",
                depth=result['contextual_depth_score']
            )

        return result

    def _process_sigma(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """BinahSigma multi-civilizational analysis."""
        try:
            # Get both perspectives in parallel
            west_prompt = self._get_sigma_prompt(scenario, previous_results, "Western")
            east_prompt = self._get_sigma_prompt(scenario, previous_results, "Eastern")

            west_model = self.config.binah_west_model
            east_model = self.config.binah_east_model

            # Western perspective (Gemini)
            self.logger.debug("Analyzing Western perspective")
            west_response = self.call_gemini(west_prompt, model=west_model)

            # Eastern perspective (DeepSeek)
            self.logger.debug("Analyzing Eastern perspective")
            east_response = self.call_deepseek(east_prompt, model=east_model)

            # Synthesize results
            result = self._synthesize_sigma(west_response, east_response, scenario)

            if self.verbose:
                self.logger.info(
                    f"BinahSigma complete",
                    bias_delta=result.get('bias_delta', 0),
                    divergence=result.get('divergence_level', 'unknown'),
                    blind_spots=result.get('blind_spots_detected', 0)
                )

            return result

        except Exception as e:
            self.logger.error(
                "BinahSigma failed, falling back to simple mode",
                error=str(e),
                exc_info=True
            )
            return self._process_simple(scenario, previous_results)

    def _get_simple_prompt(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate simple mode prompt."""
        context = self.format_previous_results(previous_results, ['keter', 'chochmah'])

        return f"""You are BINAH (בינה - Understanding), the third Sefirah in the Tikun Olam ethical reasoning architecture.

Your role is to provide DEEP CONTEXTUAL UNDERSTANDING.

{context}

SCENARIO:
{scenario}

YOUR TASK:
Provide deep contextual analysis:

1. CONTEXTUAL DEPTH (0-100%):
   - How deep is the contextual understanding?
   - Cultural, historical, social, economic layers analyzed

2. STAKEHOLDER ANALYSIS:
   Identify and analyze stakeholder groups:
   - Who benefits?
   - Who is harmed?
   - Who is ignored?

3. ETHICAL TENSIONS:
   - What values are in conflict?
   - Where do competing interests collide?
   - Irreconcilable differences

4. CONTEXTUAL FACTORS:
   - Historical context
   - Cultural context
   - Economic context
   - Political context

REQUIRED OUTPUT FORMAT:
contextual_depth_score: [0-100]

STAKEHOLDER ANALYSIS:
Beneficiaries:
- [Group 1]
- [Group 2]

Harmed:
- [Group 1]
- [Group 2]

Ignored/Invisible:
- [Group 1]
- [Group 2]

ETHICAL TENSIONS:
- [Tension 1]
- [Tension 2]

CONTEXTUAL FACTORS:
- [Factor 1]
- [Factor 2]

UNDERSTANDING ANALYSIS:
[Your deep contextual analysis]
"""

    def _get_sigma_prompt(
        self,
        scenario: str,
        previous_results: Optional[Dict[str, Any]] = None,
        perspective: str = "Western"
    ) -> str:
        """Generate BinahSigma prompt for specific perspective."""
        context = self.format_previous_results(previous_results, ['keter', 'chochmah'])

        perspective_instruction = ""
        if perspective == "Western":
            perspective_instruction = """
PERSPECTIVE: Analyze from a WESTERN civilizational lens
- Emphasis on individual rights, liberty, universal values
- Liberal democratic frameworks
- Secular humanist ethics
- Post-Enlightenment philosophy
"""
        else:  # Eastern
            perspective_instruction = """
PERSPECTIVE: Analyze from an EASTERN civilizational lens
- Emphasis on collective harmony, duty, contextual values
- Confucian/Asian value frameworks
- Social stability and order
- Community over individualism
"""

        return f"""You are BINAH SIGMA - Multi-civilizational Understanding Analysis.

{perspective_instruction}

{context}

SCENARIO:
{scenario}

YOUR TASK:
Analyze this scenario from your assigned civilizational perspective:

1. PRIMARY CONCERNS:
   - What matters most from this perspective?
   - What values are prioritized?
   - What outcomes are desired?

2. BLIND SPOTS:
   - What does THIS perspective miss?
   - What assumptions are embedded?
   - What alternative viewpoints are dismissed?

3. RISKS PERCEIVED:
   - What dangers does this perspective see?
   - What is being protected?

4. OPPORTUNITIES PERCEIVED:
   - What benefits does this perspective see?
   - What improvements are possible?

5. MORAL FRAMING:
   - How is this framed ethically?
   - What moral principles apply?

OUTPUT FORMAT:
primary_concerns:
- [Concern 1]
- [Concern 2]

blind_spots:
- [Blind spot 1 of THIS perspective]
- [Blind spot 2 of THIS perspective]

risks_perceived:
- [Risk 1]
- [Risk 2]

opportunities_perceived:
- [Opportunity 1]
- [Opportunity 2]

moral_framing:
[How this perspective frames the ethical question]

ANALYSIS:
[Detailed analysis from this civilizational lens]
"""

    def _synthesize_sigma(
        self,
        west_response: str,
        east_response: str,
        scenario: str
    ) -> Dict[str, Any]:
        """Synthesize Western and Eastern perspectives."""
        try:
            # Extract blind spots from each perspective
            west_blinds = self.extract_list(west_response, marker="-", section="blind_spots")
            east_blinds = self.extract_list(east_response, marker="-", section="blind_spots")

            # Extract concerns
            west_concerns = self.extract_list(west_response, marker="-", section="primary_concerns")
            east_concerns = self.extract_list(east_response, marker="-", section="primary_concerns")

            # Calculate divergence
            bias_delta, divergence_level = self._calculate_divergence(
                west_response, east_response, west_concerns, east_concerns
            )

            # Find convergence points (similar concerns/values)
            universal_convergence = self._find_convergence(west_concerns, east_concerns)

            # Generate transcendent synthesis
            synthesis_prompt = self._get_synthesis_prompt(
                scenario, west_response, east_response, west_blinds, east_blinds, universal_convergence
            )

            synthesis_text = self.call_claude(synthesis_prompt)

            # Build BinahSigma analysis
            sigma_analysis = BinahSigmaAnalysis(
                west_blind_spots=west_blinds[:6],  # Limit to top 6
                east_blind_spots=east_blinds[:6],
                universal_convergence=universal_convergence,
                transcendent_synthesis=synthesis_text.strip()
            )

            result_data = {
                "mode": "sigma",
                "contextual_depth_score": 90,  # Sigma mode is inherently deep
                "bias_delta": bias_delta,
                "divergence_level": divergence_level,
                "blind_spots_detected": len(west_blinds) + len(east_blinds),
                "convergence_points": len(universal_convergence),
                "sigma_synthesis": sigma_analysis.model_dump(),
                "stakeholder_analysis": {
                    "western_priority": west_concerns[:3],
                    "eastern_priority": east_concerns[:3]
                },
                "ethical_tensions": [
                    f"Western emphasis vs Eastern emphasis on {i+1}"
                    for i in range(min(3, len(west_concerns)))
                ],
                "contextual_factors": [
                    "Multi-civilizational value divergence",
                    "Geopolitical tension present",
                    "Cultural assumptions embedded"
                ],
                "raw_understanding": f"=== WESTERN PERSPECTIVE ===\n{west_response}\n\n=== EASTERN PERSPECTIVE ===\n{east_response}"
            }

            binah_result = BinahResult(**result_data)
            return binah_result.model_dump()

        except Exception as e:
            self.logger.error("Failed to synthesize Sigma results", error=str(e), exc_info=True)
            raise

    def _calculate_divergence(
        self,
        west: str,
        east: str,
        west_concerns: List[str],
        east_concerns: List[str]
    ) -> Tuple[int, str]:
        """Calculate bias delta and divergence level."""
        # Simple heuristic: divergence based on concern overlap
        if not west_concerns or not east_concerns:
            return 50, "medium"

        # Count similar concerns (crude text similarity)
        similar_count = 0
        for w_concern in west_concerns:
            for e_concern in east_concerns:
                # Check for keyword overlap
                w_words = set(w_concern.lower().split())
                e_words = set(e_concern.lower().split())
                overlap = len(w_words & e_words)
                if overlap >= 2:  # At least 2 common words
                    similar_count += 1
                    break

        total = max(len(west_concerns), len(east_concerns))
        similarity = similar_count / total if total > 0 else 0
        bias_delta = int((1 - similarity) * 100)

        if bias_delta >= 60:
            divergence_level = "high"
        elif bias_delta >= 40:
            divergence_level = "medium"
        else:
            divergence_level = "low"

        return bias_delta, divergence_level

    def _find_convergence(
        self,
        west_concerns: List[str],
        east_concerns: List[str]
    ) -> List[str]:
        """Find universal convergence points."""
        convergence = []

        for w in west_concerns:
            for e in east_concerns:
                w_words = set(w.lower().split())
                e_words = set(e.lower().split())
                overlap = len(w_words & e_words)

                if overlap >= 3:  # Strong overlap
                    convergence.append(f"Both perspectives recognize: {w[:100]}")
                    break

        # Add common universal values
        if any("poverty" in c.lower() or "poor" in c.lower() for c in west_concerns + east_concerns):
            convergence.append("Universal agreement: Poverty reduction is valuable")

        if any("suffering" in c.lower() or "harm" in c.lower() for c in west_concerns + east_concerns):
            convergence.append("Universal agreement: Reducing suffering matters")

        return list(set(convergence))[:5]  # Max 5 convergence points

    def _get_synthesis_prompt(
        self,
        scenario: str,
        west: str,
        east: str,
        west_blinds: List[str],
        east_blinds: List[str],
        convergence: List[str]
    ) -> str:
        """Generate prompt for transcendent synthesis."""
        return f"""You are synthesizing two civilizational perspectives on an ethical scenario.

SCENARIO:
{scenario}

WESTERN BLIND SPOTS (what Western perspective misses):
{chr(10).join(f"- {b}" for b in west_blinds[:4])}

EASTERN BLIND SPOTS (what Eastern perspective misses):
{chr(10).join(f"- {b}" for b in east_blinds[:4])}

UNIVERSAL CONVERGENCE (what both agree on):
{chr(10).join(f"- {c}" for c in convergence)}

YOUR TASK:
Generate a TRANSCENDENT SYNTHESIS that:
1. Acknowledges both perspectives' valid concerns
2. Identifies a third path that addresses blind spots of both
3. Builds on universal convergence
4. Offers a novel approach neither perspective alone would see

Keep response to 150-200 words. Be specific and actionable.

TRANSCENDENT SYNTHESIS:
"""

    def _parse_simple_response(self, response: str) -> Dict[str, Any]:
        """Parse simple mode response."""
        try:
            depth = self._extract_percentage(response, "contextual_depth_score", 70)

            # Extract stakeholders
            beneficiaries = self.extract_list(response, section="Beneficiaries")
            harmed = self.extract_list(response, section="Harmed")
            ignored = self.extract_list(response, section="Ignored")

            stakeholder_analysis = {
                "beneficiaries": beneficiaries,
                "harmed": harmed,
                "ignored": ignored
            }

            # Extract tensions and factors
            tensions = self.extract_list(response, section="ETHICAL TENSIONS")
            factors = self.extract_list(response, section="CONTEXTUAL FACTORS")

            result_data = {
                "mode": "simple",
                "contextual_depth_score": depth,
                "stakeholder_analysis": stakeholder_analysis,
                "ethical_tensions": tensions,
                "contextual_factors": factors,
                "raw_understanding": response
            }

            binah_result = BinahResult(**result_data)
            return binah_result.model_dump()

        except Exception as e:
            self.logger.error("Failed to parse simple response", error=str(e), exc_info=True)
            return {
                "mode": "simple",
                "contextual_depth_score": 50,
                "stakeholder_analysis": {},
                "ethical_tensions": [],
                "contextual_factors": [],
                "raw_understanding": response
            }

    def _extract_percentage(self, text: str, field: str, default: int = 50) -> int:
        """Extract percentage value."""
        value = self.extract_field(text, field, default)
        if isinstance(value, str):
            match = re.search(r'\d+', value)
            value = int(match.group()) if match else default
        return max(0, min(100, value))
