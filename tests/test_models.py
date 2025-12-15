"""
Tests for Pydantic models
"""

import pytest
from pydantic import ValidationError
from tikun.models.schemas import (
    KeterResult,
    ChochmahResult,
    BinahResult,
    Corruption,
    Precedent,
    Opportunity,
    Risk
)


def test_keter_result_valid():
    """Test valid KeterResult creation."""
    result = KeterResult(
        alignment_percentage=75,
        corruption_severity="low",
        manifestation_valid=True,
        threshold_met=True,
        scores={"Justice": 7, "Compassion": 8},
        corruptions=[],
        raw_analysis="Test analysis"
    )

    assert result.alignment_percentage == 75
    assert result.corruption_severity == "low"
    assert result.manifestation_valid is True


def test_keter_result_validation():
    """Test KeterResult validation."""
    # Invalid alignment percentage
    with pytest.raises(ValidationError):
        KeterResult(
            alignment_percentage=150,  # Over 100
            corruption_severity="low",
            manifestation_valid=True,
            threshold_met=True
        )

    # Invalid corruption severity
    with pytest.raises(ValidationError):
        KeterResult(
            alignment_percentage=75,
            corruption_severity="invalid",
            manifestation_valid=True,
            threshold_met=True
        )


def test_corruption_model():
    """Test Corruption model."""
    corruption = Corruption(
        type="Deception",
        severity="high",
        description="Misleading information about benefits",
        examples=["Example 1", "Example 2"]
    )

    assert corruption.type == "Deception"
    assert corruption.severity == "high"
    assert len(corruption.examples) == 2


def test_precedent_model():
    """Test Precedent model."""
    precedent = Precedent(
        name="Marshall Plan",
        year=1948,
        outcome="Successful economic recovery",
        relevance="Shows value of international aid",
        lessons=["Lesson 1", "Lesson 2"]
    )

    assert precedent.name == "Marshall Plan"
    assert precedent.year == 1948


def test_chochmah_result():
    """Test ChochmahResult."""
    result = ChochmahResult(
        confidence_level=80,
        epistemic_humility_ratio=40,
        insight_depth_score=75,
        patterns_identified=["Pattern 1", "Pattern 2"],
        precedents=[],
        hidden_insights=[],
        paradoxes_identified=[],
        raw_wisdom="Test wisdom"
    )

    assert result.confidence_level == 80
    assert len(result.patterns_identified) == 2


def test_binah_result_simple_mode():
    """Test BinahResult in simple mode."""
    result = BinahResult(
        mode="simple",
        contextual_depth_score=70,
        stakeholder_analysis={"beneficiaries": ["Group 1"]},
        ethical_tensions=["Tension 1"],
        contextual_factors=["Factor 1"],
        raw_understanding="Test"
    )

    assert result.mode == "simple"
    assert result.bias_delta is None  # Not used in simple mode


def test_binah_result_sigma_mode():
    """Test BinahResult in sigma mode."""
    result = BinahResult(
        mode="sigma",
        contextual_depth_score=90,
        bias_delta=45,
        divergence_level="medium",
        blind_spots_detected=8,
        convergence_points=3,
        sigma_synthesis={
            "west_blind_spots": ["Spot 1"],
            "east_blind_spots": ["Spot 2"],
            "universal_convergence": ["Point 1"],
            "transcendent_synthesis": "Synthesis text"
        },
        raw_understanding="Test"
    )

    assert result.mode == "sigma"
    assert result.bias_delta == 45
    assert result.divergence_level == "medium"


def test_opportunity_model():
    """Test Opportunity model."""
    opp = Opportunity(
        description="Increase community cohesion",
        potential_impact="high",
        beneficiaries=["Local residents", "Businesses"],
        confidence=85
    )

    assert opp.potential_impact == "high"
    assert len(opp.beneficiaries) == 2


def test_risk_model():
    """Test Risk model."""
    risk = Risk(
        description="Project may fail due to lack of funding",
        severity="medium",
        probability="possible",
        affected_parties=["Community members"],
        mitigation="Secure multiple funding sources"
    )

    assert risk.severity == "medium"
    assert risk.probability == "possible"
    assert risk.mitigation is not None
