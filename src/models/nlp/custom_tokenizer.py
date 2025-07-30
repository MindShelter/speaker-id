from collections.abc import Callable

from spacy import Language
from spacy.tokens import Doc

from src.preprocess.quote_finder.constants import VALID_QUOTES

"""If two identical valid quotes appear consecutively in a token,
split them into two tokens while leaving the rest of the token intact.
"""


def split_consecutive_quotes_in_token(word: str) -> list[str]:
    tokens: list[str] = []
    current: list[str] = []
    i = 0
    while i < len(word):
        # Check for a pair of consecutive valid quotes.
        if i < len(word) - 1 and word[i] in VALID_QUOTES and word[i + 1] == word[i]:
            if current:
                tokens.append("".join(current))
                current = []
            # Append each quote as its own token.
            tokens.append(word[i])
            tokens.append(word[i + 1])
            i += 2
        else:
            current.append(word[i])
            i += 1
    if current:
        tokens.append("".join(current))
    return tokens


def split_consecutive_quotes(words: list[str], spaces: list[bool]) -> tuple[list[str], list[bool]]:
    new_words: list[str] = []
    new_spaces: list[bool] = []

    for word, space in zip(words, spaces, strict=False):
        # Check if the token contains any consecutive valid quotes.
        has_consecutive = any(word[i] in VALID_QUOTES and word[i + 1] == word[i] for i in range(len(word) - 1))
        if has_consecutive:
            tokens = split_consecutive_quotes_in_token(word)
            for j, token in enumerate(tokens):
                new_words.append(token)
                # Only the last token retains the original whitespace flag.
                new_spaces.append(space if j == len(tokens) - 1 else False)
        else:
            new_words.append(word)
            new_spaces.append(space)

    return new_words, new_spaces


def merge_contraction_tokens(doc: Doc, text: str) -> tuple[list[str], list[bool]]:
    merged_words: list[str] = []
    merged_spaces: list[str | bool] = []

    for token in doc:
        starts_with_quote = token.text and token.text[0] in VALID_QUOTES
        preceded_by_alnum = token.idx > 0 and text[token.idx - 1].isalnum()

        if starts_with_quote and preceded_by_alnum:
            if merged_words:
                merged_words[-1] += token.text
                if token.whitespace_:
                    merged_spaces[-1] = token.whitespace_
            else:
                merged_words.append(token.text)
                merged_spaces.append(token.whitespace_)
        else:
            merged_words.append(token.text)
            merged_spaces.append(token.whitespace_)

    return merged_words, merged_spaces


def split_leading_quotes(words: list[str], spaces: list[bool]) -> tuple[list[str], list[bool]]:
    split_words: list[str] = []
    split_spaces: list[bool] = []

    for word, space in zip(words, spaces, strict=False):
        if word and word[0] in VALID_QUOTES and len(word) > 1:
            split_words.append(word[0])
            split_spaces.append(False)
            split_words.append(word[1:])
            split_spaces.append(space)
        else:
            split_words.append(word)
            split_spaces.append(space)

    return split_words, split_spaces


def split_trailing_quotes(words: list[str], spaces: list[bool]) -> tuple[list[str], list[bool]]:
    final_words: list[str] = []
    final_spaces: list[bool] = []

    for word, space in zip(words, spaces, strict=False):
        if word and word[-1] in VALID_QUOTES and len(word) > 1:
            final_words.append(word[:-1])
            final_spaces.append(False)
            final_words.append(word[-1])
            final_spaces.append(space)
        else:
            final_words.append(word)
            final_spaces.append(space)

    return final_words, final_spaces


def get_custom_tokenizer(nlp: Language, original_tokenizer: Callable[[str], Doc]) -> Callable[[str], Doc]:
    def custom_tokenizer(text: str) -> Doc:
        doc = original_tokenizer(text)
        merged_words, merged_spaces = merge_contraction_tokens(doc, text)
        leading_split_words, leading_split_spaces = split_leading_quotes(merged_words, merged_spaces)
        trailing_split_words, trailing_split_spaces = split_trailing_quotes(leading_split_words, leading_split_spaces)
        final_words, final_spaces = split_consecutive_quotes(trailing_split_words, trailing_split_spaces)

        return Doc(nlp.vocab, words=final_words, spaces=final_spaces)

    return custom_tokenizer
