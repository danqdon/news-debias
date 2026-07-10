from news_debias import ArticlePreprocessor, VagueAttributionExtractor


def _extract(text: str):
    article = ArticlePreprocessor().process(text)
    attributions = VagueAttributionExtractor().extract(article)
    return article, attributions


def test_extracts_experts_say() -> None:
    _, attributions = _extract("Experts say the policy will reduce costs.")

    assert [attribution.text for attribution in attributions] == ["Experts say"]


def test_extracts_experts_said_in_short_sentence() -> None:
    _, attributions = _extract("Experts said.")

    assert [attribution.text for attribution in attributions] == ["Experts said"]


def test_matching_is_case_insensitive_and_preserves_original_casing() -> None:
    _, attributions = _extract("EXPERTS SAID the policy will reduce costs.")

    assert [attribution.text for attribution in attributions] == ["EXPERTS SAID"]


def test_extracts_past_tense_verbs() -> None:
    _, attributions = _extract("Critics argued that the proposal was unfair.")

    assert [attribution.text for attribution in attributions] == ["Critics argued"]


def test_extracts_multi_word_actor_phrase() -> None:
    _, attributions = _extract("Many observers believe the decision was political.")

    assert [attribution.text for attribution in attributions] == [
        "Many observers believe"
    ]


def test_extracts_unnamed_officials_suggested_as_one_phrase() -> None:
    _, attributions = _extract(
        "Unnamed officials suggested that changes were imminent."
    )

    assert [attribution.text for attribution in attributions] == [
        "Unnamed officials suggested"
    ]


def test_extracts_attribution_in_middle_of_sentence() -> None:
    _, attributions = _extract(
        "According to the report, experts say the proposal may reduce costs."
    )

    assert [attribution.text for attribution in attributions] == ["experts say"]


def test_extracts_two_attributions_in_one_sentence() -> None:
    _, attributions = _extract(
        "Experts say prices will fall, while critics argue the plan is risky."
    )

    assert [attribution.text for attribution in attributions] == [
        "Experts say",
        "critics argue",
    ]


def test_returns_matches_in_article_order() -> None:
    _, attributions = _extract(
        "Experts say the policy will change. According to the note, analysts believe it will pass. Officials claim the policy is affordable, while critics argue the estimate is unrealistic."
    )

    assert [attribution.text for attribution in attributions] == [
        "Experts say",
        "analysts believe",
        "Officials claim",
        "critics argue",
    ]


def test_later_sentence_offsets_are_article_relative() -> None:
    article, attributions = _extract(
        "No attribution here. Sources claimed talks resumed."
    )

    assert [attribution.text for attribution in attributions] == ["Sources claimed"]
    attribution = attributions[0]
    assert attribution.start_offset >= article.sentences[1].start_offset
    assert (
        article.text[attribution.start_offset : attribution.end_offset]
        == attribution.text
    )


def test_returns_correct_zero_based_sentence_index() -> None:
    _, attributions = _extract("No attribution here. Experts say changes are coming.")

    assert attributions[0].sentence_index == 1


def test_slicing_invariant_holds_for_each_result() -> None:
    article, attributions = _extract(
        "Experts say this will work, while critics argue it is risky. Sources claim updates are pending."
    )

    for attribution in attributions:
        assert (
            article.text[attribution.start_offset : attribution.end_offset]
            == attribution.text
        )


def test_named_individual_is_not_extracted() -> None:
    _, attributions = _extract("Dr. Smith said the policy will reduce costs.")

    assert attributions == ()


def test_named_organization_is_not_extracted() -> None:
    _, attributions = _extract("The Ministry of Finance reported the figures.")

    assert attributions == ()


def test_reuters_reported_is_not_extracted() -> None:
    _, attributions = _extract("Reuters reported that negotiations had resumed.")

    assert attributions == ()


def test_returns_empty_tuple_when_no_vague_attributions_exist() -> None:
    _, attributions = _extract("The report includes detailed named citations.")

    assert attributions == ()


def test_does_not_match_non_configured_actor_prefixes() -> None:
    _, attributions = _extract(
        "The experts say the policy will reduce costs. Government officials said the policy will reduce costs. Reuters sources said the policy will reduce costs."
    )

    assert attributions == ()


def test_does_not_match_actor_followed_by_modifier_before_verb() -> None:
    _, attributions = _extract(
        "Experts from the university say the policy will reduce costs."
    )

    assert attributions == ()


def test_does_not_match_officials_with_intervening_modifier() -> None:
    _, attributions = _extract(
        "Officials at the ministry said the policy will reduce costs."
    )

    assert attributions == ()


def test_does_not_match_sources_with_intervening_modifier() -> None:
    _, attributions = _extract(
        "Sources close to the minister said the policy will reduce costs."
    )

    assert attributions == ()


def test_matches_some_experts_at_sentence_start() -> None:
    _, attributions = _extract("Some experts say the policy will reduce costs.")

    assert [attribution.text for attribution in attributions] == ["Some experts say"]
