"""
Obtained from https://www.mdbg.net/chinese/dictionary?page=cc-cedict
"""

from typing import List
from loguru import logger

from ccs.constants import DATA_ROOT


def extract_words_from_cc_cedict(file_path: str, simplified: bool = True) -> List[str]:
    word_set = set()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            try:
                parts = line.strip().split(" ")
                trad = parts[0]
                simp = parts[1]
                word = simp if simplified else trad
                word_set.add(word)
            except IndexError:
                continue
    return sorted(word_set)


def save_words_to_file(words: List[str], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(words))


if __name__ == "__main__":
    cedict_path = str(DATA_ROOT / "dictionary/cedict_ts.u8")
    output_path = str(DATA_ROOT / "dictionary/cedict_words.txt")

    words = extract_words_from_cc_cedict(cedict_path)
    save_words_to_file(words, output_path)

    logger.success(f"{len(words)} words saved to {output_path}")
