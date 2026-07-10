import re

from news_debias.models import Article, Sentence, VagueAttribution


_ACTOR_FRAGMENT = r"(?:some experts|some officials|many experts|many observers|unnamed sources|anonymous sources|unnamed officials|experts|sources|critics|observers|analysts|officials|insiders|commentators|researchers)"
_ATTRIBUTION_VERB_FRAGMENT = r"(?:say|said|claim|claimed|argue|argued|suggest|suggested|believe|believed|warn|warned|report|reported|indicate|indicated)"
_VAGUE_ATTRIBUTION_PATTERN = re.compile(
    rf"(?:{_ACTOR_FRAGMENT})\s+(?:{_ATTRIBUTION_VERB_FRAGMENT})(?!\w)",
    re.IGNORECASE,
)


class VagueAttributionExtractor:
    def extract(self, article: Article) -> tuple[VagueAttribution, ...]:
        attributions: list[VagueAttribution] = []
        for sentence_index, sentence in enumerate(article.sentences):
            attributions.extend(
                self._attributions_from_sentence(
                    sentence=sentence,
                    sentence_index=sentence_index,
                )
            )
        return tuple(attributions)

    def _attributions_from_sentence(
        self,
        sentence: Sentence,
        sentence_index: int,
    ) -> list[VagueAttribution]:
        match = _VAGUE_ATTRIBUTION_PATTERN.match(sentence.text)
        if match is None:
            return []

        start_offset = sentence.start_offset + match.start()
        end_offset = sentence.start_offset + match.end()
        return [
            VagueAttribution(
                text=match.group(),
                start_offset=start_offset,
                end_offset=end_offset,
                sentence_index=sentence_index,
            )
        ]
