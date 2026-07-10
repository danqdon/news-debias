from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from news_debias import ArticleAnalysis, ArticleAnalyzer


def _fixture_text() -> str:
    return Path("tests/fixtures/sample_article.txt").read_text(encoding="utf-8")


def test_analyze_returns_article_analysis() -> None:
    analysis = ArticleAnalyzer().analyze(
        "Officials said the project would cost €12 million."
    )

    assert isinstance(analysis, ArticleAnalysis)


def test_analyze_preserves_original_text_and_expected_sentences() -> None:
    text = _fixture_text()
    analysis = ArticleAnalyzer().analyze(text)

    expected_sentences = [
        "The city council approved the new transport plan on Tuesday.",
        "Officials said the project would cost €12 million.",
        "Several residents welcomed the proposal, but others called it unnecessary.",
        "Will the changes reduce traffic?",
        "Construction is expected to begin in September!",
    ]

    assert analysis.article.text == text
    assert [
        sentence.text for sentence in analysis.article.sentences
    ] == expected_sentences


def test_fixture_analysis_contains_euro_million_with_offsets_and_sentence_index() -> (
    None
):
    analysis = ArticleAnalyzer().analyze(_fixture_text())

    expression = next(
        item for item in analysis.numerical_expressions if item.text == "€12 million"
    )

    assert expression.sentence_index == 1
    assert (
        analysis.article.text[expression.start_offset : expression.end_offset]
        == expression.text
    )


def test_analysis_includes_vague_attribution_results() -> None:
    analysis = ArticleAnalyzer().analyze(
        "Experts say the project would cost €12 million."
    )

    assert [item.text for item in analysis.vague_attributions] == ["Experts say"]
    assert analysis.vague_attributions[0].sentence_index == 0
    assert (
        analysis.article.text[
            analysis.vague_attributions[0].start_offset : analysis.vague_attributions[
                0
            ].end_offset
        ]
        == analysis.vague_attributions[0].text
    )


def test_analysis_extracts_middle_and_multiple_vague_attributions() -> None:
    analysis = ArticleAnalyzer().analyze(
        "According to the report, analysts believe the final cost could reach €15 million. Officials claim the plan is affordable, while critics argue the estimate is unrealistic."
    )

    assert [item.text for item in analysis.vague_attributions] == [
        "analysts believe",
        "Officials claim",
        "critics argue",
    ]
    assert [item.sentence_index for item in analysis.vague_attributions] == [0, 1, 1]
    assert [item.text for item in analysis.numerical_expressions] == ["€15 million"]

    for item in analysis.vague_attributions:
        assert analysis.article.text[item.start_offset : item.end_offset] == item.text


def test_analysis_keeps_existing_numerical_expression_results_unchanged() -> None:
    analysis = ArticleAnalyzer().analyze(
        "Officials said the project would cost €12 million."
    )

    assert [item.text for item in analysis.numerical_expressions] == ["€12 million"]


def test_text_without_numerical_expressions_returns_empty_tuple() -> None:
    analysis = ArticleAnalyzer().analyze(
        "No quantitative claims are present in this text."
    )

    assert analysis.numerical_expressions == ()
    assert analysis.vague_attributions == ()


def test_empty_input_raises_value_error() -> None:
    with pytest.raises(ValueError):
        ArticleAnalyzer().analyze("")


def test_article_analysis_is_immutable() -> None:
    analysis = ArticleAnalyzer().analyze(
        "Officials said the project would cost €12 million."
    )

    with pytest.raises(FrozenInstanceError):
        analysis.article = analysis.article
