import json
from pathlib import Path


def write_manifest(output: Path, data: dict) -> Path:
    output.mkdir(parents=True, exist_ok=True)
    path = output / "build-manifest.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path
