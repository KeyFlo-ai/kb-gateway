"""Bootstrap langchain-course imports (shared runtime for vector + router)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .config import langchain_course_repo

_booted = False


def ensure_langchain_course() -> Path:
    """Add langchain-course to path and load env. Idempotent."""
    global _booted
    repo = langchain_course_repo()
    if not repo.is_dir():
        raise RuntimeError(
            f"langchain-course not found at {repo}. "
            "Clone okrealai/langchain-course or set LANGCHAIN_COURSE_REPO."
        )
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))
    if str(repo / "eval" / "graph") not in sys.path:
        sys.path.insert(0, str(repo / "eval" / "graph"))
    if str(repo / "graph") not in sys.path:
        sys.path.insert(0, str(repo / "graph"))

    if not _booted:
        import bootstrap  # noqa: WPS433 — langchain-course module

        bootstrap.load_env()
        _booted = True
    return repo
