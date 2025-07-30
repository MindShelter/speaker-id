from pathlib import Path

import typer

from scripts.utils.common import save_object_to_file
from scripts.utils.prepare_text_item_for_llm_processing import prepare_text_items_for_llm_training
from src.common.project_types import LLMTextItem, Speaker, TextMeta
from src.common.utils import process_book_title, read_json_file
from src.models.nlp.init_model import init_model


def process_text_meta_for_training_set(*, text_meta_path: Path, text_meta_output_path: Path) -> None:
    nlp = init_model("en_core_web_lg")
    text_meta = TextMeta.from_dict(read_json_file(text_meta_path))

    training_set: list[LLMTextItem] = []
    speakers: dict[int, Speaker] = {speaker.id: speaker for speaker in text_meta.speakers}

    for chapter in text_meta.chapters:
        training_set.extend(
            prepare_text_items_for_llm_training(nlp=nlp, items=chapter.items, speakers=speakers, char_limit=1000)
        )

    save_object_to_file(
        text_meta_output_path,
        Path(process_book_title(text_meta.title)).with_suffix(".json"),
        text_meta,
    )


app = typer.Typer(add_completion=False, help="Process text meta for training set")

TEXT_META_OPTION = typer.Option(
    None,
    "--text-meta",
    help="Existing text_meta JSON",
)
OUTPUT_OPTION = typer.Option(..., "-o", "--output", help="Directory for the resulting JSON")


@app.command()
def run(
    text_meta: Path | None = TEXT_META_OPTION,
    output: Path = OUTPUT_OPTION,
) -> None:
    if text_meta is None:
        print("❌  Provide --text-meta.[/]")
        raise typer.Exit(1)

    process_text_meta_for_training_set(text_meta_path=text_meta, text_meta_output_path=output)
    print(f"✅  Done. Results saved to {output}[/]")


if __name__ == "__main__":
    app()




