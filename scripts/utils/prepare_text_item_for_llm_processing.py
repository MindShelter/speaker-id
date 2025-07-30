from spacy import Language

from src.common.project_types import LLMTextItem, NarrationItem, Speaker, TextItemEnum, TextItemType


def normalize_fragments(direction: str, fragments: list[TextItemType]) -> list[TextItemType]:
    if direction == "before":
        fragments.reverse()
    return fragments


def gather_fragments(
    *,
    nlp: Language,
    quote_index: int,
    items: list[TextItemType],
    direction: str,
    char_limit: int,
) -> list[TextItemType]:
    indices = range(quote_index - 1, -1, -1) if direction == "before" else range(quote_index + 1, len(items))

    collected_fragments: list[TextItemType] = []
    total_char_count = 0

    for idx in indices:
        item = items[idx]

        if total_char_count >= char_limit:
            break

        if item.type in (TextItemEnum.NEXT_LINE, TextItemEnum.QUOTE):
            item_length = len(item.content)
            collected_fragments.append(item)
            total_char_count += item_length
            continue

        doc = nlp(item.content)
        sentences = list(doc.sents)

        if direction == "before":
            sentences.reverse()

        for sent in sentences:
            sent_text = sent.text
            sent_len = len(sent_text)
            if total_char_count + sent_len <= char_limit:
                frag = NarrationItem(content=sent_text)
                collected_fragments.append(frag)
                total_char_count += sent_len
            else:
                return normalize_fragments(direction, collected_fragments)

    return normalize_fragments(direction, collected_fragments)


def format_fragment_deprecated(fragment: TextItemType, speakers: dict[int, Speaker]) -> str:
    if fragment.type == TextItemEnum.QUOTE and getattr(fragment, "speaker_id", None) is not None:
        spk = speakers.get(fragment.speaker_id)
        if spk and spk.name:
            return f"[{spk.name}]{fragment.content}[/{spk.name}]"
    return fragment.content


def format_fragment(fragment: TextItemType) -> str:
    return fragment.content


def prepare_text_for_evaluation(*, nlp: Language, item_idx: int, items: list[TextItemType], char_limit: int) -> str:
    item = items[item_idx]
    before_fragments = gather_fragments(
        nlp=nlp, quote_index=item_idx, items=items, direction="before", char_limit=char_limit
    )
    after_fragments = gather_fragments(
        nlp=nlp, quote_index=item_idx, items=items, direction="after", char_limit=char_limit
    )
    before_context = "".join(format_fragment(frag) for frag in before_fragments)
    after_context = "".join(format_fragment(frag) for frag in after_fragments)
    return f"{before_context}[SPEAKER]{item.content}[/SPEAKER]{after_context}"


def prepare_text_for_prediction(*, nlp: Language, item_idx: int, items: list[TextItemType], char_limit: int) -> str:
    item = items[item_idx]
    before_fragments = gather_fragments(
        nlp=nlp, quote_index=item_idx, items=items, direction="before", char_limit=char_limit
    )
    after_fragments = gather_fragments(
        nlp=nlp, quote_index=item_idx, items=items, direction="after", char_limit=char_limit
    )
    before_context = "".join(frag.content for frag in before_fragments)
    after_context = "".join(frag.content for frag in after_fragments)
    return f"{before_context}[SPEAKER]{item.content}[/SPEAKER]{after_context}"


def prepare_text_items_for_llm_training(
    *,
    nlp: Language,
    items: list[TextItemType],
    speakers: dict[int, Speaker],
    char_limit: int,
) -> list[LLMTextItem]:
    results = []
    current_text_item_id = 0

    for i, item in enumerate(items):
        if item.type != "quote":
            continue

        before_fragments = gather_fragments(
            nlp=nlp, quote_index=i, items=items, direction="before", char_limit=char_limit
        )
        after_fragments = gather_fragments(
            nlp=nlp, quote_index=i, items=items, direction="after", char_limit=char_limit
        )
        before_context = "".join(format_fragment(frag) for frag in before_fragments)
        after_context = "".join(format_fragment(frag) for frag in after_fragments)

        speaker = speakers.get(item.speaker_id)
        speaker_name = speaker.name if speaker and speaker.name else "Undefined Speaker"

        snippet = f"{before_context}[SPEAKER]{item.content}[/SPEAKER]{after_context}"
        results.append(LLMTextItem(current_text_item_id, snippet, speaker_name))
        current_text_item_id += 1

    return results
