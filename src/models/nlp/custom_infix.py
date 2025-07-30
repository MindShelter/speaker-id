import re

from spacy import Language
from spacy.util import compile_infix_regex

from src.models.nlp.constants import PUNCTUATION_SET
from src.preprocess.quote_finder.constants import VALID_QUOTES


def get_custom_infix(nlp: Language) -> re.Pattern:
    quote_chars = "".join(re.escape(q) for q in VALID_QUOTES)
    punct_chars = "".join(re.escape(p) for p in PUNCTUATION_SET)
    infixes = list(nlp.Defaults.infixes)
    # Infix rule: Splits tokens when a punctuation symbol
    # (e.g., comma, exclamation, question mark, colon, semicolon, dash)
    # immediately precedes any valid quote character.
    # This ensures that quotes are tokenized separately from adjacent punctuation.
    infixes.append(f"(?<=[{punct_chars}])(?=[{quote_chars}])")

    return compile_infix_regex(infixes)
