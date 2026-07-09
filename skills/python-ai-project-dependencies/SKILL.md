---
name: python-ai-project-dependencies
description: Methodology for choosing, installing, grouping, and validating Python dependencies for AI-assisted or vibe-coding projects. Use this skill whenever the user asks what Python packages to preinstall, which libraries are recommended for AI projects, how to set up a reusable pyproject/requirements stack, how to avoid missing-package warnings, or how to choose dependencies for LLM apps, agents, RAG, data pipelines, FastAPI backends, notebooks, automation, scraping, visualization, testing, or code-quality workflows.
---

# Python AI Project Dependencies

Use this skill to turn "install the useful Python stuff" into a deliberate dependency plan. The goal is not to install everything; it is to pick a reliable base, add project-type extras, keep the environment reproducible, and avoid dependency bloat that makes future Codex work slower or less deterministic.

## Core Principles

- Prefer a local virtual environment or project-scoped dependency manager over global installs.
- Start with a small universal base, then add extras by project type.
- Prefer popular, maintained packages with wheels for the current Python version and platform.
- Avoid heavyweight frameworks until the project actually needs them.
- Do not mix package managers in one project unless the repo already does.
- Pin or lock resolved versions for repeatability, especially before sharing or deployment.
- Keep secrets, `.env` files, virtual environments, caches, datasets, and model artifacts out of Git.
- Treat dependency installation as a change that should be validated with import checks and the repo's tests or smoke commands.

## First Pass: Inspect Before Recommending

Before proposing or installing packages, inspect the project:

1. Look for `pyproject.toml`, `requirements*.txt`, `uv.lock`, `poetry.lock`, `Pipfile`, `setup.py`, `setup.cfg`, `.python-version`, Docker files, and existing `README` setup notes.
2. Identify the package manager already in use:
   - `uv`: prefer `uv add` / `uv sync`.
   - Poetry: prefer `poetry add`.
   - pip-tools: edit `.in` files and compile.
   - plain pip: use `requirements.txt` and optionally `requirements.lock`.
3. Check the Python version and whether packages have wheels for it. Very new Python releases can lag behind scientific and ML packages.
4. Check whether the project is an application, library, notebook workspace, web API, scraper, agent, RAG system, CLI, or automation repo.
5. Check dirty Git state before editing dependency files, and do not overwrite user changes.

## Recommended Baseline

Use this as the default base for general AI-assisted Python projects:

```text
requests
httpx
python-dotenv
PyYAML
pydantic
pydantic-settings
typer
rich
loguru
tenacity
tqdm
pytest
ruff
ipython
```

Why this base works:

- `requests` and `httpx` cover common sync and async HTTP work.
- `python-dotenv`, `PyYAML`, `pydantic`, and `pydantic-settings` cover configuration and validation.
- `typer`, `rich`, `loguru`, `tenacity`, and `tqdm` make CLIs, logs, retries, and progress usable.
- `pytest`, `ruff`, and `ipython` support quick iteration and verification.

Add `black` and `mypy` when the repo already uses formatting or typing gates, or when the user wants stricter engineering hygiene. Do not add them to tiny scripts unless useful.

## Project-Type Extras

Choose extras by the actual workflow. Do not install every group by default.

### Data Work, CSV, Excel, Analysis

```text
numpy
pandas
openpyxl
pyarrow
polars
duckdb
```

Use `pandas` for broad compatibility, `polars` for fast local analytics, `duckdb` for SQL over local files, and `pyarrow` for parquet/Arrow interoperability.

### Visualization And Reporting

```text
matplotlib
plotly
seaborn
altair
jinja2
markdown
```

Use `matplotlib` for reliable static charts, `plotly` for interactive charts, `seaborn` for statistical quick looks, and `jinja2` for HTML or Markdown report generation.

### Web APIs And Services

```text
fastapi
uvicorn
python-multipart
SQLAlchemy
alembic
orjson
redis
celery
```

Use `fastapi` and `uvicorn` for small to medium APIs. Add `SQLAlchemy` and `alembic` when persistence and migrations exist. Add queues or Redis only when there is real background work or cache behavior.

### LLM Apps And Agent Workflows

```text
openai
anthropic
litellm
instructor
json-repair
tiktoken
```

Use official SDKs for provider-specific work. Use `litellm` when the project needs a provider abstraction. Use `instructor` or Pydantic-based parsing when structured model output matters. Use `tiktoken` for token counting where OpenAI-compatible tokenization is relevant.

### RAG, Search, And Vector Work

```text
chromadb
qdrant-client
faiss-cpu
sentence-transformers
rank-bm25
rapidfuzz
unstructured
pypdf
python-docx
```

Prefer the lightest vector backend that matches deployment. Use `qdrant-client` for Qdrant services, `chromadb` for local prototypes, `faiss-cpu` for local vector indexing, and `rank-bm25`/`rapidfuzz` for lexical and fuzzy retrieval baselines. Document loaders should be chosen by source format, not installed blindly.

