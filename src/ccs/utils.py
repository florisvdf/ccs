import chardet
from loguru import logger
from collections import Counter
from pathlib import Path
from typing import Dict

from ccs.constants import SIMPLIFIED_PATTERN


def determine_encoding(path: Path) -> str:
    with open(path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    return encoding


def read_media(path: Path) -> str:
    encoding = determine_encoding(path)
    logger.info(f"Detected encoding {encoding}.")
    result = ""
    try:
        with open(path, "r", encoding=encoding) as f:
            lines = f.readlines()
            result = "".join(list(map(filter_simplified, lines)))
    except UnicodeDecodeError:
        logger.warning(f"Could not decode media with {encoding}, defaulting to utf-8")
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            result = "".join(list(map(filter_simplified, lines)))
    except UnicodeDecodeError:
        logger.error(f"Could not decode media with utf-8, returnign empty string")
    return result


def filter_simplified(line: str) -> str:
    return ''.join(SIMPLIFIED_PATTERN.findall(line))


def count_characters(text: str) -> Dict[str, int]:
    return dict(Counter(text))


def score_comprehension(media: str, vocabulary: str) -> float:
    character_counts = count_characters(media)
    total_characters = sum(character_counts.values())
    characters_unknown = 0
    for char, counts in character_counts.items():
        if char not in vocabulary:
            characters_unknown += counts
    return 100 - (characters_unknown / total_characters) * 100


