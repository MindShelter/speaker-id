from pathlib import Path

from scripts.types.config_types import MainScriptsConfig
from scripts.utils.common import found_speaker, generate_statistics, is_speaker_presents_in_text, save_object_to_file
from scripts.utils.prepare_text_item_for_llm_processing import prepare_text_for_evaluation
from src.common.constants import EMPTY_SPEAKER_NAME
from src.common.project_types import QuoteItem, Speaker, TextMeta
from src.common.utils import process_book_title, read_json_file
from src.metrics.metric_types import IncorrectPrediction
from src.metrics.metrics import compute_metrics, display_metrics, elapsed_time
from src.preprocess.chapter_processor.chapter_processor import (
    map_speakers_to_ids,
    replace_speaker_names_with_ids,
)


def evaluate_speakers(config: MainScriptsConfig) -> None:
    nlp = config.nlp
    llm = config.llm

    text_meta = TextMeta.from_dict(read_json_file(config.text_meta_path))

    next_speaker_id = 0
    predicted_speakers: dict[int, Speaker] = {}
    true_speakers: dict[int, Speaker] = {speaker.id: speaker for speaker in text_meta.speakers}

    true_labels: list[str] = []
    pred_labels: list[str] = []
    chapters = [text_meta.chapters[1]]
    test_chapters = chapters[0:1]
    incorrect_predictions: list[IncorrectPrediction] = []
    for chapter in test_chapters:
        try:
            with elapsed_time(f"Chapter {chapter.title}", enabled=config.enable_timing_logs):
                for idx, item in enumerate(chapter.items):
                    if not isinstance(item, QuoteItem):
                        continue

                    text_for_llm = prepare_text_for_evaluation(
                        nlp=nlp, item_idx=idx, items=chapter.items, char_limit=1000
                    )
                    predicted_speaker_name = llm.chat_completion(config.llm_prompt, text_for_llm)

                    if predicted_speaker_name is None:
                        predicted_speaker_name = EMPTY_SPEAKER_NAME

                    if is_speaker_presents_in_text(predicted_speaker_name, text_for_llm):
                        predicted_speaker = found_speaker(predicted_speaker_name, predicted_speakers)

                        if predicted_speaker is None:
                            predicted_speaker = Speaker(next_speaker_id, predicted_speaker_name)
                            next_speaker_id += 1
                            predicted_speakers[predicted_speaker.id] = predicted_speaker

                    true_speaker = true_speakers.get(item.speaker_id)
                    true_speaker_name = true_speaker.name if true_speaker and true_speaker.name else EMPTY_SPEAKER_NAME
                    true_labels.append(true_speaker_name)
                    pred_labels.append(predicted_speaker_name)

                    if predicted_speaker_name != true_speaker_name:
                        incorrect_predictions.append(
                            IncorrectPrediction(
                                text=item.content,
                                true_label=true_speaker_name,
                                predicted_label=predicted_speaker_name,
                                text_for_llm=text_for_llm,
                            )
                        )

        except Exception as e:
            print(f"Error processing chapter {chapter.title}: {e}")
            save_object_to_file(
                config.text_meta_output_path,
                Path(process_book_title(text_meta.title) + "_meta").with_suffix(".json"),
                text_meta,
            )
            raise

    text_meta.speakers = list(predicted_speakers.values())
    replace_speaker_names_with_ids(text_meta.chapters, map_speakers_to_ids(text_meta.speakers))

    save_object_to_file(
        config.text_meta_output_path,
        Path(process_book_title(text_meta.title) + "_meta").with_suffix(".json"),
        text_meta,
    )

    metrics = compute_metrics(true_labels, pred_labels)
    display_metrics(metrics, incorrect_predictions)

    statistics = generate_statistics(
        metrics=metrics,
        incorrect_predictions=incorrect_predictions,
        input_config=config,
    )
    save_object_to_file(
        config.text_meta_output_path,
        Path(process_book_title(text_meta.title) + "_statistics").with_suffix(".json"),
        statistics,
    )
