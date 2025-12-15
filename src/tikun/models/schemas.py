"""
Pydantic models for Tikun Olam data structures

Provides type-safe, validated data models for all Sefirot results
and pipeline outputs.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# COMMON MODELS
# ============================================================================

class Corruption(BaseModel):
    """Model for ethical corruption detection."""
    type: str = Field(..., description="Type of corruption")
    severity: Literal["low", "medium", "high", "critical"]
    description: str
    examples: List[str] = Field(default_factory=list)


class Precedent(BaseModel):
    """Model for historical precedent."""
    name: str
    year: Optional[int] = None
    outcome: str
    relevance: str
    lessons: List[str] = Field(default_factory=list)


class BlindSpot(BaseModel):
    """Model for civilizational blind spot."""
    description: str
    severity: Literal["minor", "moderate", "significant", "critical"]
    affected_stakeholders: List[str] = Field(default_factory=list)


# ============================================================================
# KETER (Scope Definition & Validation)
# ============================================================================

class KeterResult(BaseModel):
    """Result model for Keter (Scope Definition)."""
    alignment_percentage: int = Field(..., ge=0, le=100)
    corruption_severity: Literal["none", "low", "medium", "high", "critical"]
    manifestation_valid: bool
    threshold_met: bool

    # Detailed scoring
    scores: Dict[str, int] = Field(
        default_factory=dict,
        description="Dimension scores (-10 to +10)"
    )

    # Corruptions detected
    corruptions: List[Corruption] = Field(default_factory=list)

    # Raw analysis
    raw_analysis: str = Field(default="")


# ============================================================================
# CHOCHMAH (Wisdom Analysis)
# ============================================================================

class ChochmahResult(BaseModel):
    """Result model for Chochmah (Wisdom Analysis)."""
    confidence_level: int = Field(..., ge=0, le=100)
    epistemic_humility_ratio: int = Field(..., ge=0, le=100)
    insight_depth_score: int = Field(..., ge=0, le=100)

    # Pattern analysis
    patterns_identified: List[str] = Field(default_factory=list)

    # Historical precedents
    precedents: List[Precedent] = Field(default_factory=list)

    # Hidden insights
    hidden_insights: List[str] = Field(default_factory=list)

    # Paradoxes
    paradoxes_identified: List[str] = Field(default_factory=list)

    # Raw wisdom
    raw_wisdom: str = Field(default="")


# ============================================================================
# BINAH (Understanding / BinahSigma)
# ============================================================================

class BinahSigmaAnalysis(BaseModel):
    """Model for BinahSigma multi-civilizational analysis."""
    west_blind_spots: List[str] = Field(default_factory=list)
    east_blind_spots: List[str] = Field(default_factory=list)
    universal_convergence: List[str] = Field(default_factory=list)
    transcendent_synthesis: str = Field(default="")


class BinahResult(BaseModel):
    """Result model for Binah (Understanding)."""
    mode: Literal["simple", "sigma"] = Field(
        default="simple",
        description="Analysis mode: simple or sigma (multi-civilizational)"
    )
    contextual_depth_score: int = Field(..., ge=0, le=100)

    # BinahSigma specific (only if mode=sigma)
    bias_delta: Optional[int] = Field(
        None,
        ge=0,
        le=100,
        description="Divergence between perspectives (%)"
    )
    divergence_level: Optional[Literal["low", "medium", "high"]] = None
    blind_spots_detected: Optional[int] = Field(None, ge=0)
    convergence_points: Optional[int] = Field(None, ge=0)

    sigma_synthesis: Optional[BinahSigmaAnalysis] = None

    # Simple mode analysis
    stakeholder_analysis: Dict[str, List[str]] = Field(default_factory=dict)
    ethical_tensions: List[str] = Field(default_factory=list)
    contextual_factors: List[str] = Field(default_factory=list)

    # Raw analysis
    raw_understanding: str = Field(default="")


# ============================================================================
# CHESED (Kindness / Opportunity)
# ============================================================================

class Opportunity(BaseModel):
    """Model for opportunity evaluation."""
    description: str
    potential_impact: Literal["low", "medium", "high", "transformative"]
    beneficiaries: List[str]
    confidence: int = Field(..., ge=0, le=100)


class ChesedResult(BaseModel):
    """Result model for Chesed (Opportunity Evaluation)."""
    expansion_potential: int = Field(..., ge=0, le=100)
    generosity_score: int = Field(..., ge=0, le=100)

    # Opportunities
    opportunities: List[Opportunity] = Field(default_factory=list)

    # Long-term benefits
    long_term_benefits: List[str] = Field(default_factory=list)

    # Positive externalities
    positive_externalities: List[str] = Field(default_factory=list)

    # Raw analysis
    raw_opportunity: str = Field(default="")


# ============================================================================
# GEVURAH (Strength / Risk)
# ============================================================================

class Risk(BaseModel):
    """Model for risk assessment."""
    description: str
    severity: Literal["low", "medium", "high", "critical"]
    probability: Literal["unlikely", "possible", "likely", "certain"]
    affected_parties: List[str]
    mitigation: Optional[str] = None


class GevurahResult(BaseModel):
    """Result model for Gevurah (Risk Assessment)."""
    constraint_strength: int = Field(..., ge=0, le=100)
    risk_severity: Literal["low", "medium", "high", "critical"]

    # Risks
    risks: List[Risk] = Field(default_factory=list)

    # Boundaries and limits
    boundaries_identified: List[str] = Field(default_factory=list)

    # Negative externalities
    negative_externalities: List[str] = Field(default_factory=list)

    # Irreversibility assessment
    irreversible_consequences: List[str] = Field(default_factory=list)

    # Raw analysis
    raw_risk: str = Field(default="")


# ============================================================================
# TIFERET (Beauty / Synthesis)
# ============================================================================

class TiferetResult(BaseModel):
    """Result model for Tiferet (Synthesis & Balance)."""
    harmony_score: int = Field(..., ge=0, le=100)
    balance_quality: Literal["poor", "acceptable", "good", "excellent"]

    # Synthesis
    synthesis_statement: str = Field(default="")

    # Balance analysis
    chesed_gevurah_balance: str = Field(
        default="",
        description="Balance between opportunity and risk"
    )

    # Tradeoffs
    key_tradeoffs: List[str] = Field(default_factory=list)

    # Recommended path
    recommended_approach: str = Field(default="")

    # Raw synthesis
    raw_synthesis: str = Field(default="")


# ============================================================================
# NETZACH (Victory / Strategy)
# ============================================================================

class Strategy(BaseModel):
    """Model for strategic approach."""
    name: str
    description: str
    priority: Literal["low", "medium", "high", "critical"]
    timeline: Optional[str] = None
    resources_required: List[str] = Field(default_factory=list)


class NetzachResult(BaseModel):
    """Result model for Netzach (Strategy Formation)."""
    persistence_score: int = Field(..., ge=0, le=100)
    strategic_clarity: Literal["unclear", "developing", "clear", "compelling"]

    # Strategies
    strategies: List[Strategy] = Field(default_factory=list)

    # Success factors
    critical_success_factors: List[str] = Field(default_factory=list)

    # Obstacles
    potential_obstacles: List[str] = Field(default_factory=list)

    # Long-term vision
    long_term_vision: str = Field(default="")

    # Raw strategy
    raw_strategy: str = Field(default="")


# ============================================================================
# HOD (Splendor / Communication)
# ============================================================================

class CommunicationChannel(BaseModel):
    """Model for communication channel."""
    audience: str
    key_messages: List[str]
    tone: str
    medium: List[str]


class HodResult(BaseModel):
    """Result model for Hod (Communication Design)."""
    clarity_score: int = Field(..., ge=0, le=100)
    communication_quality: Literal["poor", "acceptable", "good", "excellent"]

    # Communication channels
    channels: List[CommunicationChannel] = Field(default_factory=list)

    # Stakeholder messaging
    stakeholder_messaging: Dict[str, str] = Field(default_factory=dict)

    # Transparency requirements
    transparency_requirements: List[str] = Field(default_factory=list)

    # Raw communication
    raw_communication: str = Field(default="")


# ============================================================================
# YESOD (Foundation / Integration)
# ============================================================================

class Gap(BaseModel):
    """Model for identified gap."""
    gap: str
    severity: Literal["minor", "moderate", "significant", "critical"]
    sefirah: str
    recommendation: str


class CoherenceCheck(BaseModel):
    """Model for coherence check."""
    aspect: str
    status: Literal["aligned", "partial", "conflicting"]
    details: str


class YesodResult(BaseModel):
    """Result model for Yesod (Integration & Coherence)."""
    readiness_score: int = Field(..., ge=0, le=100)
    integration_quality: Literal["poor", "acceptable", "good", "excellent"]
    foundation_strength: Literal["weak", "moderate", "strong", "robust"]
    yesod_quality: Literal["poor", "acceptable", "good", "exceptional"]

    # Coherence analysis
    sefirot_alignment: Dict[str, Any] = Field(default_factory=dict)
    overall_coherence: Dict[str, Any] = Field(default_factory=dict)

    # Gaps identified
    gaps_identified: List[Gap] = Field(default_factory=list)

    # Go/No-Go recommendation
    go_no_go_recommendation: Dict[str, Any] = Field(default_factory=dict)

    # Integration summary
    integration_summary: str = Field(default="")


# ============================================================================
# MALCHUT (Kingdom / Manifestation)
# ============================================================================

class MalchutResult(BaseModel):
    """Result model for Malchut (Manifestation & Decision)."""
    manifestation_quality: Literal["poor", "acceptable", "good", "excellent"]
    decision: Literal["GO", "NO_GO", "CONDITIONAL_GO"]
    confidence: Literal["low", "medium", "high", "very_high"]

    # Decision rationale
    decision_rationale: str = Field(default="")

    # Implementation plan
    implementation_steps: List[str] = Field(default_factory=list)

    # Conditions (if CONDITIONAL_GO)
    conditions: List[str] = Field(default_factory=list)

    # Success metrics
    success_metrics: List[str] = Field(default_factory=list)

    # Monitoring requirements
    monitoring_requirements: List[str] = Field(default_factory=list)

    # Final summary
    final_summary: str = Field(default="")


# ============================================================================
# COMPLETE RESULTS
# ============================================================================

class SefirotResults(BaseModel):
    """Container for all Sefirot results."""
    keter: Optional[KeterResult] = None
    chochmah: Optional[ChochmahResult] = None
    binah: Optional[BinahResult] = None
    chesed: Optional[ChesedResult] = None
    gevurah: Optional[GevurahResult] = None
    tiferet: Optional[TiferetResult] = None
    netzach: Optional[NetzachResult] = None
    hod: Optional[HodResult] = None
    yesod: Optional[YesodResult] = None
    malchut: Optional[MalchutResult] = None


class TikunMetadata(BaseModel):
    """Metadata for Tikun analysis."""
    version: str = Field(default="1.0.0")
    timestamp: datetime = Field(default_factory=datetime.now)
    case_name: str
    scenario_length: int = Field(..., ge=0)
    total_duration_seconds: Optional[float] = None
    models_used: Dict[str, str] = Field(default_factory=dict)


class TikunResults(BaseModel):
    """Complete Tikun Olam analysis results."""
    metadata: TikunMetadata
    sefirot_results: SefirotResults
    scenario: str = Field(..., description="Original scenario text")

    model_config = {
        "json_schema_extra": {
            "example": {
                "metadata": {
                    "version": "1.0.0",
                    "case_name": "example_case",
                    "scenario_length": 1500,
                },
                "sefirot_results": {},
                "scenario": "Example scenario text..."
            }
        }
    }
