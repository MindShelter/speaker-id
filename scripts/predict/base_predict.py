from pathlib import Path

from spacy import Language

from scripts.types.config_types import MainScriptsConfig
from scripts.utils.common import save_object_to_file
from scripts.utils.prepare_text_item_for_llm_processing import prepare_text_for_prediction
from src.common.constants import EMPTY_SPEAKER_NAME
from src.common.project_types import Chapter, QuoteItem, TextMeta
from src.common.utils import process_book_title, read_json_file
from src.metrics.metrics import elapsed_time
from src.models.llm_clients.base import BaseLLMClient
from src.preprocess.chapter_processor.chapter_processor import (
    assign_unique_speakers,
    map_speakers_to_ids,
    process_chapters,
    replace_speaker_names_with_ids,
)
from src.preprocess.document_reader.document_reader import read_document


def process_chapter(
    *,
    nlp: Language,
    llm: BaseLLMClient,
    chapter: Chapter,
    config: MainScriptsConfig,
) -> list[str]:
    predicted_speakers: list[str] = []

    for idx, item in enumerate(chapter.items):
        if not isinstance(item, QuoteItem):
            continue

        text_for_llm = prepare_text_for_prediction(nlp=nlp, item_idx=idx, items=chapter.items, char_limit=1000)
        predicted_speaker_name = llm.chat_completion(config.llm_prompt, text_for_llm)
        if predicted_speaker_name is None:
            predicted_speaker_name = EMPTY_SPEAKER_NAME

        processed_speaker_name = predicted_speaker_name.strip().capitalize()
        item.speaker = processed_speaker_name
        predicted_speakers.append(processed_speaker_name)

    return predicted_speakers


def get_text_meta(nlp: Language, config: MainScriptsConfig) -> TextMeta:
    if config.text_path is not None:
        book_title, raw_chapters = read_document(config.text_path)
        chapters, speakers = process_chapters(nlp, raw_chapters)
        return TextMeta(book_title, chapters, speakers)

    return TextMeta.from_dict(read_json_file(config.text_meta_path))


def predict_speakers(config: MainScriptsConfig) -> None:
    nlp = config.nlp
    llm = config.llm
    text_meta = get_text_meta(nlp, config)

    predicted_speakers: list[str] = []
    current_chapter_title: str | None = None

    try:
        for chapter in text_meta.chapters:
            current_chapter_title = chapter.title
            with elapsed_time(f"Chapter {current_chapter_title}", enabled=config.enable_timing_logs):
                speakers = process_chapter(nlp=nlp, llm=llm, chapter=chapter, config=config)
                predicted_speakers.extend(speakers)

    except Exception as e:
        print(f"Error processing chapter {current_chapter_title or '<unknown>'}: {e}")
        raise
    finally:
        speakers_with_ids = assign_unique_speakers(predicted_speakers)
        replace_speaker_names_with_ids(text_meta.chapters, map_speakers_to_ids(speakers_with_ids))
        text_meta.speakers = speakers_with_ids
        save_object_to_file(
            config.text_meta_output_path,
            Path(process_book_title(text_meta.title)).with_suffix(".json"),
            text_meta,
        )

