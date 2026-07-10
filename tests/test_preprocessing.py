from pathlib import Path

import pytest

from news_debias import ArticlePreprocessor


def _fixture_text() -> str:
    return Path("tests/fixtures/sample_article.txt").read_text(encoding="utf-8")


def test_fixture_produces_expected_sentences() -> None:
    article = ArticlePreprocessor().process(_fixture_text())

    expected = [
        "The city council approved the new transport plan on Tuesday.",
        "Officials said the project would cost €12 million.",
        "Several residents welcomed the proposal, but others called it unnecessary.",
        "Will the changes reduce traffic?",
        "Construction is expected to begin in September!",
    ]

    assert len(article.sentences) == 5
    assert [sentence.text for sentence in article.sentences] == expected


def test_offsets_match_original_text_and_increase() -> None:
    article = ArticlePreprocessor().process(_fixture_text())

    previous_end = -1
    for sentence in article.sentences:
        assert (
            article.text[sentence.start_offset : sentence.end_offset] == sentence.text
        )
        assert sentence.start_offset >= previous_end
        assert sentence.end_offset > sentence.start_offset
        previous_end = sentence.end_offset


def test_blank_lines_do_not_become_sentences() -> None:
    article = ArticlePreprocessor().process("First.\n\n\nSecond!")

    assert [sentence.text for sentence in article.sentences] == ["First.", "Second!"]


def test_surrounding_whitespace_is_excluded_from_sentence_text() -> None:
    article = ArticlePreprocessor().process(
        "  First sentence.   \n  Second sentence?   "
    )

    assert [sentence.text for sentence in article.sentences] == [
        "First sentence.",
        "Second sentence?",
    ]


def test_punctuation_is_preserved() -> None:
    article = ArticlePreprocessor().process("Wait! Really? Yes.")

    assert [sentence.text for sentence in article.sentences] == [
        "Wait!",
        "Really?",
        "Yes.",
    ]


def test_empty_text_raises_value_error() -> None:
    with pytest.raises(ValueError):
        ArticlePreprocessor().process("")


def test_whitespace_only_text_raises_value_error() -> None:
    with pytest.raises(ValueError):
        ArticlePreprocessor().process("   \n\t  ")


def test_final_sentence_without_terminal_punctuation_is_returned() -> None:
    article = ArticlePreprocessor().process("First sentence. Final sentence")

    assert [sentence.text for sentence in article.sentences] == [
        "First sentence.",
        "Final sentence",
    ]
