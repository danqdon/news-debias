from news_debias.extractors.numerical_expressions import NumericalExpressionExtractor
from news_debias.models import ArticleAnalysis
from news_debias.preprocessing import ArticlePreprocessor


class ArticleAnalyzer:
    def analyze(self, text: str) -> ArticleAnalysis:
        article = ArticlePreprocessor().process(text)
        numerical_expressions = NumericalExpressionExtractor().extract(article)
        return ArticleAnalysis(
            article=article,
            numerical_expressions=numerical_expressions,
        )
