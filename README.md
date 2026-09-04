# Building with Claude API

Course notebooks from working through Anthropic's *Building with the Claude API* material. Each notebook is a small, self-contained lesson that builds on the previous one — starting with a single API call and ending with an automated prompt-evaluation pipeline.

All notebooks use the [`anthropic`](https://pypi.org/project/anthropic/) Python SDK with `claude-sonnet-4-5`.

## Setup

Requires Python 3.9+ and an [Anthropic API key](https://console.anthropic.com/settings/keys).

```bash
git clone https://github.com/goran-paunovic/Building-with-Claude-API.git
cd Building-with-Claude-API

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install anthropic python-dotenv jupyter
```

Copy the example env file and add your key:

```bash
cp .env.example .env           # Windows: copy .env.example .env
```

```
ANTHROPIC_API_KEY=sk-ant-...
```

`.env` is gitignored and never committed. Every notebook picks the key up automatically:

```python
from dotenv import load_dotenv
load_dotenv(override=True)

from anthropic import Anthropic
client = Anthropic()           # reads ANTHROPIC_API_KEY from the environment
```

Then launch Jupyter and open any lesson:

```bash
jupyter notebook
```

> **Note:** running these notebooks makes real API calls and will consume credits. The evaluation lessons (11–14) call the API once per test case — plus a second time per case for model-based grading — so they are the most expensive to run.

## Lessons

### Fundamentals

| Notebook | Topic | What it covers |
| --- | --- | --- |
| [`lesson03.ipynb`](lesson03.ipynb) | First API call | `client.messages.create()`, the `messages` list, reading `message.content[0].text` |
| [`lesson04.ipynb`](lesson04.ipynb) | Multi-turn conversations | `add_user_message` / `add_assistant_message` / `chat` helpers; keeping history so follow-up questions have context |
| [`lesson05.ipynb`](lesson05.ipynb) | System prompts | Passing a `system` parameter to steer behaviour — same question answered with and without a "patient math tutor" persona |
| [`lesson06.ipynb`](lesson06.ipynb) | Temperature | Comparing `temperature=0.0` (focused, repeatable) against `temperature=1.0` (varied) on a creative prompt |
| [`lesson07.ipynb`](lesson07.ipynb) | Streaming | `client.messages.stream()`, iterating `stream.text_stream` for token-by-token output, then `get_final_message()` |

The helper trio introduced in lesson 04 is carried forward and extended in every later notebook — lesson 05 adds `system`, lesson 06 adds `temperature`, lesson 11 adds `stop_sequences`.

### Prompt evaluation

Lessons 11–14 build one pipeline incrementally: generate a dataset, run a prompt against it, then grade the results.

| Notebook | Topic | What it covers |
| --- | --- | --- |
| [`lesson11.ipynb`](lesson11.ipynb) | Generating an eval dataset | Prompting Claude to produce test cases for AWS-related Python/JSON/Regex tasks; assistant prefill plus `stop_sequences=["```"]` to get clean JSON back; saves to `lesson11-dataset.json` |
| [`lesson12.ipynb`](lesson12.ipynb) | Eval harness skeleton | `run_prompt` → `run_test_case` → `run_eval` structure, with grading stubbed out at a hardcoded score |
| [`lesson13.ipynb`](lesson13.ipynb) | Model-based grading | `grade_by_model` asks Claude to review each solution and return structured JSON (`strengths`, `weaknesses`, `reasoning`, `score`); reports an average score across the dataset |
| [`lesson14.ipynb`](lesson14.ipynb) | Code-based grading | Adds deterministic syntax validation — `json.loads`, `ast.parse`, `re.compile` — and averages that with the model score for a combined grade |

Lesson 14 also tightens the prompt itself ("Respond only with Python, JSON, or a plain Regex, no commentary"), since the syntax validators need raw output rather than prose with a code block in it.

### Dataset

[`lesson11-dataset.json`](lesson11-dataset.json) is the generated eval set consumed by lessons 12–14. Each entry pairs a task description with the output format expected from it:

```json
{
  "task": "Write a Python function that parses an ARN and returns a dictionary with its components...",
  "format": "python"
}
```

`format` is one of `python`, `json`, or `regex`, and lesson 14's `grade_syntax` dispatches on it to pick the right validator.

## Repository layout

```
.
├── lesson03.ipynb … lesson07.ipynb   # API fundamentals
├── lesson11.ipynb … lesson14.ipynb   # Prompt evaluation pipeline
├── lesson11-dataset.json             # Generated eval dataset
├── .env.example                      # Template for your API key
└── .gitignore
```

Lesson numbering follows the course; the gap between 07 and 11 is where the course covers material without accompanying notebooks.
