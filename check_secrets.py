"""Scan the repo for exposed API keys before committing or sharing.

    python check_secrets.py      # exit code 1 if anything is found

Also runs automatically on every push via .github/workflows/secret-scan.yml.
"""

import re
import subprocess
import sys
from pathlib import Path

PATTERNS = {
    "Google API key": r"AIza[0-9A-Za-z_\-]{35}",
    "Hard-coded GEMINI_API_KEY": r"GEMINI_API_KEY\s*=\s*['\"]?[A-Za-z0-9_\-]{20,}",
    "Private key block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
}
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}


def tracked_files() -> list[Path]:
    try:
        out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True)
        return [Path(p) for p in out.stdout.splitlines()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [p for p in Path(".").rglob("*") if p.is_file() and not SKIP_DIRS & set(p.parts)]


def main() -> int:
    problems = []
    files = tracked_files()
    for f in files:
        if f.name == ".env":
            problems.append(f"{f}: .env file is tracked by git — remove it and rotate the key")
            continue
        if f.name == Path(__file__).name:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for label, pat in PATTERNS.items():
            for m in re.finditer(pat, text):
                line = text.count("\n", 0, m.start()) + 1
                problems.append(f"{f}:{line}: {label}")
    if problems:
        print("Possible secrets found:\n  " + "\n  ".join(problems))
        print("\nRemove them, rotate the key in Google AI Studio, and use environment variables.")
        return 1
    print(f"OK: no API keys found in {len(files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
