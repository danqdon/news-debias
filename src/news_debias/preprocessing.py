import re

from news_debias.models import Article, Sentence


_SENTENCE_PATTERN = re.compile(r"\S.*?(?:[.!?](?=\s|$)|$)", re.DOTALL)


class ArticlePreprocessor:
    def process(self, text: str) -> Article:
        self._validate_text(text)
        return Article(text=text, sentences=self._sentences_from_text(text))

    def _validate_text(self, text: str) -> None:
        if not text or text.isspace():
            raise ValueError("Input text must not be empty or whitespace-only")

    def _sentences_from_text(self, text: str) -> tuple[Sentence, ...]:
        return tuple(
            self._sentence_from_match(match, text)
            for match in _SENTENCE_PATTERN.finditer(text)
        )

    def _sentence_from_match(self, match: re.Match[str], text: str) -> Sentence:
        start_offset = match.start()
        end_offset = match.end()
        while text[end_offset - 1].isspace():
            end_offset -= 1

        return Sentence(
            text=text[start_offset:end_offset],
            start_offset=start_offset,
            end_offset=end_offset,
        )
