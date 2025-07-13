import chardet
from loguru import logger
from collections import Counter
from pathlib import Path
from typing import Dict, List
import re

import jieba

from ccs.constants import SIMPLIFIED_PATTERN, DATA_ROOT


def sort_dict_by_values(dictionary: Dict[str, int]) -> Dict[str, int]:
    return {
        key: value
        for key, value in sorted(
            dictionary.items(), key=lambda item: item[1], reverse=True
        )
    }


def is_all_simplified_chinese(text: str) -> bool:
    return all(re.fullmatch(SIMPLIFIED_PATTERN, char) for char in text)


def remove_non_chinese_words(words: List[str]) -> List[str]:
    filtered_words = [word for word in words if is_all_simplified_chinese(word)]
    return filtered_words


def determine_encoding(path: Path) -> str:
    with open(path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"]
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
        logger.error(f"Could not decode media with utf-8, returning empty string")
    return result


def read_char_vocab(path: Path) -> str:
    chars = []
    with open(path, "r") as f:
        for line in f.readlines():
            chars.extend(SIMPLIFIED_PATTERN.findall(line))
    return "".join(set(chars))


def read_word_vocab(path: Path) -> List[str]:
    with open(path, "r") as f:
        word_vocab = [word.strip("\n") for word in f.readlines()]
    return word_vocab


def filter_simplified(line: str) -> str:
    return "".join(SIMPLIFIED_PATTERN.findall(line))


def count_characters(text: str) -> Dict[str, int]:
    return dict(Counter(text))


def count_words(
    text: str, cut_all: bool = False, filter_by_dictionary="XDHYCD7th"
) -> Dict[str, int]:
    segmented_words = jieba.cut(text, cut_all=cut_all)
    segmented_words = remove_non_chinese_words(segmented_words)
    counts = dict(Counter(segmented_words))
    if filter_by_dictionary:
        dictionary = read_word_vocab(DATA_ROOT / "dictionary/XDHYCD7th_words.txt")
        counts = {word: count for word, count in counts.items() if word in dictionary}
    return counts


def score_character_comprehension(media: str, vocabulary: str) -> float:
    character_counts = count_characters(media)
    total_characters = sum(character_counts.values())
    characters_unknown = 0
    for char, counts in character_counts.items():
        if char not in vocabulary:
            characters_unknown += counts
    return 100 - (characters_unknown / total_characters) * 100


def score_word_comprehension(media: str, vocabulary: List[str]) -> float:
    word_counts = count_words(media)
    total_words = sum(word_counts.values())
    words_unknown = 0
    for word, counts in word_counts.items():
        if word not in vocabulary:
            words_unknown += counts
    return 100 - (words_unknown / total_words) * 100


def score_hsk_word_difficulty(media: str, version: str = "new") -> Dict[str, float]:
    data_dir = DATA_ROOT / f"vocabulary/words/hsk_{version}"
    scores = {}
    for filename in data_dir.glob("*.txt"):
        hsk_level = filename.name.split(".")[0]
        vocab = read_word_vocab(filename)
        score = score_word_comprehension(media, vocab)
        scores[f"hsk_{hsk_level}"] = score
    return scores


def score_hsk_character_difficulty(
    media: str, version: str = "new"
) -> Dict[str, float]:
    data_dir = DATA_ROOT / f"vocabulary/characters/hsk_{version}"
    scores = {}
    for filename in data_dir.glob("*.txt"):
        hsk_level = filename.name.split(".")[0]
        vocab = read_char_vocab(filename)
        score = score_character_comprehension(media, vocab)
        scores[f"hsk_{hsk_level}"] = score
    return scores


def count_characters_till_mastery(media: str, vocabulary: str) -> int:
    character_counts = count_characters(media)
    characters_unknown = 0
    for char in character_counts.keys():
        if char not in vocabulary:
            characters_unknown += 1
    return characters_unknown


def count_words_till_mastery(media: str, vocabulary: List[str]) -> int:
    word_counts = count_words(media)
    words_unknown = 0
    for word in word_counts.keys():
        if word not in vocabulary:
            words_unknown += 1
    return words_unknown


def word_vocab_to_learn(
    media: str, vocabulary: List[str], desired_score: float
) -> List[str]:
    word_counts = count_words(media)
    total_words = sum(word_counts.values())
    unknown_counts = {}
    for word, counts in word_counts.copy().items():
        if word not in vocabulary:
            unknown_counts.update({word: word_counts.pop(word)})

    total_words_known_hypothetical = sum(word_counts.values())
    unknown_counts = sort_dict_by_values(unknown_counts)
    new_vocab = []
    for unknown_word, unknown_count in unknown_counts.items():
        total_words_known_hypothetical += unknown_count
        score = (total_words_known_hypothetical / total_words) * 100
        new_vocab.append(unknown_word)
        if score >= desired_score:
            break
    return new_vocab


def character_vocab_to_learn(
    media: str, vocabulary: str, desired_score: float
) -> List[str]:
    char_counts = count_characters(media)
    total_chars = sum(char_counts.values())
    unknown_counts = {}
    for char, counts in char_counts.copy().items():
        if char not in vocabulary:
            unknown_counts.update({char: char_counts.pop(char)})

    total_chars_known_hypothetical = sum(char_counts.values())
    unknown_counts = sort_dict_by_values(unknown_counts)
    new_vocab = []
    for unknown_char, unknown_count in unknown_counts.items():
        total_chars_known_hypothetical += unknown_count
        score = (total_chars_known_hypothetical / total_chars) * 100
        new_vocab.append(unknown_char)
        if score >= desired_score:
            break
    return new_vocab
