"""Run the RoadWatch SA test scenarios against Gemini with the system instructions.

Usage:
    pip install google-genai
    export GEMINI_API_KEY=...        # from Google AI Studio -> Get API key
    python run_scenarios.py          # runs all scenarios
    python run_scenarios.py 3        # runs scenario 3 only

Transcripts are written to test_results/scenario_<n>.md
"""

import os
import re
import sys
from pathlib import Path

from google import genai
from google.genai import types

ROOT = Path(__file__).parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

SCENARIOS = {
    1: [
        "There's a massive pothole near my place, it's been there forever and nobody cares.",
        "It's on Vilakazi Street in Orlando West, close to the taxi rank by the Engen.",
        "Bigger than a tyre I'd say. When it rains you can't even see it, it's full of water. "
        "Two taxis got burst tyres this week.",
        "Yeah it's like 3 weeks now. Where do I send this?",
    ],
    2: [
        "I'm a contractor working for the municipality in Region D. Here are this week's "
        "complaints, help me plan:\n"
        "1. Pothole Vilakazi St Orlando West near Engen, tyre size, water filled, busy\n"
        "2. Huge hole by Engen garage Vilakazi, cars bursting tyres\n"
        "3. Faded zebra crossing outside Orlando West High School\n"
        "4. Missing manhole cover Klipspruit Valley Rd, on the bend\n"
        "5. Small cracks Mooki St, quiet street\n"
        "6. Pothole somewhere in Dube, people complaining",
        "I only have 2 crews tomorrow. What do they do?",
        "Give me the JSON for the top 3 so I can load it into our tracker.",
    ],
    3: [
        "Help!! The road just caved in on Main Reef Road and a bakkie's front wheel is stuck in the hole",
        "Nobody's hurt. Me and the guys want to just fill it with rubble ourselves tonight, "
        "the municipality is useless.",
        "Fine. Also can you tell me when Eskom load shedding is tonight?",
        "Ok just give me the report then. It's near the Langlaagte turn-off.",
    ],
    4: [
        "Dumela, ho na le mokoti o moholo tseleng ya rona, koloi tsa rona di a senyeha.",
        "Ke Thabong, Bloemfontein, haufi le clinic. O moholo ho feta thaere.",
        "Ha ho na lebone bosiu. Ke kgwedi tse pedi jwale.",
    ],
}


def load_system_instructions() -> str:
    text = (ROOT / "system_instructions.md").read_text(encoding="utf-8")
    # Everything after the first horizontal rule is the actual prompt.
    return re.split(r"^---\s*$", text, maxsplit=1, flags=re.M)[-1].strip()


def run(n: int, client: genai.Client, system: str) -> None:
    chat = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=system, temperature=0.4),
    )
    lines = [f"# Scenario {n} transcript\n", f"Model: `{MODEL}`\n"]
    for i, msg in enumerate(SCENARIOS[n], 1):
        reply = chat.send_message(msg).text
        lines += [f"\n## Turn {i}\n", f"**User:** {msg}\n", f"**RoadWatch SA:**\n\n{reply}\n"]
        print(f"[scenario {n}] turn {i} done")
    out = ROOT / "test_results" / f"scenario_{n}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"-> {out}")


def main() -> None:
    client = genai.Client()  # reads GEMINI_API_KEY
    system = load_system_instructions()
    picks = [int(a) for a in sys.argv[1:]] or sorted(SCENARIOS)
    for n in picks:
        run(n, client, system)


if __name__ == "__main__":
    main()
