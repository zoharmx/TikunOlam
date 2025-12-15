"""
API Request/Response Models

Pydantic models for FastAPI endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal


class AnalysisRequest(BaseModel):
    """Request model for scenario analysis."""

    scenario: str = Field(
        ...,
        description="The ethical scenario to analyze",
        min_length=50,
        max_length=50000
    )

    case_name: Optional[str] = Field(
        None,
        description="Optional name for this case"
    )

    verbose: bool = Field(
        default=False,
        description="Enable verbose logging"
    )

    auto_export: bool = Field(
        default=True,
        description="Automatically export results to files"
    )

    include_full_results: bool = Field(
        default=True,
        description="Include full Sefirot results in response"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "scenario": "PROPOSAL: Implement universal basic healthcare...",
                "case_name": "healthcare_proposal",
                "verbose": False,
                "auto_export": True,
                "include_full_results": True
            }
        }
    }


class AnalysisResponse(BaseModel):
    """Response model for completed analysis."""

    case_name: str
    status: Literal["completed", "failed"]
    decision: str = Field(description="Final decision: GO, NO_GO, or CONDITIONAL_GO")
    confidence: str = Field(description="Confidence level: low, medium, high, very_high")
    duration_seconds: float
    results: Optional[Dict[str, Any]] = Field(
        None,
        description="Full Sefirot results (if include_full_results=True)"
    )
    summary: str = Field(description="Human-readable summary")


class JobResponse(BaseModel):
    """Response model for async job creation."""

    job_id: str
    status: Literal["pending", "processing"]
    message: str


class JobStatus(BaseModel):
    """Job status model."""

    job_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    case_name: str
    created_at: float
    completed_at: Optional[float] = None
    duration_seconds: Optional[float] = None
    error: Optional[str] = None
    results: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: Literal["healthy", "degraded", "unhealthy"]
    version: str
    environment: str


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str
    status_code: int
    details: Optional[str] = None
