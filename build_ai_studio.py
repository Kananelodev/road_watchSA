"""Build the single text block to paste into Google AI Studio's System Instructions.

    python build_ai_studio.py   ->  ai_studio/system_instructions_full.txt

It joins the system instructions with the reference JSON files, so the agent has
the reference data even without uploading files.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent


def system_instructions() -> str:
    text = (ROOT / "system_instructions.md").read_text(encoding="utf-8")
    return re.split(r"^---\s*$", text, maxsplit=1, flags=re.M)[-1].strip()


def reference_block() -> str:
    parts = ["=== REFERENCE DATA ==="]
    for f in sorted((ROOT / "reference").glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        parts.append(f"--- {f.name} ---\n{json.dumps(data, ensure_ascii=False, separators=(',', ':'))}")
    return "\n\n".join(parts)


def full_prompt() -> str:
    return f"{system_instructions()}\n\n{reference_block()}\n"


if __name__ == "__main__":
    out = ROOT / "ai_studio" / "system_instructions_full.txt"
    out.parent.mkdir(exist_ok=True)
    out.write_text(full_prompt(), encoding="utf-8")
    print(f"Wrote {out} ({len(out.read_text()):,} chars)")
