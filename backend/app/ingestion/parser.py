import re
from pathlib import Path
from typing import Any

def _scalar(value: str) -> Any:
    value = value.strip().strip('"').strip("'")
    if value.startswith("[") and value.endswith("]"):
        return [x.strip().strip('"').strip("'") for x in value[1:-1].split(",") if x.strip()]
    return value

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"): return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3: return {}, text
    metadata: dict[str, Any] = {}
    for line in parts[1].splitlines():
        if ":" in line and not line.lstrip().startswith("-"):
            key, value = line.split(":", 1); metadata[key.strip()] = _scalar(value)
    return metadata, parts[2].strip()

def parse_markdown(path: Path) -> tuple[dict[str, Any], str]:
    metadata, content = parse_frontmatter(path.read_text(encoding="utf-8"))
    metadata.setdefault("document_id", path.stem.upper())
    metadata.setdefault("title", re.sub(r"[-_]", " ", path.stem).title())
    metadata.setdefault("source_path", str(path))
    return metadata, content
