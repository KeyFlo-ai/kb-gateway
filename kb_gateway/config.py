"""Environment configuration (no secrets in repo)."""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_LC_REPO = "/root/langchain-course"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8790

# Collaborator-safe Pinecone namespaces (fail-closed whitelist)
ALLOWED_NAMESPACES = frozenset({"patterns", "course-transcripts", "langchain-docs"})


def langchain_course_repo() -> Path:
    return Path(os.environ.get("LANGCHAIN_COURSE_REPO", DEFAULT_LC_REPO))


def gateway_host() -> str:
    return os.environ.get("KB_GATEWAY_HOST", DEFAULT_HOST)


def gateway_port() -> int:
    return int(os.environ.get("KB_GATEWAY_PORT", str(DEFAULT_PORT)))


def api_token() -> str | None:
    return os.environ.get("KB_GATEWAY_API_TOKEN") or None


def public_url() -> str:
    return os.environ.get("KB_GATEWAY_PUBLIC_URL", f"http://{gateway_host()}:{gateway_port()}")
