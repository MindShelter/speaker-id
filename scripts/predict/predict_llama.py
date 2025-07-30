import os
from pathlib import Path

import typer

from scripts.predict.base_predict import predict_speakers
from scripts.types.config_types import MainScriptsConfig
from src.models.llm_clients.configs.llama import LlamaConfig
from src.models.llm_clients.llama import LlamaLLMClient
from src.models.llm_clients.prompts.single_prompt import single_prompt
from src.models.nlp.init_model import init_model

app = typer.Typer(add_completion=False, help="Speaker prediction with Llama LLM")


def build_config(
    *,
    text_path: Path | None,
    text_meta: Path | None,
    output: Path,
    timing: bool,
) -> MainScriptsConfig:
    if (text_path is None) == (text_meta is None):
        print("❌  Provide either --text-path or --text-meta (but not both).[/]")
        raise typer.Exit(1)

    if "LLAMA_API_KEY" not in os.environ:
        print("❌  Set LLAMA_API_KEY environment variable first.[/]")
        raise typer.Exit(1)

    nlp = init_model("en_core_web_lg")
    llm = LlamaLLMClient(config=LlamaConfig.from_env())

    return MainScriptsConfig(
        nlp=nlp,
        llm=llm,
        llm_prompt=single_prompt,
        text_path=text_path,
        text_meta_path=text_meta,
        text_meta_output_path=output,
        enable_timing_logs=timing,
    )


TEXT_PATH_OPTION = typer.Option(
    None,
    "--text-path",
    help="Raw book file (.txt/.epub)",
)
TEXT_META_OPTION = typer.Option(
    None,
    "--text-meta",
    help="Existing text_meta JSON",
)
OUTPUT_OPTION = typer.Option(..., "-o", "--output", help="Directory for the resulting JSON")
TIMING_OPTION = typer.Option(False, "--timing", help="Print per‑chapter timings")


@app.command()
def run(
    text_path: Path | None = TEXT_PATH_OPTION,
    text_meta: Path | None = TEXT_META_OPTION,
    output: Path = OUTPUT_OPTION,
    timing: bool = TIMING_OPTION,
) -> None:
    config = build_config(
        text_path=text_path,
        text_meta=text_meta,
        output=output.resolve(),
        timing=timing,
    )
    predict_speakers(config)
    print(f"✅  Done. Results saved to {output}[/]")


if __name__ == "__main__":
    app()
