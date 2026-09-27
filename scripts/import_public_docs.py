"""Import a small, attributed set of openly licensed official operations docs."""
from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "raw" / "external"

SOURCES = [
    {
        "id": "EXT-PG-001",
        "title": "PostgreSQL 17 — Connections and Authentication",
        "publisher": "PostgreSQL Global Development Group",
        "url": "https://www.postgresql.org/docs/17/runtime-config-connection.html",
        "service": "database",
        "tags": ["postgresql", "connections", "configuration"],
        "license": "PostgreSQL License",
    },
    {
        "id": "EXT-K8S-001",
        "title": "Kubernetes — Deployments and Rollbacks",
        "publisher": "Kubernetes Authors",
        "url": "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/",
        "service": "platform",
        "tags": ["kubernetes", "deployment", "rollback"],
        "license": "CC BY 4.0",
    },
    {
        "id": "EXT-K8S-002",
        "title": "Kubernetes — Debug Running Pods",
        "publisher": "Kubernetes Authors",
        "url": "https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/",
        "service": "platform",
        "tags": ["kubernetes", "pods", "debugging"],
        "license": "CC BY 4.0",
    },
    {
        "id": "EXT-REDIS-001",
        "title": "Redis — Diagnosing Latency Issues",
        "publisher": "Redis documentation contributors",
        "url": "https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/",
        "service": "cache",
        "tags": ["redis", "latency", "troubleshooting"],
        "license": "BSD-3-Clause",
    },
    {
        "id": "EXT-REDIS-002",
        "title": "Redis — Latency Monitoring",
        "publisher": "Redis documentation contributors",
        "url": "https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency-monitor/",
        "service": "cache",
        "tags": ["redis", "monitoring", "latency"],
        "license": "BSD-3-Clause",
    },
    {
        "id": "EXT-KAFKA-001",
        "title": "Apache Kafka — Operations Monitoring",
        "publisher": "Apache Software Foundation",
        "url": "https://kafka.apache.org/43/operations/monitoring/",
        "service": "event-streaming",
        "tags": ["kafka", "consumer-lag", "monitoring"],
        "license": "Apache-2.0",
    },
]


class TextExtractor(HTMLParser):
    SKIP = {"script", "style", "nav", "footer", "svg", "noscript"}
    BLOCK = {"h1", "h2", "h3", "h4", "p", "li", "pre", "code", "table", "tr", "div"}

    def __init__(self) -> None:
        super().__init__()
        self.depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in self.SKIP:
            self.depth += 1
        if self.depth == 0 and tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP and self.depth:
            self.depth -= 1
        if self.depth == 0 and tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.depth == 0:
            self.parts.append(data)

    def text(self) -> str:
        raw = html.unescape(" ".join(self.parts))
        lines = [re.sub(r"\s+", " ", line).strip() for line in raw.splitlines()]
        lines = [line for line in lines if len(line) > 2]
        return "\n\n".join(lines)


def fetch(url: str) -> str:
    import requests

    response = requests.get(url, headers={"User-Agent": "ResolveAI public-doc importer/1.0"}, timeout=30)
    response.raise_for_status()
    return response.text


def import_docs() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        parser = TextExtractor()
        parser.feed(fetch(source["url"]))
        body = parser.text()
        if len(body.split()) < 250:
            raise RuntimeError(f"Source returned too little usable text: {source['url']}")
        frontmatter = f'''---
document_id: {source['id']}
title: {source['title']}
document_type: public_reference
service: {source['service']}
version: current
product: upstream-technology
created_at: 2026-09-25
updated_at: 2026-09-25
environment: [staging, production]
tags: [{", ".join(source['tags'])}]
publisher: {source['publisher']}
source_url: {source['url']}
license: {source['license']}
---

# {source['title']}

> Official upstream documentation imported for operational reference. Always verify the linked current documentation before making production changes.

**Publisher:** {source['publisher']}  
**Official source:** {source['url']}  
**License:** {source['license']}

## Imported reference content

'''
        (DEST / f"{source['id'].lower()}.md").write_text(frontmatter + body + "\n", encoding="utf-8")
        print(f"Imported {source['id']}: {len(body.split()):,} words")


if __name__ == "__main__":
    import_docs()
