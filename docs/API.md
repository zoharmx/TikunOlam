# Tikun Olam API Documentation

REST API for ethical reasoning analysis.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required. In production, set `API_AUTH_TOKEN` in `.env`.

## Endpoints

### GET /

Root endpoint with API information.

**Response:**
```json
{
  "name": "Tikun Olam API",
  "version": "1.0.0",
  "description": "An Ethical Reasoning Architecture for AI Decision Systems",
  "docs": "/docs"
}
```

---

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

---

### POST /analyze

Analyze scenario synchronously (blocking).

**Request Body:**
```json
{
  "scenario": "Your ethical scenario text (50-50000 chars)",
  "case_name": "optional_case_name",
  "verbose": false,
  "auto_export": true,
  "include_full_results": true
}
```

**Parameters:**
- `scenario` (string, required): Ethical scenario to analyze
- `case_name` (string, optional): Name for this case
- `verbose` (boolean, default: false): Enable verbose logging
- `auto_export` (boolean, default: true): Export results to files
- `include_full_results` (boolean, default: true): Include full Sefirot results

**Response (200 OK):**
```json
{
  "case_name": "healthcare_proposal",
  "status": "completed",
  "decision": "CONDITIONAL_GO",
  "confidence": "high",
  "duration_seconds": 187.3,
  "results": {
    "sefirot_results": { ... },
    "metadata": { ... }
  },
  "summary": "TIKUN OLAM ANALYSIS SUMMARY\n..."
}
```

**Errors:**
- `400 Bad Request`: Invalid scenario (too short, too long, suspicious content)
- `500 Internal Server Error`: Analysis failed

**Example:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "PROPOSAL: Universal basic income...",
    "case_name": "ubi_analysis"
  }'
```

---

### POST /analyze/async

Analyze scenario asynchronously (non-blocking).

Returns job ID immediately. Use `/jobs/{job_id}` to check status.

**Request Body:** Same as `/analyze`

**Response (200 OK):**
```json
{
  "job_id": "a3d4e5f6-7890-1234-5678-90abcdef1234",
  "status": "pending",
  "message": "Analysis started. Check /jobs/{job_id} for status."
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/analyze/async \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "PROPOSAL: Carbon tax...",
    "case_name": "carbon_tax"
  }'
```

---

### GET /jobs/{job_id}

Get status of async analysis job.

**Path Parameters:**
- `job_id` (string): Job ID from `/analyze/async`

**Response (200 OK):**
```json
{
  "job_id": "a3d4e5f6-7890-1234-5678-90abcdef1234",
  "status": "completed",
  "case_name": "carbon_tax",
  "created_at": 1704123456.789,
  "completed_at": 1704123640.123,
  "duration_seconds": 183.334,
  "results": { ... },
  "error": null
}
```

**Status Values:**
- `pending`: Job created, not yet started
- `processing`: Analysis in progress
- `completed`: Analysis finished successfully
- `failed`: Analysis failed (check `error` field)

**Errors:**
- `404 Not Found`: Job ID doesn't exist

**Example:**
```bash
curl http://localhost:8000/jobs/a3d4e5f6-7890-1234-5678-90abcdef1234
```

---

### GET /jobs

List all jobs.

**Query Parameters:**
- `limit` (integer, default: 100): Maximum jobs to return
- `status` (string, optional): Filter by status (pending, processing, completed, failed)

**Response (200 OK):**
```json
{
  "jobs": [
    {
      "id": "job-1",
      "status": "completed",
      "case_name": "test1",
      "created_at": 1704123456.789
    },
    ...
  ],
  "total": 42
}
```

**Example:**
```bash
# Get all completed jobs
curl "http://localhost:8000/jobs?status=completed&limit=10"
```

---

### DELETE /jobs/{job_id}

Delete a job and its results.

**Path Parameters:**
- `job_id` (string): Job ID to delete

**Response (200 OK):**
```json
{
  "message": "Job deleted successfully"
}
```

**Errors:**
- `404 Not Found`: Job ID doesn't exist

---

## Response Models

### AnalysisResponse

```typescript
{
  case_name: string,
  status: "completed" | "failed",
  decision: "GO" | "NO_GO" | "CONDITIONAL_GO",
  confidence: "low" | "medium" | "high" | "very_high",
  duration_seconds: number,
  results?: {
    sefirot_results: SefirotResults,
    metadata: Metadata,
    scenario: string
  },
  summary: string
}
```

### SefirotResults

```typescript
{
  keter: KeterResult,
  chochmah: ChochmahResult,
  binah: BinahResult,
  chesed: ChesedResult,
  gevurah: GevurahResult,
  tiferet: TiferetResult,
  netzach: NetzachResult,
  hod: HodResult,
  yesod: YesodResult,
  malchut: MalchutResult
}
```

### KeterResult

```typescript
{
  alignment_percentage: number,     // 0-100
  corruption_severity: "none" | "low" | "medium" | "high" | "critical",
  manifestation_valid: boolean,
  threshold_met: boolean,
  scores: {
    Justice: number,              // -10 to +10
    Compassion: number,
    Wisdom: number,
    Sustainability: number,
    Dignity: number
  },
  corruptions: Corruption[],
  raw_analysis: string
}
```

### BinahResult (Sigma Mode)

```typescript
{
  mode: "sigma",
  contextual_depth_score: number,   // 0-100
  bias_delta: number,               // 0-100 (divergence %)
  divergence_level: "low" | "medium" | "high",
  blind_spots_detected: number,
  convergence_points: number,
  sigma_synthesis: {
    west_blind_spots: string[],
    east_blind_spots: string[],
    universal_convergence: string[],
    transcendent_synthesis: string
  },
  raw_understanding: string
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "status_code": 400,
  "details": "Additional details (development only)"
}
```

**Common HTTP Status Codes:**
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service unhealthy

---

## Rate Limiting

Configured via `RATE_LIMIT_RPM` in `.env` (default: 60 requests/minute).

No rate limiting headers implemented yet.

---

## Interactive Documentation

When API is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Python Client Example

```python
import requests

# Synchronous analysis
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "scenario": "PROPOSAL: ...",
        "case_name": "my_analysis"
    }
)

result = response.json()
print(f"Decision: {result['decision']}")
print(f"Confidence: {result['confidence']}")

# Async analysis
job_response = requests.post(
    "http://localhost:8000/analyze/async",
    json={"scenario": "...", "case_name": "async_test"}
)

job_id = job_response.json()["job_id"]

# Poll for completion
import time
while True:
    status = requests.get(f"http://localhost:8000/jobs/{job_id}").json()

    if status["status"] == "completed":
        print("Analysis complete!")
        break
    elif status["status"] == "failed":
        print(f"Analysis failed: {status['error']}")
        break

    print("Still processing...")
    time.sleep(10)
```

---

## WebSocket Support

Not yet implemented. Coming in v1.1.

---

## Versioning

API version is included in response metadata. Breaking changes will increment major version.

Current version: `1.0.0`

---

For more information, see:
- [Installation Guide](INSTALL.md)
- [Quick Start](../QUICKSTART.md)
- [BinahSigma Documentation](BINAH_SIGMA.md)
