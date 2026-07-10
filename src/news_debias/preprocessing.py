import re

from news_debias.models import Article, Sentence


_TERMINAL_PUNCTUATION = ".!?"
_SENTENCE_PATTERN = re.compile(r"\S.*?(?:[.!?](?=\s|$)|$)", re.DOTALL)


class ArticlePreprocessor:
    def process(self, text: str) -> Article:
        self._validate_text(text)
        return Article(text=text, sentences=self._extract_sentences(text))

    def _validate_text(self, text: str) -> None:
        if not text or text.isspace():
            raise ValueError("Input text must not be empty or whitespace-only")

    def _extract_sentences(self, text: str) -> tuple[Sentence, ...]:
        sentences: list[Sentence] = []
        for match in _SENTENCE_PATTERN.finditer(text):
            sentence = self._build_sentence(match, text)
            if sentence is not None:
                sentences.append(sentence)
        return tuple(sentences)

    def _build_sentence(self, match: re.Match[str], text: str) -> Sentence | None:
        start_offset, end_offset = self._trimmed_offsets(match)
        sentence_text = text[start_offset:end_offset]
        if self._is_incomplete_match(sentence_text, match, len(text)):
            return None

        return Sentence(
            text=sentence_text,
            start_offset=start_offset,
            end_offset=end_offset,
        )

    def _trimmed_offsets(self, match: re.Match[str]) -> tuple[int, int]:
        start_offset = match.start()
        end_offset = match.end()
        while match.string[end_offset - 1].isspace():
            end_offset -= 1
        return start_offset, end_offset

    def _is_incomplete_match(
        self,
        sentence_text: str,
        match: re.Match[str],
        text_length: int,
    ) -> bool:
        return (
            sentence_text[-1] not in _TERMINAL_PUNCTUATION and match.end() < text_length
        )
