from pathlib import Path


def read_simple_yaml(path: Path) -> dict[str, str | list[str]]:
    data: dict[str, str | list[str]] = {}
    current_key: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            value = line[4:].strip()
            existing = data.setdefault(current_key, [])
            if isinstance(existing, list):
                existing.append(value)
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            data[key] = [] if value == "" else value
    return data
