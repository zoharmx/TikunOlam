"""
Tikun Olam FastAPI Application

REST API for ethical reasoning analysis.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import time
from typing import Dict, Any, Optional
import uuid
from pathlib import Path

from tikun.config import get_config
from tikun.orchestrator import TikunOrchestrator
from tikun.utils.logging import get_logger, setup_logging
from tikun.api.models import (
    AnalysisRequest,
    AnalysisResponse,
    HealthResponse,
    ErrorResponse,
    JobStatus,
    JobResponse
)
from tikun.api.persistence import get_persistence

# Setup logging
config = get_config()
setup_logging(level=config.log_level, enable_console=True)
logger = get_logger(__name__)

# Job persistence (GCS in Cloud Run, local files in dev)
persistence = get_persistence()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    logger.info("Starting Tikun Olam API", version="1.0.0")

    # Warmup Vertex AI to eliminate cold-start overhead
    from tikun.utils.warmup import warmup_vertex_ai
    logger.info("Initiating Vertex AI warmup...")
    warmup_success = await warmup_vertex_ai()
    if warmup_success:
        logger.info("Vertex AI ready - cold-start overhead eliminated")
    else:
        logger.warning("Vertex AI warmup failed - first request may be slow")

    yield
    # Shutdown
    logger.info("Shutting down Tikun Olam API")


# Create FastAPI app
app = FastAPI(
    title="Tikun Olam API",
    description="An Ethical Reasoning Architecture for AI Decision Systems",
    version="1.0.0",
    docs_url="/docs" if config.api_docs_enabled else None,
    redoc_url="/redoc" if config.api_docs_enabled else None,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    logger.info(
        f"Request completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=f"{duration:.2f}s"
    )

    return response


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            status_code=exc.status_code
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            status_code=500,
            details=str(exc) if config.is_development() else None
        ).model_dump()
    )


# Routes
# Note: Root "/" route is defined at the end of file to serve frontend


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint."""
    try:
        # Basic health check
        # In production, check DB connections, API keys, etc.
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            environment=config.tikun_env
        )
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_scenario(request: AnalysisRequest):
    """
    Analyze scenario through Tikun Olam pipeline (synchronous).

    This endpoint processes the scenario immediately and returns results.
    For long-running analyses, use /analyze/async instead.
    """
    try:
        logger.info(
            "Starting synchronous analysis",
            case_name=request.case_name,
            scenario_length=len(request.scenario)
        )

        # Create orchestrator
        orchestrator = TikunOrchestrator(verbose=request.verbose)

        # Process scenario
        results = orchestrator.process(
            scenario=request.scenario,
            case_name=request.case_name,
            auto_export=request.auto_export
        )

        # Extract key metrics
        metadata = results.get('metadata', {})
        sefirot = results.get('sefirot_results', {})

        malchut = sefirot.get('malchut', {})
        final_decision = malchut.get('decision', 'UNKNOWN')

        # Get structured summary
        summary_dict = orchestrator.get_summary(results)

        return AnalysisResponse(
            case_name=metadata.get('case_name', 'unknown'),
            status="completed",
            decision=final_decision,
            confidence=malchut.get('confidence', 'unknown'),
            duration_seconds=metadata.get('total_duration_seconds', 0),
            results=results if request.include_full_results else None,
            summary=summary_dict,
            sefirot_results=sefirot,
            metadata=metadata
        )

    except ValueError as e:
        logger.error("Validation error", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error("Analysis failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/async", response_model=JobResponse, tags=["Analysis"])
async def analyze_scenario_async(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Analyze scenario asynchronously.

    Returns a job ID immediately. Use /jobs/{job_id} to check status.
    """
    try:
        # Generate job ID
        job_id = str(uuid.uuid4())

        # Create job data
        job_data = {
            "id": job_id,
            "status": "pending",
            "case_name": request.case_name,
            "created_at": time.time(),
            "results": None,
            "error": None
        }

        # Save to persistence
        if not persistence.save_job(job_id, job_data):
            raise HTTPException(status_code=500, detail="Failed to save job")

        # Add to background tasks
        background_tasks.add_task(
            process_analysis_background,
            job_id,
            request
        )

        logger.info("Created async analysis job", job_id=job_id, case_name=request.case_name)

        return JobResponse(
            job_id=job_id,
            status="pending",
            message="Analysis started. Check /jobs/{job_id} for status."
        )

    except Exception as e:
        logger.error("Failed to create async job", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@app.get("/jobs/{job_id}", response_model=JobStatus, tags=["Jobs"])
async def get_job_status(job_id: str):
    """Get status of async analysis job."""
    # Load from persistence
    job = persistence.load_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    response = JobStatus(
        job_id=job_id,
        status=job["status"],
        case_name=job["case_name"],
        created_at=job["created_at"],
        completed_at=job.get("completed_at"),
        duration_seconds=job.get("duration_seconds"),
        error=job.get("error")
    )

    # Include results if completed
    if job["status"] == "completed" and job.get("results"):
        response.results = job["results"]

    return response


@app.delete("/jobs/{job_id}", tags=["Jobs"])
async def delete_job(job_id: str):
    """Delete a job and its results."""
    if not persistence.job_exists(job_id):
        raise HTTPException(status_code=404, detail="Job not found")

    persistence.delete_job(job_id)
    logger.info("Deleted job", job_id=job_id)

    return {"message": "Job deleted successfully"}


@app.get("/jobs", tags=["Jobs"])
async def list_jobs(limit: int = 100, status: Optional[str] = None):
    """List all jobs."""
    # Get all job IDs
    job_ids = persistence.list_jobs(limit=limit * 2)  # Get extra for filtering

    # Load job data
    job_list = []
    for job_id in job_ids:
        job_data = persistence.load_job(job_id)
        if job_data:
            job_list.append(job_data)

    # Filter by status if provided
    if status:
        job_list = [j for j in job_list if j["status"] == status]

    # Sort by created_at descending
    job_list.sort(key=lambda x: x.get("created_at", 0), reverse=True)

    # Limit
    job_list = job_list[:limit]

    return {
        "jobs": job_list,
        "total": len(job_list)
    }


# Background task function
async def process_analysis_background(job_id: str, request: AnalysisRequest):
    """Process analysis in background."""
    try:
        # Load job and update status
        job = persistence.load_job(job_id)
        if job:
            job["status"] = "processing"
            persistence.save_job(job_id, job)

        start_time = time.time()

        # Create orchestrator and process
        orchestrator = TikunOrchestrator(verbose=request.verbose)

        results = orchestrator.process(
            scenario=request.scenario,
            case_name=request.case_name,
            auto_export=request.auto_export
        )

        duration = time.time() - start_time

        # Load job again and update with results
        job = persistence.load_job(job_id)
        if job:
            job.update({
                "status": "completed",
                "completed_at": time.time(),
                "duration_seconds": duration,
                "results": results if request.include_full_results else None
            })
            persistence.save_job(job_id, job)

        logger.info(
            "Background analysis completed",
            job_id=job_id,
            duration=duration
        )

    except Exception as e:
        logger.error(
            "Background analysis failed",
            job_id=job_id,
            error=str(e),
            exc_info=True
        )

        # Load job and update with error
        job = persistence.load_job(job_id)
        if job:
            job.update({
                "status": "failed",
                "completed_at": time.time(),
                "error": str(e)
            })
            persistence.save_job(job_id, job)


# Serve frontend static files
frontend_dist = Path("/app/frontend/dist")
if frontend_dist.exists():
    # Mount static assets (CSS, JS, images)
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    # Root route for frontend
    @app.get("/", include_in_schema=False)
    async def serve_frontend_root():
        """Serve React frontend root."""
        index_file = frontend_dist / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        raise HTTPException(status_code=404, detail="Frontend not found")

    # Catch-all route for SPA (must be last)
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        """Serve React frontend for all non-API routes."""
        # Serve index.html for SPA routing
        index_file = frontend_dist / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        raise HTTPException(status_code=404, detail="Frontend not found")

    logger.info("Frontend static files mounted", path=str(frontend_dist))
else:
    logger.warning("Frontend dist folder not found", path=str(frontend_dist))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "tikun.api.main:app",
        host=config.api_host,
        port=config.api_port,
        reload=config.is_development(),
        log_level=config.log_level.lower()
    )
