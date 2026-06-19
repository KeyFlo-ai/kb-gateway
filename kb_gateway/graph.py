"""Read-only Neo4j queries for the learning knowledge graph."""

from __future__ import annotations

import os
import re

LANE_KEYWORDS: dict[str, list[str]] = {
    "copy": ["copy", "headline", "storytelling", "persuasion", "email", "writing"],
    "design": ["design", "creative", "image", "visual", "scroll", "contrast", "canva", "photoshop"],
    "campaign": ["campaign", "ad set", "budget", "audience", "targeting", "objective", "facebook"],
    "tracking": ["conversion", "tracking", "pixel", "remarketing", "attribution", "landing page"],
}

WRITE_PATTERN = re.compile(r"\b(CREATE|MERGE|DELETE|SET|REMOVE|DROP)\b", re.I)


def _assert_read_only(cypher: str) -> None:
    if WRITE_PATTERN.search(cypher):
        raise ValueError("read-only violation: write keyword in Cypher")


def _run(cypher: str, **params) -> list[dict]:
    _assert_read_only(cypher)
    from neo4j import GraphDatabase, READ_ACCESS

    uri = os.environ.get("LEARNING_KG_NEO4J_URI")
    user = os.environ.get("LEARNING_KG_NEO4J_USER")
    password = os.environ.get("LEARNING_KG_NEO4J_PASSWORD")
    missing = [k for k, v in {
        "LEARNING_KG_NEO4J_URI": uri,
        "LEARNING_KG_NEO4J_USER": user,
        "LEARNING_KG_NEO4J_PASSWORD": password,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"Missing Neo4j env: {', '.join(missing)}")

    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        with driver.session(default_access_mode=READ_ACCESS) as session:
            return [r.data() for r in session.run(cypher, **params)]


def corpus_stats() -> dict:
    rows = _run("""
CALL () { MATCH (c:Course) RETURN count(c) AS courses }
CALL () { MATCH (l:Lecture) RETURN count(l) AS lectures }
CALL () { MATCH (t:Topic) WHERE NOT t:Admin RETURN count(t) AS topics }
CALL () { MATCH (d:Discipline) RETURN count(d) AS disciplines }
CALL () { MATCH (cl:Claim) RETURN count(cl) AS claims }
RETURN courses, lectures, topics, disciplines, claims
    """.strip())
    return rows[0] if rows else {}


def topics_for_keywords(keywords: list[str], limit: int = 12) -> list[dict]:
    return _run("""
MATCH (l:Lecture)-[:COVERS]->(t:Topic)
WHERE NOT t:Admin AND any(kw IN $kws WHERE toLower(t.label) CONTAINS kw)
RETURN t.domain AS domain, t.label AS topic,
       count(DISTINCT l) AS lectures, count(DISTINCT l.course) AS courses
ORDER BY lectures DESC LIMIT $limit
    """.strip(), kws=keywords, limit=limit)


def marketing_disputes(min_conf: float = 0.6, limit: int = 8) -> list[dict]:
    return _run("""
MATCH (a:Claim)-[r:CONTRADICTS]->(b:Claim)
WHERE a.course <> b.course AND r.confidence >= $min_conf
  AND (a.domain IN ['marketing','sales'] OR b.domain IN ['marketing','sales'])
RETURN r.confidence AS confidence, a.course AS course_a, a.statement AS claim_a,
       b.course AS course_b, b.statement AS claim_b, r.explanation AS why
ORDER BY r.confidence DESC LIMIT $limit
    """.strip(), min_conf=min_conf, limit=limit)
