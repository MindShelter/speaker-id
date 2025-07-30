from pathlib import Path

import typer

from scripts.utils.common import save_object_to_file
from src.common.project_types import TextMeta
from src.common.utils import process_book_title
from src.models.nlp.init_model import init_model
from src.preprocess.chapter_processor.chapter_processor import process_chapters
from src.preprocess.document_reader.document_reader import read_document


def process_text_to_text_meta(*, text_path: Path, text_meta_output_path: Path) -> None:
    nlp = init_model("en_core_web_lg")
    book_title, raw_chapters = read_document(text_path)
    chapters, speakers = process_chapters(nlp, raw_chapters)
    text_meta = TextMeta(book_title, chapters, speakers)
    save_object_to_file(
        text_meta_output_path,
        Path(process_book_title(text_meta.title)).with_suffix(".json"),
        text_meta,
    )


app = typer.Typer(add_completion=False, help="Process text (.txt/.epub) to text meta")

TEXT_OPTION = typer.Option(
    None,
    "--text",
    help="Text source file (.txt or .epub)",
)
OUTPUT_OPTION = typer.Option(..., "-o", "--output", help="Directory for the resulting JSON")


@app.command()
def run(
    text: Path | None = TEXT_OPTION,
    output: Path = OUTPUT_OPTION,
) -> None:
    if text is None:
        print("❌  Provide text source file (.txt or .epub)")
        raise typer.Exit(1)

    process_text_to_text_meta(text_path=text, text_meta_output_path=output)
    print(f"✅  Done. Results saved to {output}[/]")


if __name__ == "__main__":
    app()





