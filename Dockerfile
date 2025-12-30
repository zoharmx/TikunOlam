# Tikun Olam - Cloud Run Optimized Multi-Stage Build
# Google Cloud AI Partner Catalyst - Datadog Challenge

# ============================================================================
# Stage 1: Use Pre-built Frontend (Skip build in Docker)
# ============================================================================
FROM scratch AS frontend-builder

# This is a placeholder stage - we'll copy the pre-built dist directly

# ============================================================================
# Stage 2: Build Python Dependencies
# ============================================================================
FROM python:3.11-slim AS python-builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies to user directory
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================================================
# Stage 3: Runtime Image (Cloud Run Optimized)
# ============================================================================
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies (curl for health checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 tikun && \
    mkdir -p /app/results /app/logs && \
    chown -R tikun:tikun /app

# Copy Python dependencies from builder
COPY --from=python-builder /root/.local /home/tikun/.local

# Copy application code
COPY --chown=tikun:tikun src/ /app/src/
COPY --chown=tikun:tikun monitoring/ /app/monitoring/
COPY --chown=tikun:tikun .env.example /app/.env.example

# Copy pre-built frontend from local build
COPY --chown=tikun:tikun frontend/dist /app/frontend/dist

# Switch to non-root user
USER tikun

# Environment setup
ENV PATH=/home/tikun/.local/bin:$PATH \
    PYTHONPATH=/app/src:$PYTHONPATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Cloud Run uses PORT environment variable (defaults to 8080)
EXPOSE 8080

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Start application with uvicorn
# Cloud Run will inject PORT environment variable
CMD exec uvicorn src.tikun.api.main:app \
    --host 0.0.0.0 \
    --port ${PORT} \
    --workers 2 \
    --log-level info \
    --access-log
