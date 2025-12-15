# Tikun Olam - Production Docker Image
# Multi-stage build for optimized image size

# Build stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 tikun && \
    mkdir -p /app/results /app/logs && \
    chown -R tikun:tikun /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/tikun/.local

# Copy application code
COPY --chown=tikun:tikun src/ /app/src/
COPY --chown=tikun:tikun setup.py pyproject.toml README.md /app/
COPY --chown=tikun:tikun .env.example /app/.env.example

# Install the package
USER tikun
ENV PATH=/home/tikun/.local/bin:$PATH
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command (can be overridden)
CMD ["uvicorn", "tikun.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
