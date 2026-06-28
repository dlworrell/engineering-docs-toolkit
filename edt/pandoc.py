import shutil
import subprocess
from pathlib import Path


def pandoc_available() -> bool:
    return shutil.which("pandoc") is not None


def run_pandoc(source: Path, target: Path) -> bool:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        return False
    subprocess.run([pandoc, str(source), "-o", str(target)], check=True)
    return True
