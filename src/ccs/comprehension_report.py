from typing import Optional
from pathlib import Path

import typer

from ccs.utils import (
    read_media,
    read_char_vocab,
    read_word_vocab,
    count_characters,
    count_words,
    score_word_comprehension,
    score_character_comprehension,
    score_hsk_word_difficulty,
    score_hsk_character_difficulty,
    count_characters_till_mastery,
    count_words_till_mastery,
    word_vocab_to_learn,
    character_vocab_to_learn,
    remove_non_chinese_words,
)
from ccs.io import write_tables


def main(media: str, unit: str, output_path: Optional[str] = None, vocab: str = "hsk"):
    if output_path is None:
        output_path = str(Path().resolve())
    body = read_media(Path(media))
    if vocab == "hsk":
        if unit == "word":
            scores_old = score_hsk_word_difficulty(body, version="old")
            scores_new = score_hsk_word_difficulty(body, version="new")
            write_tables([scores_old, scores_new], Path(output_path))


# Create better logic for collecting content
# Focus as little as possible on prettiness. Just needs to be clear
# Change columns names from key, value to something else, ideally reflecting HSK old and new
# Add table for media stats (total words, total chars, etc)
# Add plots
# Add other cases (character, own vocab)

if __name__ == "__main__":
    typer.run(main)