### Scraping, Public-Web Collection, And Automation

```text
beautifulsoup4
lxml
feedparser
markdownify
selectolax
trafilatura
playwright
aiohttp
```

Use `beautifulsoup4`/`lxml` for HTML parsing, `feedparser` for RSS/Atom, `markdownify` for converting HTML to Markdown, and `trafilatura` for article extraction. Add Playwright only when browser rendering is truly required; it is heavier and needs a browser install step.

### Documents, Images, Audio, And Media

```text
Pillow
opencv-python-headless
pypdf
python-docx
openpyxl
pdfplumber
pydub
moviepy
```

Prefer headless variants for server or automation environments. Add media packages only when the project actually processes those formats, because native dependencies and wheels vary by platform.

### Notebooks And Exploration

```text
jupyterlab
ipykernel
ipywidgets
nbformat
```

Use these for notebook-first workspaces. Avoid adding Jupyter to backend services unless notebooks are part of the repo workflow.

### Databases And Storage Clients

```text
psycopg
asyncpg
pymongo
boto3
supabase
fsspec
s3fs
```

Choose clients based on the actual service. Do not add cloud SDKs as a generic default because they increase dependency surface and often require credentials.

### Testing, Quality, And Developer Tooling

```text
pytest
pytest-asyncio
pytest-cov
ruff
black
mypy
pre-commit
types-requests
```

Use `pytest-asyncio` for async code, `pytest-cov` for coverage gates, and `pre-commit` only if the repo is ready to standardize hooks. Add `types-*` stubs only when type checking complains about specific libraries.

## Dependency Tiers

When creating a reusable setup, organize dependencies into tiers:

- **Base**: small set used by almost every project.
- **Dev**: tests, lint, type checking, notebooks, debugging tools.
- **Feature extras**: `web`, `data`, `rag`, `scraping`, `media`, `llm`, `deploy`.
- **Optional heavy extras**: Playwright, Jupyter, ML frameworks, vector databases, OCR, video/audio tooling.

For `pyproject.toml`, prefer optional dependency groups:

```toml
[project.optional-dependencies]
dev = ["pytest", "ruff", "ipython"]
web = ["fastapi", "uvicorn", "python-multipart"]
data = ["numpy", "pandas", "openpyxl", "pyarrow", "duckdb"]
scraping = ["beautifulsoup4", "lxml", "feedparser", "trafilatura"]
llm = ["openai", "anthropic", "litellm", "instructor"]
rag = ["qdrant-client", "chromadb", "rank-bm25", "rapidfuzz", "pypdf"]
```

## Installation Patterns

Use the existing package manager. Examples:

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade --no-input pip setuptools wheel
.venv/bin/python -m pip install --no-input -r requirements.txt
```

```bash
uv add requests httpx pydantic rich pytest ruff
uv add --dev black mypy
```

```bash
poetry add requests httpx pydantic rich
poetry add --group dev pytest ruff black mypy
```

If using plain pip, keep:

- `requirements.txt` for human-curated top-level requirements.
- `requirements.lock` or a generated freeze file for the exact resolved environment.

## Validation Checklist

After changing dependencies:

1. Run the install command and read stderr if it fails.
2. Run import smoke checks for key packages.
3. Run the smallest relevant test command.
4. Run typecheck, lint, or build commands if the repo already has them.
5. Check `git diff --check`.
6. Confirm no `.env`, virtualenv, cache, model artifact, or dataset was added accidentally.
7. Report packages installed, files changed, commands run, and remaining risk.

Example import smoke:

```bash
python -c "import httpx, pydantic, rich, pytest; print('imports ok')"
```

## Common Pitfalls

- Installing globally and later debugging the wrong interpreter.
- Adding ML/RAG/browser packages before the project needs them.
- Using packages that do not support the current Python release yet.
- Mixing `pip`, `uv`, Poetry, and Conda in one repo.
- Committing `.venv`, caches, notebooks with large outputs, local databases, or credentials.
- Treating an install success as full validation without import checks or tests.
- Hiding install failures behind `|| true`, shell redirection, or incomplete logs.

## Decision Rules

- For a blank AI project, recommend `base + dev`, then ask or infer project-type extras.
- For a repo with existing dependency files, modify the existing dependency system instead of introducing a new one.
- For one-off scripts, prefer `requests`, `rich`, `typer`, `python-dotenv`, and `pytest` before heavier frameworks.
- For backend APIs, prefer `fastapi`, `uvicorn`, `pydantic-settings`, and add database libraries only when persistence is present.
- For data-heavy work, prefer `pandas`, `polars`, `duckdb`, and `openpyxl` before ML frameworks.
- For RAG prototypes, include retrieval baselines (`rank-bm25`, `rapidfuzz`) before committing to a vector database.
- For browser automation, add Playwright only after confirming static HTTP/parsing is insufficient.
