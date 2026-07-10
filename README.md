# news-debias

news-debias is an exploratory Python project intended to study how different news sources present similar events by comparing claims, framing choices, omissions, numerical statements, and language.

The project is currently in an early experimental stage, and the focus is on building and validating a small, reliable foundation before adding analysis features.

## Setup (uv)

```bash
uv sync
```

## Commands

Install dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest
```

Run Ruff linting:

```bash
uv run ruff check .
```

Run Ruff formatting check:

```bash
uv run ruff format --check .
```

## Initial roadmap

1. Define a very small first analysis experiment.
2. Test structured article and claim representations.
3. Build a minimal interface only after the analysis proves useful.
