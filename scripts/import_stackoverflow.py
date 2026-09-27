"""Import a reproducible, attributed real-world troubleshooting corpus.

The importer uses the public Stack Exchange API and stores selected Stack
Overflow questions with their accepted answers as local Markdown documents.
Only posts licensed under CC BY-SA 4.0 are selected.
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "raw" / "stackoverflow"
MANIFEST = ROOT / "data" / "real" / "stackoverflow_manifest.json"
API = "https://api.stackexchange.com/2.3"
LICENSE_CUTOFF = 1525219200  # 2018-05-02: Stack Overflow contributions use CC BY-SA 4.0.
TARGETS = {
    "stripe-payments": "payments",
    "paypal": "payments",
    "payment-gateway": "payments",
    "checkout": "commerce",
    "javascript": "frontend",
    "reactjs": "frontend",
    "cors": "api",
    "rest": "api",
    "node.js": "backend",
    "authentication": "identity",
    "oauth-2.0": "identity",
    "docker": "containers",
    "nginx": "web-server",
    "postgresql": "database",
    "kubernetes": "platform",
    "redis": "cache",
    "apache-kafka": "event-streaming",
}
PER_TAG = 12


class MarkdownParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.in_pre = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "pre":
            self.in_pre = True
            self.parts.append("\n```\n")
        elif tag in {"p", "div", "blockquote", "br", "h1", "h2", "h3"}:
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "code" and not self.in_pre:
            self.parts.append("`")
        elif tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.parts.append("[")

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre":
            self.in_pre = False
            self.parts.append("\n```\n")
        elif tag in {"p", "div", "blockquote", "li", "h1", "h2", "h3"}:
            self.parts.append("\n")
        elif tag == "code" and not self.in_pre:
            self.parts.append("`")
        elif tag == "a":
            self.parts.append("]")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def markdown(self) -> str:
        text = unescape("".join(self.parts)).replace("\xa0", " ")
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def to_markdown(value: str) -> str:
    parser = MarkdownParser()
    parser.feed(value)
    return parser.markdown()


def api_get(path: str, **params: object) -> list[dict]:
    response = requests.get(f"{API}/{path}", params={"site": "stackoverflow", **params}, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if payload.get("backoff"):
        time.sleep(int(payload["backoff"]))
    return payload.get("items", [])


def iso_date(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()


def safe(value: str) -> str:
    return value.replace("\r", " ").replace("\n", " ").replace('"', "'").strip()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    selected_by_id: dict[int, tuple[str, str, dict]] = {}
    for tag, service in TARGETS.items():
        questions = api_get(
            "questions",
            tagged=tag,
            pagesize=50,
            order="desc",
            sort="votes",
            fromdate=LICENSE_CUTOFF,
            filter="withbody",
        )
        accepted = [q for q in questions if q.get("accepted_answer_id") and q.get("body") and q.get("score", 0) >= 2]
        for question in accepted[:PER_TAG]:
            selected_by_id.setdefault(question["question_id"], (tag, service, question))

    selected = list(selected_by_id.values())
    answer_ids = [str(question["accepted_answer_id"]) for _, _, question in selected]
    answers = []
    for start in range(0, len(answer_ids), 80):
        answers.extend(api_get(f"answers/{';'.join(answer_ids[start:start+80])}", pagesize=100, filter="withbody"))
    answers_by_id = {answer["answer_id"]: answer for answer in answers}
    manifest: list[dict] = []

    for tag, service, question in selected:
        answer = answers_by_id.get(question["accepted_answer_id"])
        if not answer:
            continue
        question_id = question["question_id"]
        document_id = f"SO-{question_id}"
        title = safe(unescape(question["title"]))
        question_author = safe(question.get("owner", {}).get("display_name", "Stack Overflow contributor"))
        answer_author = safe(answer.get("owner", {}).get("display_name", "Stack Overflow contributor"))
        source_url = question["link"]
        tags = ", ".join(safe(item) for item in question.get("tags", []))
        body = f'''---
document_id: {document_id}
title: "{title}"
document_type: community_support
service: {service}
version: community
product: public-technical-support
created_at: {iso_date(question["creation_date"])}
updated_at: {iso_date(question.get("last_activity_date", question["creation_date"]))}
environment: [public]
tags: [{tags}]
publisher: Stack Overflow
source_url: {source_url}
license: CC BY-SA 4.0
author: "{question_author}"
answer_author: "{answer_author}"
---

# {title}

## Question

{to_markdown(question["body"])}

## Accepted answer

{to_markdown(answer["body"])}

## Source and attribution

This is a real public troubleshooting thread from Stack Overflow. The question was posted by {question_author}; the accepted answer was posted by {answer_author}. It was imported from {source_url} and converted from HTML to Markdown with formatting normalised. The content is available under the Creative Commons Attribution-ShareAlike 4.0 license: https://creativecommons.org/licenses/by-sa/4.0/
'''
        (OUTPUT / f"{document_id.lower()}.md").write_text(body, encoding="utf-8")
        manifest.append({
            "document_id": document_id,
            "question_id": question_id,
            "title": title,
            "tag": tag,
            "source_url": source_url,
            "question_author": question_author,
            "answer_author": answer_author,
            "license": "CC BY-SA 4.0",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
        })

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Imported {len(manifest)} real Stack Overflow question-and-answer records into {OUTPUT}")


if __name__ == "__main__":
    main()
