import re

from news_debias.models import Article, Sentence


_TERMINAL_PUNCTUATION = ".!?"
_SENTENCE_PATTERN = re.compile(r"\S.*?(?:[.!?](?=\s|$)|$)", re.DOTALL)


class ArticlePreprocessor:
    def process(self, text: str) -> Article:
        if not text or text.isspace():
            raise ValueError("Input text must not be empty or whitespace-only")

        sentences: list[Sentence] = []
        for match in _SENTENCE_PATTERN.finditer(text):
            segment = match.group(0)
            trimmed = segment.strip()
            if not trimmed:
                continue

            leading_ws = len(segment) - len(segment.lstrip())
            trailing_ws = len(segment) - len(segment.rstrip())
            start_offset = match.start() + leading_ws
            end_offset = match.end() - trailing_ws

            sentence_text = text[start_offset:end_offset]
            if not sentence_text:
                continue

            if sentence_text[-1] not in _TERMINAL_PUNCTUATION and match.end() < len(
                text
            ):
                continue

            sentences.append(
                Sentence(
                    text=sentence_text,
                    start_offset=start_offset,
                    end_offset=end_offset,
                )
            )

        return Article(text=text, sentences=tuple(sentences))
