from spacy import Language

from src.common.project_types import Chapter, QuoteItem, RawChapter, Speaker
from src.common.utils import prep_document_for_quote_detection
from src.preprocess.chapter_processor.join_quotes_with_narrative import join_quotes_with_narrative
from src.preprocess.quote_finder.quote_finder import find_quotes


def assign_unique_speakers(all_speakers: list[str]) -> list[Speaker]:
    unique_speakers = list(dict.fromkeys(all_speakers))
    return [Speaker(idx + 1, speaker) for idx, speaker in enumerate(unique_speakers)]


def map_speakers_to_ids(speakers_with_ids: list[Speaker]) -> dict[str, int]:
    return {speaker.name: speaker.id for speaker in speakers_with_ids}


def replace_speaker_names_with_ids(chapters: list[Chapter], speaker_mapping: dict[str, int]) -> None:
    for chapter in chapters:
        for item in chapter.items:
            if isinstance(item, QuoteItem):
                speaker_name = item.speaker
                if speaker_name:
                    item.speaker_id = speaker_mapping.get(speaker_name)
                    del item.speaker


def process_chapters(nlp: Language, raw_chapters: list[RawChapter]) -> tuple[list[Chapter], list[Speaker]]:
    all_speakers = []
    chapters: list[Chapter] = []

    for chapter_id, raw_chapter in enumerate(raw_chapters):
        prepared_text = prep_document_for_quote_detection(raw_chapter.text)
        text_doc = nlp(prepared_text)
        quotes = find_quotes(text_doc)
        join_result = join_quotes_with_narrative(quotes, text_doc)
        chapters.append(Chapter(chapter_id, raw_chapter.title, join_result.get("items")))
        all_speakers.extend(join_result.get("speakers"))

    speakers_with_ids = assign_unique_speakers(all_speakers)
    speaker_mapping = map_speakers_to_ids(speakers_with_ids)
    replace_speaker_names_with_ids(chapters, speaker_mapping)

    return chapters, speakers_with_ids
