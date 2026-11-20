import pytest

# ===========================================================================
# Правила
#   register: 'password' => 'required|string|min:6|max:255'
#   login:    'password' => 'required|string'   (без min/max)
#
# min/max для рядків у Laravel рахують СИМВОЛИ (mb_strlen), а не байти.
# ===========================================================================

# ===========================================================================
# НЕГАТИВНІ (очікується 422, помилка в ключі "password")
# ===========================================================================

# required: порожній рядок (-> null) і рядок лише з пробілів
# (Laravel `required` відхиляє рядок, який порожній після trim).
# У UI порожнє поле зупиняє нативна підказка браузера (required),
# запит на бекенд не йде. Пробіли браузер пропускає, їх відсікає бекенд.
EMPTY_PASSWORD_CASES = [
    pytest.param("", id="empty"),
    pytest.param("     ", id="spaces-only"),
]

# Не-рядкові значення (лише через API/JSON-тіло, у формі так не відправити).
# Окремий тест: поле password відсутнє у тілі -> 422
INVALID_PASSWORD_TYPE_CASES = [
    pytest.param(None, id="null"),
    pytest.param(["password123"], id="array"),
    pytest.param(123456, id="number"),
    pytest.param(True, id="bool"),
    pytest.param({"a": "b"}, id="object"),
]

# LOGIN: окрім EMPTY_PASSWORD_CASES і типів, інших негативних кейсів
# за правилами немає (min/max у login не діють).
LOGIN_INVALID_PASSWORD_CASES = [
    *EMPTY_PASSWORD_CASES,
]

# REGISTER ------------------------------------------------------------------

# Лише пробіли/таби довжиною >= 6: min:6 виконано, але required відхиляє
_REGISTER_WHITESPACE_ONLY_CASES = [
    pytest.param(" " * 6, id="spaces-6"),
    pytest.param("\t" * 6, id="tabs-6"),
]

# min:6 -> 1..5 символів
_REGISTER_TOO_SHORT_CASES = [
    pytest.param("a", id="1-char"),
    pytest.param("12345", id="5-digits"),
    pytest.param("ab cd", id="5-chars-with-space"),
    pytest.param("абвгд", id="5-cyrillic-chars"),
    pytest.param("😀" * 5, id="5-emoji"),
]

# max:255 -> 256 символів (рахуються символи, а не байти)
_REGISTER_TOO_LONG_CASES = [
    pytest.param("a" * 256, id="256-latin"),
    pytest.param("я" * 256, id="256-cyrillic"),
    pytest.param("😀" * 256, id="256-emoji"),
]

REGISTER_INVALID_PASSWORD_CASES = [
    *EMPTY_PASSWORD_CASES,
    *_REGISTER_WHITESPACE_ONLY_CASES,
    *_REGISTER_TOO_SHORT_CASES,
    *_REGISTER_TOO_LONG_CASES,
]

# ===========================================================================
# ПОЗИТИВНІ МЕЖІ (поле password НЕ має давати 422)
# Решту полів робіть валідними; для login очікуйте не-422 (успіх або
# помилка автентифікації), для register успіх.
# ===========================================================================

LOGIN_VALID_PASSWORD_CASES = [
    pytest.param("1", id="1-char-no-min"),
    pytest.param("p" * 1000, id="1000-chars-no-max"),
    pytest.param("pass word", id="space-inside"),
    pytest.param("пароль😀!@#$%^&*()", id="unicode-emoji-special"),
]

REGISTER_VALID_PASSWORD_CASES = [
    pytest.param("a" * 6, id="6-chars-min-boundary"),
    pytest.param("a" * 255, id="255-chars-max-boundary"),
    pytest.param("я" * 255, id="255-cyrillic-chars"),
    pytest.param("😀" * 6, id="6-emoji"),
    pytest.param("pass word1", id="space-inside"),
    pytest.param("пароль123", id="cyrillic-password"),
    pytest.param("!@#$%^&*()_+-=[]{};':\",.<>/?\\|`~", id="special-chars-only"),
]

# ===========================================================================
# НЕПЕРЕВІРЕНІ: залежить від налаштувань middleware TrimStrings.
# За замовчуванням у Laravel поле password з trim виключене, тоді пробіли
# по краях зберігаються і це валідний пароль. Якщо ж у проєкті trim
# застосовується, "  pass12  " стане "pass12" (6 символів, теж валідний),
# а "  abc  " (7 символів з пробілами) стане "abc" і дасть 422 (min:6).
# Прожени вручну й зафіксуй baseline.
# ===========================================================================
REGISTER_TRIM_UNVERIFIED_CASES = [
    pytest.param("  pass12  ", id="padded-valid-after-trim"),
    pytest.param("  abc  ", id="padded-short-after-trim"),
]