import hashlib
import re
from typing import Any
from app.schemas import Chunk

def _tokens(text: str) -> int: return max(1, len(text) // 4)

def _split_long(section: str, target_tokens: int) -> list[str]:
    paragraphs = [p for p in re.split(r"\n\s*\n", section) if p.strip()]
    groups, current = [], []
    for paragraph in paragraphs:
        if current and _tokens("\n\n".join(current + [paragraph])) > target_tokens and paragraph.count("```") % 2 == 0:
            groups.append("\n\n".join(current)); current = []
        current.append(paragraph)
    if current: groups.append("\n\n".join(current))
    return groups

def chunk_markdown(metadata: dict[str, Any], content: str, target_tokens: int = 550) -> list[Chunk]:
    matches = list(re.finditer(r"^(#{1,3})\s+(.+)$", content, re.MULTILINE)); sections = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        sections.append((match.group(2).strip(), content[match.start():end].strip()))
    if not sections: sections = [(metadata.get("title", "Document"), content)]
    chunks = []
    for section_title, section in sections:
        for part in _split_long(section, target_tokens):
            stable = hashlib.sha1(f"{metadata['document_id']}:{section_title}:{part}".encode()).hexdigest()[:12]
            env, tags = metadata.get("environment", []), metadata.get("tags", [])
            chunks.append(Chunk(chunk_id=f"CHK-{stable}", document_id=str(metadata["document_id"]), title=str(metadata.get("title", metadata["document_id"])), section_title=section_title, text=part, document_type=str(metadata.get("document_type", "product_doc")), service=str(metadata.get("service", "platform")), version=str(metadata.get("version", "")), updated_at=str(metadata.get("updated_at", "")), environment=env if isinstance(env, list) else [str(env)], tags=tags if isinstance(tags, list) else [str(tags)], publisher=str(metadata.get("publisher", "")), source_url=str(metadata.get("source_url", ""))))
    return chunks
