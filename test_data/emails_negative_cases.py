import pytest

from utils.fake_user_data import fake

# ===========================================================================
# EMPTY / TYPES (однакові для login і register)
# ===========================================================================

# required (TrimStrings + ConvertEmptyStringsToNull)
EMPTY_EMAIL_CASES = [
    pytest.param("", id="empty"),
    pytest.param("     ", id="spaces-only"),
]

# Не-рядкові значення (слати JSON-тілом).
# Окремий тест: поле email відсутнє у тілі -> 422
INVALID_EMAIL_TYPE_CASES = [
    pytest.param(None, id="null"),
    pytest.param(["a@b.com"], id="array"),
    pytest.param(12345, id="number"),
    pytest.param(True, id="bool"),
    pytest.param({"a": "b"}, id="object"),
]

# ===========================================================================
# Спільні будівельні блоки
# (набір скорочено: один представник на клас еквівалентності, щоб не впиратись
#  у throttle логіну ~30 запитів/хв; парні символи ")" і "]" прибрані)
# ===========================================================================

# Символи, заборонені в local part поза лапками
_FORBIDDEN_CHARS = list("(<>[,;:\"\\")

_FORBIDDEN_CHAR_IDS = {
    "(": "paren-open", "<": "lt", ">": "gt", "[": "bracket-open",
    ",": "comma", ";": "semicolon", ":": "colon",
    '"': "double-quote", "\\": "backslash",
}

_STRUCTURE_CASES = [
    pytest.param(f"@{fake.free_email_domain()}", id="no-local-part"),
    pytest.param(f"{fake.user_name()}{fake.domain_name()}", id="no-at-sign"),
    pytest.param(f"{fake.user_name()}@", id="no-domain"),
    pytest.param(f"{fake.user_name()}@@{fake.domain_name()}", id="double-at"),
    pytest.param(f"{fake.user_name()}@gmail@com", id="two-at-signs"),
]

_DOT_CASES = [
    pytest.param(f"{fake.user_name()}@.{fake.domain_name()}", id="domain-leading-dot"),
    pytest.param(f"{fake.user_name()}@{fake.domain_name()}.", id="domain-trailing-dot"),
    pytest.param(f"{fake.user_name()}@kdteam..test", id="double-dot-domain"),
    pytest.param(f"user..{fake.user_name()}@{fake.domain_name()}", id="double-dot-local"),
    pytest.param(f".{fake.email(domain='kdteam.test')}", id="local-leading-dot"),
    pytest.param(f"{fake.user_name()}.@{fake.domain_name()}", id="local-trailing-dot"),
]

_SPACE_CASES = [
    pytest.param(f"{fake.user_name()} {fake.user_name()}@{fake.domain_name()}", id="space-in-local"),
    pytest.param(f"{fake.user_name()}@ {fake.domain_name()}", id="space-after-at"),
    pytest.param(f"{fake.user_name()}@kdteam .test", id="space-in-domain"),
]

_DOMAIN_CHAR_CASES = [
    pytest.param(f"{fake.user_name()}@-{fake.domain_name()}", id="domain-leading-hyphen"),
    pytest.param(f"{fake.user_name()}@kdteam-.test", id="domain-label-trailing-hyphen"),
    pytest.param(f"{fake.user_name()}@kdteam!.test", id="special-in-domain"),
]

_FORBIDDEN_CHAR_CASES = [
    pytest.param(
        f"{fake.user_name()}{char}{fake.user_name()}@{fake.domain_name()}",
        id=f"special-{_FORBIDDEN_CHAR_IDS[char]}",
    )
    for char in _FORBIDDEN_CHARS
]

# Фіксовані комбінації безпечних заборонених символів <>,;:
# (без лапок, дужок і [ ] \ , які можуть утворити quoted string або RFC-коментар).
_FIXED_FORBIDDEN_CASES = [
    pytest.param("<>,;:@kdteam.test", id="all-safe-forbidden-chars"),
    pytest.param("a,b;c:d<e>f@kdteam.test", id="mixed-between-letters"),
]

# ===========================================================================
# LOGIN: email => 'required|email'  (лише RFC-синтаксис)
# Кирилиця, діакритика, довжина, no-tld, disposable тут 422 НЕ дають.
# ===========================================================================

LOGIN_INVALID_EMAIL_CASES = [
    *_STRUCTURE_CASES,
    *_DOT_CASES,
    *_SPACE_CASES,
    *_DOMAIN_CHAR_CASES,
    *_FORBIDDEN_CHAR_CASES,
    *_FIXED_FORBIDDEN_CASES,
]

# НЕПЕРЕВІРЕНІ: результат залежить від версії egulias/email-validator.
# Прожени вручну й перенеси в LOGIN_INVALID_EMAIL_CASES лише ті, що дали 422.
LOGIN_EMOJI_UNVERIFIED_CASES = [
    pytest.param("😀@kdteam.test", id="emoji-local-only"),
    pytest.param(f"{fake.user_name()}😀@kdteam.test", id="emoji-local-end"),
    pytest.param(f"😀{fake.user_name()}@kdteam.test", id="emoji-local-start"),
    pytest.param(f"{fake.user_name()}@kdteam😀.test", id="emoji-domain"),
    pytest.param(f"{fake.user_name()}@😀.test", id="emoji-domain-only"),
    pytest.param(f"{fake.user_name()}@kdteam.test😀", id="emoji-after-tld"),
    pytest.param("👨‍👩‍👧‍👦@kdteam.test", id="emoji-zwj-sequence"),
    pytest.param(f"{fake.user_name()}@kdteam.te😀st", id="emoji-in-tld"),
]

