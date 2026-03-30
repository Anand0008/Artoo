# Copyright (c) 2025-2026 Telomere LLC. All rights reserved.
# Proprietary and confidential. See LICENSE file in the project root.

# ═══════════════════════════════════════════════════════════════
# Stage 1: BUILD — Cython compile Python source to .so binaries
# ═══════════════════════════════════════════════════════════════
FROM python:3.12-slim AS builder

# Build tools for Cython compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Install Cython + project dependencies (cached layer)
COPY src/requirements.txt .
RUN pip install --no-cache-dir cython setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Copy source and compilation manifest
COPY src/ .
COPY setup.py .

# Compile all modules to .so
RUN python setup.py build_ext --inplace

# ── Strip source: remove .py files (keep only entry points) ──
# Remove all .c artifacts from Cython
RUN find . -name "*.c" -delete

# Remove .py files EXCEPT the 3 entry points and __init__.py
RUN find . -name "*.py" \
    ! -name "main.py" \
    ! -name "dashboard.py" \
    ! -path "./metrics/server.py" \
    ! -name "__init__.py" \
    ! -name "setup.py" \
    -delete

# Remove setup.py (no longer needed)
RUN rm -f setup.py

# Remove build/ directory from setuptools
RUN rm -rf build/

# ═══════════════════════════════════════════════════════════════
# Stage 2: RUNTIME — slim image with no build tools
# ═══════════════════════════════════════════════════════════════
FROM python:3.12-slim

# ── OCI Metadata ─────────────────────────────────────────────
LABEL org.opencontainers.image.title="Artoo" \
      org.opencontainers.image.description="Multi-agent AI system — AI-driven SDLC workflow automation" \
      org.opencontainers.image.vendor="Telomere LLC" \
      org.opencontainers.image.licenses="Telomere-Proprietary-Freeware" \
      org.opencontainers.image.authors="Telomere LLC <<email>>"

# ── Environment ──────────────────────────────────────────────
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ── System dependencies ─────────────────────────────────────
# curl: health checks
# git:  langchain/mcp packages inspect git at import time
# Node 20: @modelcontextprotocol/server-github (npx)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── uv (required to run uvx mcp-atlassian) ──────────────────
RUN pip install uv

# ── Pre-warm MCP servers ────────────────────────────────────
RUN npx --yes @modelcontextprotocol/server-github --help 2>/dev/null || true
RUN uvx mcp-atlassian --help 2>/dev/null || true

WORKDIR /app

# ── Python dependencies ─────────────────────────────────────
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Compiled application (no source code) ────────────────────
COPY --from=builder /build/ /app/

# ── Runtime directories ──────────────────────────────────────
RUN mkdir -p /app/logs

# ── Non-root user ────────────────────────────────────────────
RUN useradd --no-create-home --shell /bin/false appuser \
    && chown -R appuser:appuser /app
USER appuser

# ── Expose metrics API port ──────────────────────────────────
EXPOSE 8080

# ── Default: run the Jira scheduler ──────────────────────────
CMD ["python", "main.py", "--mode", "scheduler"]
