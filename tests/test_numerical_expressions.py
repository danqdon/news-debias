from pathlib import Path

from news_debias import ArticlePreprocessor, NumericalExpressionExtractor


def _extract(text: str):
    article = ArticlePreprocessor().process(text)
    expressions = NumericalExpressionExtractor().extract(article)
    return article, expressions


def test_extracts_euro_million_from_fixture_with_offsets_and_sentence_index() -> None:
    text = Path("tests/fixtures/sample_article.txt").read_text(encoding="utf-8")
    article, expressions = _extract(text)

    target = next(
        expression for expression in expressions if expression.text == "€12 million"
    )

    assert target.text == "€12 million"
    assert article.text[target.start_offset : target.end_offset] == target.text
    assert target.sentence_index == 1


def test_extracts_multiple_expressions_in_single_sentence_in_order() -> None:
    article, expressions = _extract("Revenue reached $1,500, then 12.5% and 2 billion.")

    assert [expression.text for expression in expressions] == [
        "$1,500",
        "12.5%",
        "2 billion",
    ]
    assert [expression.sentence_index for expression in expressions] == [0, 0, 0]
    for expression in expressions:
        assert (
            article.text[expression.start_offset : expression.end_offset]
            == expression.text
        )


def test_expressions_in_later_sentence_have_correct_absolute_offsets() -> None:
    article, expressions = _extract("No numbers here. Then 42% and 1,500 appear.")

    assert [expression.text for expression in expressions] == ["42%", "1,500"]
    assert [expression.sentence_index for expression in expressions] == [1, 1]
    for expression in expressions:
        assert (
            article.text[expression.start_offset : expression.end_offset]
            == expression.text
        )
        assert expression.start_offset >= article.sentences[1].start_offset


def test_extracts_percentages() -> None:
    _, expressions = _extract("Approval was 42% and later 12.5%.")

    assert [expression.text for expression in expressions] == ["42%", "12.5%"]


def test_extracts_decimal_values() -> None:
    _, expressions = _extract("The score moved from 12.5 to 13.0.")

    assert [expression.text for expression in expressions] == ["12.5", "13.0"]


def test_extracts_grouped_values() -> None:
    _, expressions = _extract("Population rose to 1,500 and then 2,000.")

    assert [expression.text for expression in expressions] == ["1,500", "2,000"]


def test_extracts_currency_with_supported_symbols() -> None:
    _, expressions = _extract("Costs were $1,500, €12, and £12.5.")

    assert [expression.text for expression in expressions] == ["$1,500", "€12", "£12.5"]


def test_includes_magnitude_word_with_number_and_currency() -> None:
    _, expressions = _extract("The budget is €12 million and debt is 2 billion.")

    assert [expression.text for expression in expressions] == [
        "€12 million",
        "2 billion",
    ]


def test_returns_empty_tuple_when_no_expressions_exist() -> None:
    _, expressions = _extract("No quantitative claims are present in this text.")

    assert expressions == ()


def test_currency_symbol_without_number_is_not_extracted() -> None:
    _, expressions = _extract("The report used $ and € symbols only.")

    assert expressions == ()


def test_does_not_produce_overlapping_duplicate_results() -> None:
    _, expressions = _extract("The estimate is €12 million.")

    assert [expression.text for expression in expressions] == ["€12 million"]
    assert len({(e.start_offset, e.end_offset) for e in expressions}) == len(
        expressions
    )
