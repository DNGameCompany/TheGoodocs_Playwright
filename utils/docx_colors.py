# utils/docx_colors.py
import re
import zipfile
from collections import Counter

# Шукаємо і w:color="RRGGBB" (рамки), і w:color w:val="RRGGBB" (текст), і w:fill="RRGGBB" (заливка)
COLOR_RE = re.compile(r'w:(?:color|fill)(?: w:val)?="([0-9A-Fa-f]{6})"')


def _is_neutral(hex_color: str, tolerance: int = 12) -> bool:
    """Білий, чорний, сірі та дуже блідий відтінок. Вони не є акцентом."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return max(r, g, b) - min(r, g, b) < tolerance


def get_accent_color(docx_path) -> str | None:
    """Найчастіший не нейтральний колір у document.xml, колонтитулах і т. д."""
    counter = Counter()
    with zipfile.ZipFile(docx_path) as z:
        for name in z.namelist():
            # styles.xml не беремо: там дефолтні сині кольори Word
            if name.startswith("word/") and name.endswith(".xml") and name != "word/styles.xml":
                xml = z.read(name).decode("utf8", errors="ignore")
                counter.update(c.upper() for c in COLOR_RE.findall(xml))

    for color, _ in counter.most_common():
        if not _is_neutral(color):
            return color
    return None