# ===========================================================================
# REGISTER: required|string|email|min:5|max:100|not_regex(кирилиця)|ValidEmail
# (UniqueColumn і DisposableEmail тут не враховано)
# ValidEmail = filter_var(FILTER_VALIDATE_EMAIL): тільки ASCII, домен із крапкою.
# ===========================================================================

# Домен без TLD (для login це 401, для register 422 через ValidEmail)
_REGISTER_NO_TLD_CASES = [
    pytest.param(f"{fake.user_name()}@kdteamtest", id="no-tld"),
    pytest.param(f"{fake.user_name()}@localhost", id="localhost"),
]

# min:5 / max:100 / межі RFC
_REGISTER_LENGTH_CASES = [
    pytest.param("a@b", id="min-3-chars"),
    pytest.param("a@bc", id="min-4-chars"),
    pytest.param("a" * 64 + "@" + "b" * 32 + ".com", id="max-101-chars"),
    pytest.param("a" * 65 + "@example.com", id="local-part-65"),
    pytest.param(f"{fake.user_name()}@" + "a" * 64 + ".com", id="domain-label-64"),
]

# not_regex:/[А-Яа-яЁё]/u — кирилиця будь-де. Українські і ї є ґ у діапазон
# не входять, але їх відсікає ValidEmail (не ASCII).
# Гомогліфи задані через \u-коди, щоб було видно, що це кирилиця.
_REGISTER_CYRILLIC_CASES = [
    pytest.param("користувач@gmail.com", id="cyrillic-local"),
    pytest.param("user@пошта.укр", id="cyrillic-domain"),
    pytest.param("юзер@пошта.укр", id="cyrillic-local-and-domain"),
    pytest.param("Ёлка@gmail.com", id="cyrillic-yo"),
    pytest.param("user@gmail.c\u043em", id="cyrillic-homoglyph-o-in-tld"),
    pytest.param("us\u0435r@gmail.com", id="cyrillic-homoglyph-e-in-local"),
    pytest.param("їжак@gmail.com", id="ukrainian-yi-local"),
    pytest.param("user@gma\u0456l.com", id="ukrainian-i-domain"),
    pytest.param("є@gmail.com", id="ukrainian-ye-local"),
    pytest.param("ґанок@gmail.com", id="ukrainian-ge-local"),
]

# Інший не-ASCII: filter_var без UNICODE-флагу його відхиляє
_REGISTER_NON_ASCII_CASES = [
    pytest.param("josé@example.com", id="latin-diacritics"),
    pytest.param("münchen@example.de", id="umlaut"),
    pytest.param("用户@example.com", id="cjk-local"),
    pytest.param(f"{fake.user_name()}@münchen.de", id="diacritics-domain"),
]

_REGISTER_EMOJI_CASES = [
    pytest.param("😀@gmail.com", id="emoji-local-only"),
    pytest.param(f"{fake.user_name()}😀@gmail.com", id="emoji-local-end"),
    pytest.param(f"😀{fake.user_name()}@gmail.com", id="emoji-local-start"),
    pytest.param(f"{fake.user_name()}@gmail😀.com", id="emoji-domain"),
    pytest.param(f"{fake.user_name()}@😀.com", id="emoji-domain-only"),
    pytest.param(f"{fake.user_name()}@gmail.com😀", id="emoji-after-tld"),
    pytest.param("👨‍👩‍👧‍👦@gmail.com", id="emoji-zwj-sequence"),
    pytest.param(f"{fake.user_name()}@gmail.c😀m", id="emoji-in-tld"),
]

# Керувальні символи всередині адреси (на краях їх обріже TrimStrings)
_REGISTER_CONTROL_CHAR_CASES = [
    pytest.param(f"{fake.user_name()}\t{fake.user_name()}@{fake.domain_name()}", id="tab-inside"),
    pytest.param(f"{fake.user_name()}\n{fake.user_name()}@{fake.domain_name()}", id="newline-inside"),
]

REGISTER_INVALID_EMAIL_CASES = [
    *_STRUCTURE_CASES,
    *_DOT_CASES,
    *_SPACE_CASES,
    *_DOMAIN_CHAR_CASES,
    *_FORBIDDEN_CHAR_CASES,
    *_FIXED_FORBIDDEN_CASES,
    *_REGISTER_NO_TLD_CASES,
    *_REGISTER_LENGTH_CASES,
    *_REGISTER_CYRILLIC_CASES,
    *_REGISTER_NON_ASCII_CASES,
    *_REGISTER_EMOJI_CASES,
    *_REGISTER_CONTROL_CHAR_CASES,
]