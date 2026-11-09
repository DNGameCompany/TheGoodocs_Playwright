import string

import pytest

from utils.fake_user_data import fake, fake_ua

EMPTY_EMAIL_CASES = [
    pytest.param("", id="empty"),
    pytest.param("     ", id="spaces-only"),
]

INVALID_EMAIL_CASES = [
    pytest.param(f"@{fake.free_email_domain()}", id="no-local-part"),
    pytest.param(f"{fake.user_name()}{fake.domain_name()}", id="no-at-sign"),
    pytest.param(f"{fake.user_name()}@", id="no-domain"),
    pytest.param(f"{fake.user_name()}@kdteamtest", id="no-tld"),
    pytest.param(f"{fake_ua.first_name().lower()}@{fake.domain_name()}", id="cyrillic-local"),
    pytest.param(f"{fake.user_name()}@кдтім.тест", id="cyrillic-domain"),
    pytest.param(
        f"{fake_ua.first_name().lower()}_{fake.user_name()}@kdteam.тест",
        id="cyrillic-local-and-tld",
    ),
    pytest.param(f" {fake.email(domain='kdteam.test')}", id="leading-space"),
    pytest.param(f"{fake.email(domain='kdteam.test')} ", id="trailing-space"),
    pytest.param(f"{fake.user_name()}@.{fake.domain_name()}", id="domain-leading-dot"),
    pytest.param(f"{fake.user_name()}@{fake.domain_name()}.", id="domain-trailing-dot"),
]

# Спецсимволи, згенеровані через Faker
_SPECIAL_CHARS = list("()<>[],;:\"'\\")


def _special_char_id(char: str) -> str:
    names = {
        "(": "paren-open", ")": "paren-close", "<": "lt", ">": "gt",
        "[": "bracket-open", "]": "bracket-close", ",": "comma",
        ";": "semicolon", ":": "colon", '"': "double-quote",
        "'": "single-quote", "\\": "backslash",
    }
    return f"special-{names[char]}"


SPECIAL_CHAR_EMAIL_CASES = [
    pytest.param(f"{fake.user_name()}{char}{fake.user_name()}@{fake.domain_name()}",
                 id=_special_char_id(char))
    for char in _SPECIAL_CHARS
]

# Рядок із випадкових спецсимволів через Faker
RANDOM_SPECIAL_EMAIL_CASES = [
    pytest.param(
        f"{''.join(fake.random_choices(elements=string.punctuation, length=6))}@{fake.domain_name()}",
        id="random-punctuation-local",
    ),
]

INVALID_EMAIL_SPECIAL_CASES = [
    *SPECIAL_CHAR_EMAIL_CASES,
    *RANDOM_SPECIAL_EMAIL_CASES,
    pytest.param(f"{fake.user_name()} {fake.user_name()}@{fake.domain_name()}", id="space-inside"),
    pytest.param(f"{fake.user_name()}@@{fake.domain_name()}", id="double-at"),
    pytest.param(f"{fake.user_name()}@kdteam..test", id="double-dot-domain"),
    pytest.param(f".{fake.email(domain='kdteam.test')}", id="leading-dot"),
    pytest.param(f"{fake.user_name()}.@{fake.domain_name()}", id="trailing-dot"),
    pytest.param(f"{fake.user_name()}@-{fake.domain_name()}", id="domain-leading-hyphen"),
    pytest.param(f"{fake.user_name()}@gmail!.com", id="special-in-domain"),

    # --- Емодзі ---
    pytest.param("😀@gmail.com", id="emoji-local-only"),
    pytest.param(f"{fake.user_name()}😀@gmail.com", id="emoji-local-end"),
    pytest.param(f"😀{fake.user_name()}@gmail.com", id="emoji-local-start"),
    pytest.param(f"{fake.user_name()}@gmail😀.com", id="emoji-domain"),
    pytest.param(f"{fake.user_name()}@😀.com", id="emoji-domain-only"),
    pytest.param(f"{fake.user_name()}@gmail.com😀", id="emoji-after-tld"),
    pytest.param("👨‍👩‍👧‍👦@gmail.com", id="emoji-zwj-sequence"),
    pytest.param(f"{fake.user_name()}@gmail.c😀m", id="emoji-in-tld"),
]