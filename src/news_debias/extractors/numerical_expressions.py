import re

from news_debias.models import Article, NumericalExpression, Sentence


_NUMBER_FRAGMENT = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?"
_MAGNITUDE_FRAGMENT = r"(?:million|billion)"
_NUMERICAL_EXPRESSION_PATTERN = re.compile(
    rf"""
    (?<!\w)(?:
        [€$£]{_NUMBER_FRAGMENT}(?:\s+{_MAGNITUDE_FRAGMENT})?
        |
        {_NUMBER_FRAGMENT}%
        |
        {_NUMBER_FRAGMENT}(?:\s+{_MAGNITUDE_FRAGMENT})?
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
                    sentence=sentence,
                    sentence_index=sentence_index,
                )
            )
        return tuple(expressions)

    def _expressions_from_sentence(
        self,
        sentence: Sentence,
        sentence_index: int,
    ) -> list[NumericalExpression]:
        expressions: list[NumericalExpression] = []
        for match in _NUMERICAL_EXPRESSION_PATTERN.finditer(sentence.text):
            start_offset = sentence.start_offset + match.start()
            end_offset = sentence.start_offset + match.end()
            expressions.append(
                NumericalExpression(
                    text=match.group(),
                    start_offset=start_offset,
                    end_offset=end_offset,
                    sentence_index=sentence_index,
                )
            )
        return expressions
