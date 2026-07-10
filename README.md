# news-debias

news-debias is an exploratory Python project intended to study how different news sources present similar events by comparing claims, framing choices, omissions, numerical statements, and language.

The project is currently in an early experimental stage, and the focus is on building and validating a small, reliable foundation before adding analysis features.

## Current capability

The project currently supports deterministic sentence segmentation and deterministic extraction of basic numerical expressions from manually supplied text. Sentences and extracted expressions keep exact character offsets into the original text so later analysis can attach evidence directly to source spans. The project does not yet evaluate truth, sourcing, bias, or unsupported claims.

```python
from news_debias import ArticleAnalyzer

analysis = ArticleAnalyzer().analyze(
	"Officials said the project would cost €12 million."
)
```

Current analysis output is intentionally narrow: deterministic sentence segmentation, basic numerical-expression extraction, and exact offsets into the source text.

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
