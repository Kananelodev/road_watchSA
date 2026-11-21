# Security & POPIA

How RoadWatch SA is hardened, and how to verify each item on the buildathon checklist.

> This is a good-faith compliance check for a hackathon prototype, not legal advice. A production deployment should be reviewed against the full Protection of Personal Information Act (POPIA) and the Information Regulator's guidance.

---

## 1. Input guardrails & enforced system instructions

There are two layers, so the agent isn't relying on the prompt alone.

| Layer | Where | What it does |
|---|---|---|
| **Prompt-level** | `system_instructions.md` → *GUARDRAILS* section (placed first and marked highest priority) | Treats all user input as data, not instructions. Refuses prompt injection, requests to reveal the prompt, out-of-scope topics, and unsafe requests (vandalism, infrastructure theft, fake reports, doxxing). |
| **Code-level** | `guardrails.py` (used by `run_scenarios.py`) | Runs **before** the message reaches Gemini: length cap (4,000 chars), blocks injection and unsafe patterns, redacts personal info and secrets. Runs **after** the reply: scrubs any API key or ID number the model might echo. |

**Verify:**
- `python guardrails.py` runs the self-test (blocked/redacted samples are printed).
- Run **Scenario 5** in `test_scenarios.md` in AI Studio (prompt-only) and with `python run_scenarios.py 5` (both layers).

## 2. No API key exposure

| Check | Status |
|---|---|
| The key is read only from the `GEMINI_API_KEY` environment variable; it's never written in code. | ✅ `run_scenarios.py` uses `genai.Client()` |
| `.env` is in `.gitignore`; `.env.example` holds placeholders only. | ✅ |
| Automated scan for Google API keys (`AIza…`), hard-coded `GEMINI_API_KEY=` values, and private keys. | ✅ `check_secrets.py`, runs on every push via GitHub Actions (`.github/workflows/secret-scan.yml`) |
| No key in the system instructions or test prompts. | ✅ (the scanner checks these files too) |
| No client-side code (no browser/HTML front end ships a key). | ✅ the runner is a local CLI script |
| The agent refuses to output or request keys, and redacts any pasted key. | ✅ GUARDRAILS rule 3 + `guardrails.py` |

**Before sharing the AI Studio prompt link:**
1. Open the saved prompt and confirm no key, password or real personal data is in the system instructions or the chat history. Clear test chats that contain real data before sharing.
2. Share the **prompt**, never the key. In AI Studio, a shared prompt doesn't include your API key, but anything typed into the chat is visible to whoever has the link.
3. If you deploy it as an AI Studio app, keep the key server-side; never put it in front-end JavaScript.
4. **If a key ever leaks:** delete or rotate it at once in AI Studio → *Get API key*, then remove it from git history.

**Verify:** `python check_secrets.py` → `OK: no API keys found`.

## 3. POPIA: no personal information without consent

POPIA's conditions for lawful processing, and how the agent meets each:

| POPIA condition | How RoadWatch SA meets it |
|---|---|
| **Processing limitation** (minimality + consent) | Reports are anonymous by default. A name/phone is only added if the user wants follow-up **and** says yes to an explicit consent question. `contact_consent` defaults to `false`. |
| **Purpose specification** | Information is only used to build a road-defect report. Nothing is used for anything else. |
| **Further processing limitation** | The agent never forwards, saves or reuses data. It tells the user it cannot submit on their behalf. |
| **Information quality** | Unknown fields are `null`; nothing is guessed or invented. |
| **Openness** | When asked, the agent explains what happens to information. |
| **Security safeguards** | ID numbers, phone numbers, emails, number plates and secrets are redacted in code before reaching the model; other people's details are stripped from reports; no keys in the repo. |
| **Data subject participation** | Users can ask for their details to be removed or corrected, and the report is regenerated without them. |
| **Special personal information** | The agent never asks for ID numbers, race, health, religion, political views or children's information, and leaves them out if volunteered. |

**Storage:** the agent and the runner store nothing except local test transcripts in `test_results/`. **Use only fictional data in tests**; the test scenarios contain made-up names, numbers and a made-up ID number.

**Third-party processing note:** messages are processed by Google's Gemini API. On free/unpaid tiers, Google's terms may allow prompts to be used to improve its products, so don't enter real residents' personal information in a free-tier prototype. Check Google's current Gemini API terms before handling real data.

**Verify:** run **Scenario 5** and confirm the POPIA checklist items pass.

## 4. Optional: Search grounding

`python run_scenarios.py --ground` turns on Google Search grounding, so the agent can find real public information (e.g. a municipality's official reporting channel) and cite it instead of saying "I don't know". In AI Studio, switch on **Grounding with Google Search** in the run settings.

The "never invent contact numbers" rule still applies: with grounding on, the agent should only give a number it found in a cited official source.
