# Speaker ID

*A Python‑powered pipeline that detects unique speakers in text or books and outputs structured metadata ready for
multi‑voice audiobook generators.*

**Status: early alpha 🚧**
> The project is still experimental and the API will change.  
> If the idea excites you, open an issue or ping me on GitHub.  
> All proposals—features, formats, languages—are welcome!

## Table of Contents

1. [Features](#features)
2. [Quick start & installation](#quick-start)
3. [Input/Output Example](#input--output-example)
4. [Roadmap](#roadmap)

---

## Features

- 🗣️ **Detect speakers** in English text (.txt or .epub)
- 🏷️ **Assign each quote** to the correct speaker ID
- 📦 **Export JSON** ready for multi‑voice TTS / audiobook generators

---

## Quick start

```bash
# 1  Clone and create a virtual environment
git clone https://github.com/your-user/speaker-id.git
cd speaker-id

# 2. Make sure Poetry is installed (https://python-poetry.org/docs/#installation)
#    Then install all runtime + dev dependencies into a fresh virtualenv
poetry install           # add --all-extras if you want to develop
poetry shell             # activates the venv

# 3. (Optional) run with a local LLM
#    Either:
#      a) implement your own wrapper under src/models/llm_clients
#                      –or–
#      b) install the Unsloth for drop‑in usage.
#         See the Unsloth installation guide:
#         https://github.com/unslothai/unsloth
#
# 4. Run on a sample text file
poetry run predict_open_ai --input data/example.txt --o out --timing
```

The command writes `out/example.json`—see the [example](#input--output-example) below.

---

## Input / Output example

**Input** (`example.txt`)

```text
"Hey Bob, did you finish the chapter?" Alice asked.
"Almost there—just decoding the last paragraph," Bob replied, eyes still glued to the screen.
Bob’s eyes darted across the lines as Alice leaned over his shoulder.
"Need any help?" she offered.
"A fresh cup of coffee would help more than anything!" he laughed.
```

**Output** (`example.json`)

```json
{
  "title": "example",
  "speakers": [
    {
      "id": 0,
      "name": "Alice"
    },
    {
      "id": 1,
      "name": "Bob"
    }
  ],
  "chapters": [
    {
      "id": 0,
      "title": "Chapter 1",
      "items": [
        {
          "type": "quote",
          "speaker_id": 0,
          "content": "\"Hey Bob, did you finish the chapter?\""
        },
        {
          "type": "narration",
          "content": "Alice asked"
        },
        {
          "content": "\n",
          "type": "next-line"
        },
        {
          "type": "quote",
          "speaker_id": 1,
          "content": "\"Almost there—just decoding the last paragraph,\""
        },
        {
          "type": "narration",
          "content": " Bob replied, eyes still glued to the screen"
        },
        {
          "content": "\n",
          "type": "next-line"
        },
        {
          "type": "narration",
          "content": "Bob’s eyes darted across the lines as Alice leaned over his shoulder."
        },
        {
          "content": "\n",
          "type": "next-line"
        },
        {
          "type": "quote",
          "speaker_id": 0,
          "content": "\"Need any help?\""
        },
        {
          "type": "narration",
          "content": " she offered."
        },
        {
          "content": "\n",
          "type": "next-line"
        },
        {
          "type": "quote",
          "speaker_id": 1,
          "content": "\"A fresh cup of coffee would help more than anything!\""
        },
        {
          "type": "narration",
          "content": " he laughed."
        }
      ]
    }
  ]
}
```

---

## CLI scripts (Typer‑powered)

All project entry‑points are [Typer](https://typer.tiangolo.com/) apps, so live docs are *always* one flag away.
All available command‑line entry points are listed in **`pyproject.toml`** under `[project.scripts]`.
Append `--help` to any of them to discover their options.

```bash
# See top‑level commands of the predict open ai pipeline
poetry run predict_open_ai --help
```

### Roadmap

Below is the *living* feature list. Checkboxes show completed status; **priorities** are indicated by P‑levels (P1 = top
priority).

|   | Task                                                                                                                                                 | Priority | Status      |
|---|------------------------------------------------------------------------------------------------------------------------------------------------------|----------|-------------|
| ☐ | **Frontend validation UI & dataset builder** – web app for convenient tagging and dataset creation                                                   | **P1**   | Almost done |
| ☐ | **Fine‑tune a local LLM** dedicated to speaker detection for offline use                                                                             | **P1**   | in progress |
| ☐ | **“Golden Speakers” alias resolver** – automatically join short/long names (e.g. “Harry” ⇆ “Harry Potter”)                                           | **P1**   | not started |
| ☐ | **Universal multi‑language layer** – pluggable tokenization & heuristics, with first target packs for **Polish**, **Spanish**, **German**            | **P2**   | not started |
| ☐ | **Em‑dash / dash‑initiated dialogue support** – recognise lines such as `—To be or not to be…` or `- Hello!` as quotes when no “ ” marks are present | **P2**   | not started |
| ☐ | Ingest **pre‑annotated dialogues** (poems, plays like *«Hamlet»*) where speakers are already indicated in the text                                   | **P3**   | not started |
| ☐ | **Chapter segmentation for plain`.txt` and additional e‑book formats (`.fb2`, etc.)** – robust detection of chapter headings and automatic splitting | **P2**   | not started |
| ☐ | Better handling of **first‑person narration** – narrator becomes its own speaker ID                                                                  | **P3**   | not started |
| ☐ | **Character description generator** – summarise role, personality and key traits for every detected speaker                                          | **P4**   | not started |

---
