# Artoo — Deployment Guide

Copyright (c) 2025-2026 Telomere LLC. All rights reserved.
See [LICENSE](LICENSE) for terms.

Artoo is a multi-agent AI system that automates SDLC workflows by monitoring
Jira tickets, validating completeness, scouting repositories, searching
Confluence, and generating implementation plans with Draft GitHub PRs.

---

## Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine + Compose** (Linux)
- An internet connection (for Jira, GitHub, Confluence, and LLM API access)

No Python, Node.js, or PostgreSQL installation is required on your machine.

---

## Quick Start

### 1. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and fill in:
- **AWS Bedrock** credentials (or OpenAI API key)
- **Jira** URL, username, and API token
- **Confluence** URL and space keys
- **GitHub** personal access token, repo owner, and repo name
- **Database URL** (see below)
- **Metrics API key** (choose any secure string)

### 2a. AWS Deployment (EC2 + RDS PostgreSQL)

Set `DATABASE_URL` in `.env` to your RDS endpoint:
```
DATABASE_URL=postgresql://<user>:<password>@your-rds-instance.region.rds.amazonaws.com:5432/artoo
```

Start all services:
```bash
docker compose up -d
```

### 2b. Laptop / Local Development

Leave `DATABASE_URL` as the default in `.env.example` — the laptop override
provides a local PostgreSQL container automatically.

```bash
docker compose -f docker-compose.yml -f docker-compose.laptop.yml up -d
```

### 3. Verify

| Service    | URL                          | Purpose               |
|------------|------------------------------|-----------------------|
| Dashboard  | http://localhost:8501         | KPI cards, run history |
| Metrics API| http://localhost:8080/docs    | Swagger UI            |
| Health     | http://localhost:8080/health  | Liveness check        |

Check logs:
```bash
docker compose logs -f artoo_scheduler
```

---

## Services

| Container          | Role                                      |
|--------------------|-------------------------------------------|
| `artoo_scheduler`  | Polls Jira, runs the full agent pipeline  |
| `artoo_metrics`    | FastAPI metrics server (port 8080)        |
| `artoo_dashboard`  | Streamlit dashboard UI (port 8501)        |
| `postgres`         | Local PostgreSQL (laptop mode only)       |

---

## Common Operations

**Process a single ticket manually:**
```bash
docker compose exec artoo_scheduler python main.py --mode single --ticket PROJ-123
```

**Dry run (no Jira comments, no GitHub PRs):**
```bash
docker compose exec artoo_scheduler python main.py --mode single --ticket PROJ-123 --dry-run
```

**View current metrics:**
```bash
docker compose exec artoo_scheduler python main.py --mode metrics
```

**Stop all services:**
```bash
docker compose down
```

**Stop and remove all data (laptop mode):**
```bash
docker compose -f docker-compose.yml -f docker-compose.laptop.yml down -v
```

---

## Updating

When Telomere provides a new Docker image:

```bash
docker compose pull
docker compose up -d
```

Your `.env` and database are preserved across updates.
