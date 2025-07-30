NEW_LINE = "\n"

PRECEDING_PUNCTUATION_SET = {".", ",", "!", "?", '"', "”", "'", "’"}

QUOTATION_MARK_PAIRS_ORIGIN = [
    ('"', '"'),
    ("'", "'"),
    ("`", "’"),
    ("«", "»"),
    ("‘", "’"),
    ("‚", "’"),
    ("“", "”"),
    ("„", "”"),
    ("‹", "›"),
    ("「", "」"),
    ("『", "』"),
    ("“", '"'),
    ("‘", '"'),
    ("`", '"'),
    ("«", '"'),
    ("‹", '"'),
    ("「", '"'),
    ("『", '"'),
    ("„", '"'),
    ("‚", '"'),
    ('"', "”"),
    ('"', "’"),
]
QUOTATION_MARK_PAIRS = [(ord(x), ord(y)) for x, y in QUOTATION_MARK_PAIRS_ORIGIN]
VALID_QUOTES = {char for pair in QUOTATION_MARK_PAIRS_ORIGIN for char in pair}

QUOTE_TRANSLATION_TABLE: dict[int, int] = {
    ord(x): ord(y)
    for x, y in [
        # Single quotes / apostrophes
        ("ʼ", "'"),
        ("‘", "'"),
        ("’", "'"),
        ("´", "'"),
        ("`", "'"),
        ("ʻ", "'"),
        ("ʹ", "'"),
        # Double quotes
        ("“", '"'),
        ("”", '"'),
        ("„", '"'),
        ("‟", '"'),
        ("″", '"'),  # double prime often used as quote
        ("«", '"'),
        ("»", '"'),
        ("‹", '"'),
        ("›", '"'),
    ]
}
