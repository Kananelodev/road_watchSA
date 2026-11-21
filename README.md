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

## Testing

[`test_scenarios.md`](test_scenarios.md) has 4 multi-turn scenarios with expected-behaviour checklists:

1. Vague resident report (Soweto)
2. Contractor triaging a batch of 6 messy complaints, with 2 crews
3. Emergency sinkhole + unsafe DIY + off-topic request
4. Sesotho-speaking resident (Bloemfontein)

Run them by hand in AI Studio, or automatically:

```bash
pip install google-genai
export GEMINI_API_KEY=your_key_here
python run_scenarios.py        # all scenarios
python run_scenarios.py 2      # just one
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

## Future ideas

- WhatsApp front end (where residents already complain)
- Photo-based size estimation with Gemini vision
- Push reports to a Google Sheet / Maps layer for a live pothole heatmap
- Ward-level dashboards for councillors

## Team

_add names here_
