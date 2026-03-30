# Copyright (c) 2025-2026 Telomere LLC. All rights reserved.
# Proprietary and confidential. See LICENSE file in the project root.

"""
Cython compilation manifest for Artoo.

Used inside the Docker build stage to compile .py modules to .so binaries.
Do NOT run this directly — it is invoked by the Dockerfile.

Files that MUST stay as .py (not compiled):
  - main.py           : Entry point, subprocess spawning, thin launcher
  - dashboard.py      : Streamlit requires source introspection
  - metrics/server.py : Uvicorn string import "metrics.server:app"
"""

import os
from pathlib import Path

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

# Files that must NOT be compiled
KEEP_AS_PYTHON = {
    "main.py",
    "dashboard.py",
    os.path.join("metrics", "server.py"),
}

SRC_DIR = Path(".")


def collect_extensions() -> list[Extension]:
    """Find all .py files to compile, excluding entry points."""
    extensions = []

    for py_file in SRC_DIR.rglob("*.py"):
        relative = py_file.relative_to(SRC_DIR)
        relative_str = str(relative).replace("\\", "/")

        # Skip entry points that must stay as .py
        if str(relative) in KEEP_AS_PYTHON:
            continue

        # Skip setup.py itself
        if relative.name == "setup.py":
            continue

        # Skip __init__.py — keep as empty .py for package discovery
        if relative.name == "__init__.py":
            continue

        # Convert path to dotted module name
        module_name = str(relative.with_suffix("")).replace(os.sep, ".").replace("/", ".")

        extensions.append(Extension(module_name, [str(relative)]))

    return extensions


extensions = collect_extensions()

print(f"[CYTHON] Compiling {len(extensions)} modules:")
for ext in sorted(extensions, key=lambda e: e.name):
    print(f"  -> {ext.name}")
print()

setup(
    name="artoo",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
            "boundscheck": False,
            "wraparound": False,
        },
        nthreads=os.cpu_count() or 4,
    ),
    packages=find_packages(),
)
