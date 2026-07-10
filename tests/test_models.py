from dataclasses import FrozenInstanceError

import pytest

from news_debias import Article, NumericalExpression, Sentence


def test_sentence_is_immutable() -> None:
    sentence = Sentence(text="Example.", start_offset=0, end_offset=8)

    with pytest.raises(FrozenInstanceError):
        sentence.text = "Changed."


def test_article_is_immutable() -> None:
    article = Article(
        text="Example.",
        sentences=(Sentence(text="Example.", start_offset=0, end_offset=8),),
    )

    with pytest.raises(FrozenInstanceError):
        article.text = "Changed"


def test_article_sentences_is_tuple() -> None:
    article = Article(
        text="One. Two.",
        sentences=(
            Sentence(text="One.", start_offset=0, end_offset=4),
            Sentence(text="Two.", start_offset=5, end_offset=9),
        ),
    )

    assert isinstance(article.sentences, tuple)


def test_numerical_expression_is_immutable() -> None:
    expression = NumericalExpression(
        text="€12 million",
        start_offset=10,
        end_offset=21,
        sentence_index=0,
    )

    with pytest.raises(FrozenInstanceError):
        expression.text = "€13 million"
