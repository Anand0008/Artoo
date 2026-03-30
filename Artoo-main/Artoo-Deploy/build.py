#!/usr/bin/env python3
# Copyright (c) 2025-2026 Telomere LLC. All rights reserved.
# Proprietary and confidential. See LICENSE file in the project root.

"""
Artoo-Deploy Build Script

Copies source from the Artoo project, applies PostgreSQL patches,
and prepares the src/ directory for Cython compilation inside Docker.

Usage:
    python build.py              # Full build: copy + patch
    python build.py --clean      # Remove src/ and start fresh
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent
ARTOO_SRC = ROOT.parent / "Artoo"
BUILD_DIR = ROOT / "src"

# ── What to copy / exclude ───────────────────────────────────────────────────

EXCLUDE_DIRS = {
    "tests",
    ".claude",
    "__pycache__",
    ".pytest_cache",
    "venv",
    ".venv",
    "data",
    "logs",
    ".git",
    ".idea",
    ".vscode",
    "docker-volumes",
}

EXCLUDE_FILES = {
    "conftest.py",
    "Artoo.md",
    "CLIENT_DEMO_GUIDE.md",
    "github_project_and_confluence_setup_guide.md",
    "Dockerfile",
    "docker-compose.yml",
    ".gitignore",
    ".env",
    "run_output.txt",
    "requirements.in",
}


def clean() -> None:
    """Remove the src/ build directory."""
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print(f"[CLEAN] Removed {BUILD_DIR}")
    else:
        print(f"[CLEAN] {BUILD_DIR} does not exist, nothing to remove")


def copy_source() -> None:
    """Copy Artoo source into src/, excluding non-essential files."""
    if not ARTOO_SRC.exists():
        print(f"[ERROR] Artoo source not found at {ARTOO_SRC}", file=sys.stderr)
        sys.exit(1)

    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    print(f"[COPY] {ARTOO_SRC} -> {BUILD_DIR}")

    def _ignore(directory: str, contents: list[str]) -> set[str]:
        ignored = set()
        dir_name = os.path.basename(directory)

        for item in contents:
            item_path = os.path.join(directory, item)

            # Exclude directories
            if os.path.isdir(item_path) and item in EXCLUDE_DIRS:
                ignored.add(item)
                continue

            # Exclude specific files
            if item in EXCLUDE_FILES:
                ignored.add(item)
                continue

            # Exclude dotfiles/dotfolders (except .env.example)
            if item.startswith(".") and item != ".env.example":
                ignored.add(item)
                continue

        return ignored

    shutil.copytree(ARTOO_SRC, BUILD_DIR, ignore=_ignore)
    print(f"[COPY] Done — {_count_files(BUILD_DIR)} files copied")


def _count_files(path: Path) -> int:
    return sum(1 for _ in path.rglob("*") if _.is_file())


def patch_postgresql() -> None:
    """Patch settings.py and database.py for PostgreSQL instead of SQLite."""
    settings_path = BUILD_DIR / "config" / "settings.py"
    database_path = BUILD_DIR / "persistence" / "database.py"

    # ── Patch settings.py ────────────────────────────────────────────────
    print("[PATCH] config/settings.py — SQLite -> PostgreSQL")
    text = settings_path.read_text(encoding="utf-8")

    # Replace sqlite_db_path with database_url
    text = text.replace(
        '    sqlite_db_path: str = "data/artoo.db"',
        '    database_url: str = "postgresql://<user>:<password>@localhost:5432/artoo"',
    )

    settings_path.write_text(text, encoding="utf-8")

    # ── Patch database.py ────────────────────────────────────────────────
    print("[PATCH] persistence/database.py — SQLite -> PostgreSQL")
    database_path.write_text(
        '''\
# Copyright (c) 2025-2026 Telomere LLC. All rights reserved.
# Proprietary and confidential. See LICENSE file in the project root.

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import settings
from persistence.models import Base


engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db() -> None:
    """Create all tables if they don\'t exist."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db_session() -> Iterator[Session]:
    """Context manager for database sessions with auto-rollback on error."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
''',
        encoding="utf-8",
    )

    # ── Patch requirements.txt — add psycopg2-binary ─────────────────────
    req_path = BUILD_DIR / "requirements.txt"
    if req_path.exists():
        print("[PATCH] requirements.txt — adding psycopg2-binary")
        text = req_path.read_text(encoding="utf-8")
        if "psycopg2" not in text:
            text += "\n# ── PostgreSQL Driver ─────────────────────────────────────────\npsycopg2-binary==2.9.10\n"
            req_path.write_text(text, encoding="utf-8")


def patch_env_example() -> None:
    """Update .env.example to use DATABASE_URL instead of SQLITE_DB_PATH."""
    env_path = BUILD_DIR / ".env.example"
    if not env_path.exists():
        return

    print("[PATCH] .env.example — SQLite -> PostgreSQL")
    text = env_path.read_text(encoding="utf-8")
    text = text.replace(
        "# ── Persistence ──────────────────────────────────────────────\n"
        "SQLITE_DB_PATH=data/artoo.db\n"
        "DB_ECHO=false",
        "# ── Database ─────────────────────────────────────────────────\n"
        "# AWS RDS:   postgresql://<user>:<password>@your-rds-endpoint.amazonaws.com:5432/artoo\n"
        "# Laptop:    leave as-is (docker-compose.laptop.yml provides local PostgreSQL)\n"
        "DATABASE_URL=postgresql://<user>:<password>@postgres:5432/artoo\n"
        "DB_ECHO=false",
    )
    env_path.write_text(text, encoding="utf-8")


def remove_test_dependencies() -> None:
    """Strip test-only packages from requirements.txt."""
    req_path = BUILD_DIR / "requirements.txt"
    if not req_path.exists():
        return

    print("[PATCH] requirements.txt — removing test dependencies")
    lines = req_path.read_text(encoding="utf-8").splitlines()
    filtered = []
    skip_section = False
    test_packages = {"pytest", "pytest-asyncio", "pytest-mock", "moto", "coverage", "responses"}

    for line in lines:
        # Skip the testing section header
        if "── Testing" in line:
            skip_section = True
            continue
        if skip_section and line.strip() == "":
            skip_section = False
            continue
        if skip_section:
            continue
        # Also catch any stray test packages
        if any(line.strip().startswith(pkg) for pkg in test_packages):
            continue
        filtered.append(line)

    req_path.write_text("\n".join(filtered), encoding="utf-8")


def report() -> None:
    """Print summary of build artifacts."""
    py_files = list(BUILD_DIR.rglob("*.py"))
    other_files = [f for f in BUILD_DIR.rglob("*") if f.is_file() and f.suffix != ".py"]

    print()
    print("=" * 60)
    print("  Artoo-Deploy Build Summary")
    print("=" * 60)
    print(f"  Python modules:   {len(py_files)}")
    print(f"  Other files:      {len(other_files)}")
    print(f"  Output directory:  {BUILD_DIR}")
    print()
    print("  Next step: docker compose build")
    print("=" * 60)
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Artoo-Deploy Build Script")
    parser.add_argument("--clean", action="store_true", help="Remove src/ and exit")
    args = parser.parse_args()

    if args.clean:
        clean()
        return

    print()
    print("=" * 60)
    print("  Building Artoo-Deploy")
    print("=" * 60)
    print()

    copy_source()
    patch_postgresql()
    patch_env_example()
    remove_test_dependencies()
    report()


if __name__ == "__main__":
    main()
