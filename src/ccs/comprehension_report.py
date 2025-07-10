from typing import Optional
from pathlib import Path
import json
from loguru import logger

import matplotlib.pyplot as plt
import typer

from ccs.utils import (
    read_media,
    read_char_vocab,
    read_word_vocab,
    score_word_comprehension,
    score_character_comprehension,
)
from ccs.plotting import plot_characters_to_learn, plot_words_to_learn
from ccs.constants import DATA_ROOT

scoring_function = {
    "words": score_word_comprehension,
    "characters": score_character_comprehension,
}
vocab_reading_function = {"words": read_word_vocab, "characters": read_char_vocab}
plotting_function = {
    "words": plot_words_to_learn,
    "characters": plot_characters_to_learn,
}


def main(
    media: str, unit: str, output_path: Optional[str] = None, vocab: str = "hsk_old"
):
    """Also save some book stats: total number of words/chars in media,
    unique number of words/chars"""
    body = read_media(Path(media))
    if vocab.startswith("hsk"):
        version = vocab.split("_")[1]
        vocab_file_paths = [
            file_path
            for file_path in (DATA_ROOT / f"vocabulary/{unit}/hsk_{version}").glob(
                "*.txt"
            )
        ]
    elif Path(vocab).exists():
        vocab_file_paths = [Path(vocab)]
    else:
        raise ValueError(
            f"Must pass either a path to a vocabulary, 'hsk_old' or 'hsk_new' as vocab"
            f" argument."
        )
    scores = {}
    for fp in vocab_file_paths:
        vocab_file_name = fp.name.split(".")[0]
        vocabulary = vocab_reading_function[unit](fp)
        score = scoring_function[unit](body, vocabulary)
        scores[vocab_file_name] = score
        _ = plotting_function[unit](body, vocabulary)
        plt.tight_layout()
        plt.savefig(Path(output_path) / f"{vocab_file_name}_{unit}_to_learn.pdf")
        plt.clf()
    with open(Path(output_path) / f"{unit}_scores.json", "w") as fp:
        json.dump(scores, fp)
    logger.success(f"Wrote scores and figures to {output_path}.")


if __name__ == "__main__":
    typer.run(main)
