# RoadWatch SA 🚧

An AI agent built in **Google AI Studio** that turns messy pothole complaints into structured, prioritised repair reports for South African municipalities and independent road contractors.

Built for the **GDG Johannesburg Buildathon**.

## The problem

Potholes are an everyday South African problem: burst tyres, damaged rims, accidents, and taxis swerving into oncoming lanes. Residents complain on WhatsApp groups and social media, but those complaints are vague ("massive hole near the Engen"), duplicated, and hard to act on. Road crews and contractors can't tell which hole to fix first.

## The solution

RoadWatch SA works in two modes:

| Mode | Who | What it does |
|---|---|---|
| **Resident** | Motorists, taxi drivers, pedestrians, ward committees | Asks a few smart follow-up questions (in their language) and produces a complete, structured report with a severity and priority score. |
| **Responder** | Municipal officials, councillors, contractors | Takes a batch of messy complaints, merges duplicates, scores and ranks them, clusters nearby jobs for one crew trip, and flags missing info. |

Every report comes out as **JSON**, so it can go straight into a tracker, spreadsheet or GIS map.

## How the system instructions are structured

See [`system_instructions.md`](system_instructions.md).

- **Persona:** practical, local, brief; understands SA terms ("robot", "kombi", ward numbers, landmarks).
- **Constraints:** never invents reference numbers or repair dates, safety-first emergency handling (112 / 10177), no unsafe DIY, privacy (no ID or home addresses), stays on topic, no political blame.
- **Output format:** Summary → JSON report → Next steps for residents; ranked table + clustering + JSON + data gaps for responders.
- **Transparent scoring:** a documented 0–100 priority formula (severity, traffic, vulnerable locations like schools and clinics, hidden hazards, repeat reports).
- **Multilingual:** English, isiZulu, Sesotho, Setswana, isiXhosa, Afrikaans, Sepedi. JSON field names stay in English.

## Security & POPIA

See [`SECURITY_AND_POPIA.md`](SECURITY_AND_POPIA.md).

- **Two layers of guardrails:** a highest-priority GUARDRAILS section in the system instructions, plus `guardrails.py`, which blocks prompt injection and unsafe requests and redacts personal info and secrets in code before anything reaches Gemini.
- **No exposed keys:** the key is read only from `GEMINI_API_KEY`; `.env` is git-ignored; `check_secrets.py` scans the repo on every push (GitHub Actions).
- **POPIA:** anonymous by default, contact details only with explicit consent, other people's details stripped, nothing stored, users can ask for removal.
- **Optional:** Google Search grounding (`--ground`) for verifiable, cited answers.

## Testing

[`test_scenarios.md`](test_scenarios.md) has 5 multi-turn scenarios with expected-behaviour checklists:

1. Vague resident report (Soweto)
2. Contractor triaging a batch of 6 messy complaints, with 2 crews
3. Emergency sinkhole + unsafe DIY + off-topic request
4. Sesotho-speaking resident (Bloemfontein)
5. Guardrails & POPIA: prompt injection, infrastructure theft, personal data, consent

Run them by hand in AI Studio, or automatically:

```bash
pip install google-genai
export GEMINI_API_KEY=your_key_here   # never commit this
python run_scenarios.py               # all scenarios
python run_scenarios.py 5             # just one
python run_scenarios.py --ground      # with Google Search grounding
python guardrails.py                  # guardrail self-test
python check_secrets.py               # scan for exposed API keys
```

Transcripts are saved to `test_results/`.

## Setup in Google AI Studio

1. Go to [aistudio.google.com](https://aistudio.google.com) → **Create new prompt** (Chat).
2. Paste the contents of `system_instructions.md` (below the line) into **System instructions**.
3. Set temperature to around **0.4** for consistent reports.
4. Run the 3+ scenarios from `test_scenarios.md`.
5. Click **Save**, name it `RoadWatch SA`, and add the share link below.

**AI Studio prompt link:** _add after saving_

## Buildathon checklist

- [x] Clear persona, constraints and output format in System Instructions
- [ ] Tested with at least 3 realistic multi-turn scenarios (see `test_results/`)
- [ ] Prompt saved in Google AI Studio
- [x] Input guardrails + enforced system instructions
- [x] No API key in prompts, shared links or client-side code (`check_secrets.py`)
- [x] POPIA: no personal info collected or stored without consent
- [x] (Extra) Search grounding option

## Future ideas

- WhatsApp front end (where residents already complain)
- Photo-based size estimation with Gemini vision
- Push reports to a Google Sheet / Maps layer for a live pothole heatmap
- Ward-level dashboards for councillors

## Team

_add names here_
