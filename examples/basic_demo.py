from news_debias import ArticleAnalyzer


def main() -> None:
    text = (
        "Experts say the project will cost €12 million. "
        "According to the report, analysts believe the final cost could reach €15 million. "
        "Officials claim the plan is affordable, while critics argue the estimate is unrealistic."
    )
    analysis = ArticleAnalyzer().analyze(text)

    print("Sentences")
    print("---------")
    for index, sentence in enumerate(analysis.article.sentences):
        print(f"[{index}] {sentence.text}")

    print()
    print("Numerical expressions")
    print("---------------------")
    for expression in analysis.numerical_expressions:
        print(
            f"{expression.text} | sentence={expression.sentence_index} | offsets={expression.start_offset}:{expression.end_offset}"
        )

    print()
    print("Vague attributions")
    print("------------------")
    for attribution in analysis.vague_attributions:
        print(
            f"{attribution.text} | sentence={attribution.sentence_index} | offsets={attribution.start_offset}:{attribution.end_offset}"
        )


if __name__ == "__main__":
    main()
