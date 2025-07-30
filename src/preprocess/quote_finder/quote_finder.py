from spacy.tokens import Doc, Span, Token

from src.preprocess.quote_finder.constants import (
    NEW_LINE,
    PRECEDING_PUNCTUATION_SET,
    QUOTATION_MARK_PAIRS,
    QUOTE_TRANSLATION_TABLE,
    VALID_QUOTES,
)


def detect_quotes_idx_pairs(doc: Doc) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    open_quote_idx: int | None = None

    def is_valid_pair(open_tok: Token, close_tok: Token) -> bool:
        if len(open_tok.text) != 1 or len(close_tok.text) != 1:
            return False
        return (ord(open_tok.text), ord(close_tok.text)) in QUOTATION_MARK_PAIRS

    # That is for checking possible fake-quotes
    # For instance “sip”ping will be detected by Spacy as two tokens as “ and sip”ping
    def is_fake_quote(_quote_index: int) -> bool:
        if _quote_index + 1 < len(doc):
            quote = doc[_quote_index]
            next_tok = doc[_quote_index + 1]
            if quote.idx + len(quote.text) == next_tok.idx:
                canonical_quote = quote.text.translate(QUOTE_TRANSLATION_TABLE)
                canonical_next = next_tok.text.translate(QUOTE_TRANSLATION_TABLE)
                if canonical_next.find(canonical_quote) > 0:
                    return True
        return False

    def is_newline_delimiter(item_idx: int) -> bool:
        if item_idx <= 0 or item_idx >= len(doc) - 1:
            return False
        prev_tok = doc[item_idx - 1]
        next_tok = doc[item_idx + 1]
        if prev_tok.text not in PRECEDING_PUNCTUATION_SET:
            return False
        return (next_tok.text in VALID_QUOTES or
                (next_tok.text and next_tok.text[0].isupper()))

    for i, token in enumerate(doc):
        if NEW_LINE in token.text:
            if is_newline_delimiter(i) and open_quote_idx is not None:
                pairs.append((open_quote_idx, i))
                open_quote_idx = None
            continue

        if token.text not in VALID_QUOTES:
            continue

        if is_fake_quote(i):
            continue

        if open_quote_idx is None:
            open_quote_idx = i
        elif is_valid_pair(doc[open_quote_idx], token):
            pairs.append((open_quote_idx, i))
            open_quote_idx = None
        else:
            continue

    return pairs


def find_quotes(doc: Doc) -> list[Span]:
    return [doc[start : end + 1] for start, end in detect_quotes_idx_pairs(doc)]
