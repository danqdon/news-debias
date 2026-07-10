from dataclasses import dataclass


@dataclass(frozen=True)
class Sentence:
    text: str
    start_offset: int
    end_offset: int


@dataclass(frozen=True)
class Article:
    text: str
    sentences: tuple[Sentence, ...]


@dataclass(frozen=True)
class NumericalExpression:
    text: str
    start_offset: int
    end_offset: int
    sentence_index: int


@dataclass(frozen=True)
class ArticleAnalysis:
    article: Article
    numerical_expressions: tuple[NumericalExpression, ...]
