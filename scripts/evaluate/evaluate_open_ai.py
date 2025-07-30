import os
from pathlib import Path

import typer

from scripts.evaluate.base_evaluate import evaluate_speakers
from scripts.types.config_types import MainScriptsConfig
from src.models.llm_clients.configs.open_ai import OpenAIConfig
from src.models.llm_clients.open_ai import OpenAILLMClient
from src.models.llm_clients.prompts.single_prompt import single_prompt
from src.models.nlp.init_model import init_model

app = typer.Typer(add_completion=False, help="Speaker evaluation with OpenAI")


def build_config(
    *,
    text_meta: Path | None,
    output: Path,
    timing: bool,
) -> MainScriptsConfig:
    if text_meta is None:
        print("❌  Provide --text-meta.[/]")
        raise typer.Exit(1)

    if "OPENAI_API_KEY" not in os.environ:
        print("❌  Set OPENAI_API_KEY environment variable first.[/]")
        raise typer.Exit(1)

    nlp = init_model("en_core_web_lg")
    llm = OpenAILLMClient(config=OpenAIConfig.from_env())

    return MainScriptsConfig(
        nlp=nlp,
        llm=llm,
        llm_prompt=single_prompt,
        text_meta_path=text_meta,
        text_meta_output_path=output,
        enable_timing_logs=timing,
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
    text_meta: Path | None = TEXT_META_OPTION,
    output: Path = OUTPUT_OPTION,
    timing: bool = TIMING_OPTION,
) -> None:
    config = build_config(
        text_meta=text_meta,
        output=output.resolve(),
        timing=timing,
    )
    evaluate_speakers(config)
    print(f"✅  Done. Results saved to {output}[/]")


if __name__ == "__main__":
    app()
