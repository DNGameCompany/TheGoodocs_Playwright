import os

def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Не задано обов'язкову змінну середовища: {name}")
    return value