from collections.abc import Callable

import pytest
from spacy import Language

from src.models.nlp.init_model import init_model
from src.preprocess.quote_finder.quote_finder import find_quotes as _find_quotes_base


@pytest.fixture(scope="session")
def nlp() -> Language:
    return init_model("en_core_web_lg")


@pytest.fixture
def find_quotes(nlp: Language) -> Callable[[str], list[str]]:
    def _inner(text: str) -> list[str]:
        return [q.text for q in _find_quotes_base(nlp(text))]

    return _inner


@pytest.mark.parametrize(
    ("case", "text", "expected"),
    [
        ("simple-single", '"Test quote" \n Some narration', ['"Test quote"']),
        (
            "simple-multi",
            'She said, "Hello there!" and then replied, "How are you?"',
            ['"Hello there!"', '"How are you?"'],
        ),
        ("empty-string", 'He said, "" and continued.', ['""']),
        ("whitespace-only", 'Notice the gap: "   " right there.', ['"   "']),
        (
            "leading-trailing-spaces",
            '"   Leading and trailing spaces   " extra',
            ['"   Leading and trailing spaces   "'],
        ),
        (
            "adjacent-quotes",
            '"First quote""Second quote"',
            ['"First quote"', '"Second quote"'],
        ),
        ("custom-infix-no-space", '"Exactly!"She said.', ['"Exactly!"']),
        (
            "custom-infix-after-comma",
            'He said,"First quote"\n"Exactly!"She said',
            ['"First quote"', '"Exactly!"'],
        ),
        ("custom-infix-after-exclamation", 'She said "Amazing!"', ['"Amazing!"']),
        (
            "nested-single-inside-double",
            "He said, \"This is a 'nested quote' example.\" And left.",
            ["\"This is a 'nested quote' example.\""],
        ),
        (
            "newline-delimiter-after",
            '"Multiline quote ends" , \n Narration follows',
            ['"Multiline quote ends"'],
        ),
        (
            "newline-inside",
            '"This is a quote\nthat spans multiple lines." More text follows.',
            ['"This is a quote\nthat spans multiple lines."'],
        ),
        (
            "unclosed-quote-with-newline",
            '"Multiline quote not ends properly,\n"But it\'s not a problem"',
            ['"Multiline quote not ends properly,\n', '"But it\'s not a problem"'],
        ),
        ("unclosed-quote-no-newline", '"This quote never closes', []),
        (
            "mismatched-quotes",
            '"Mismatched closing quote” and text',
            ['"Mismatched closing quote”'],
        ),
        (
            "several-quotes-plus-recovery",
            '"Quote one" some text, then "Quote two with punctuation!" '
            'and finally, a tricky case: "Unclosed quote starts and then resets '
            "with 'proper closure' after error.\" More narration.",
            [
                '"Quote one"',
                '"Quote two with punctuation!"',
                "\"Unclosed quote starts and then resets with 'proper closure' after error.\"",
            ],
        ),
        (
            "fake-quote (“sip”ping)",
            "Walking into the conference room, Sarah started “sip”ping her coffee, glancing at her notes."
            " “What a lovely view,” she exclaimed",
            ["“What a lovely view,”"],
        ),
        (
            "uote surrounded by punctuation: quotes immediately follow a period with no space",
            "“All right,” David said, adjusting his glasses, surveying the scene."
            "He paused.“Are you ready for the demonstration?”",
            ["“All right,”", "“Are you ready for the demonstration?”"],
        ),
    ],
)
def test_quote_extraction_cases(case: str, text: str, expected: str, find_quotes: Callable[[str], list[str]]) -> None:
    assert find_quotes(text) == expected
