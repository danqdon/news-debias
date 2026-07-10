import re

from news_debias.models import Article, NumericalExpression


_NUMBER_PATTERN = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?"
_MAGNITUDE_PATTERN = r"(?:million|billion)"
_NUMERICAL_EXPRESSION_PATTERN = re.compile(
    rf"""
    (?<!\w)(
        [€$£]{_NUMBER_PATTERN}(?:\s+{_MAGNITUDE_PATTERN})?
        |
        {_NUMBER_PATTERN}%
        |
        {_NUMBER_PATTERN}(?:\s+{_MAGNITUDE_PATTERN})?
    )(?!\w)
    """,
    re.VERBOSE | re.IGNORECASE,
)


class NumericalExpressionExtractor:
    def extract(self, article: Article) -> tuple[NumericalExpression, ...]:
        expressions: list[NumericalExpression] = []
        for sentence_index, sentence in enumerate(article.sentences):
            expressions.extend(
                self._expressions_from_sentence(
                    sentence_text=sentence.text,
                    sentence_start_offset=sentence.start_offset,
                    sentence_index=sentence_index,
                )
            )
        return tuple(expressions)

    def _expressions_from_sentence(
        self,
        sentence_text: str,
        sentence_start_offset: int,
        sentence_index: int,
    ) -> list[NumericalExpression]:
        expressions: list[NumericalExpression] = []
        for match in _NUMERICAL_EXPRESSION_PATTERN.finditer(sentence_text):
            start_offset = sentence_start_offset + match.start(1)
            end_offset = sentence_start_offset + match.end(1)
            expressions.append(
                NumericalExpression(
                    text=match.group(1),
                    start_offset=start_offset,
                    end_offset=end_offset,
                    sentence_index=sentence_index,
                )
            )
        return expressions
