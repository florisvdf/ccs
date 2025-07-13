"""
Obtained from https://github.com/CNMan/XDHYCD7th
"""

import re
from loguru import logger

from ccs.constants import DATA_ROOT


def extract_words_from_xdhycd(file_path: str, output_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    words = re.findall(r"【([\u4e00-\u9fff]+)】", text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(words))
    logger.success(f"{len(words)} words saved to {output_path}")


if __name__ == "__main__":
    xdhycd_path = str(DATA_ROOT / "dictionary/XDHYCD7th.txt")
    output_path = str(DATA_ROOT / "dictionary/XDHYCD7th_words.txt")
    extract_words_from_xdhycd(xdhycd_path, output_path)
