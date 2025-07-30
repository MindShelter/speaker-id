import spacy
from spacy import Language
from spacy.cli import download as spacy_download

from src.models.nlp.custom_infix import get_custom_infix
from src.models.nlp.custom_tokenizer import get_custom_tokenizer


def load_or_download(model_name: str, fallback: str | None = "en_core_web_sm") -> Language:
    try:
        return spacy.load(model_name)
    except OSError:
        try:
            spacy_download(model_name, direct=False)
            return spacy.load(model_name)
        except Exception as dl_err:
            if fallback:
                print(f"⚠️ Could not download '{model_name}': {dl_err}")
                print(f"➜  Falling back to '{fallback}'.")
                return spacy.load(fallback)
            raise


def init_model(model_name: str = "en_core_web_lg") -> Language:
    nlp = load_or_download(model_name)

    infix_re = get_custom_infix(nlp)
    nlp.tokenizer.infix_finditer = infix_re.finditer

    original_tokenizer = nlp.tokenizer
    nlp.tokenizer = get_custom_tokenizer(nlp, original_tokenizer)

    return nlp
