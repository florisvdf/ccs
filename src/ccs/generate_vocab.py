from pathlib import Path
from loguru import logger

import typer

from ccs.utils import (
    read_media,
    read_word_vocab,
    read_char_vocab,
    word_vocab_to_learn,
    character_vocab_to_learn,
)

vocab_reading_function = {"words": read_word_vocab, "characters": read_char_vocab}
vocab_to_learn_function = {
    "words": word_vocab_to_learn,
    "characters": character_vocab_to_learn,
}


def main(
    media: str, unit: str, vocab: str, output_path: str, desired_score: float = 98
):
    body = read_media(Path(media))
    vocab_file_path = Path(vocab)
    vocabulary = vocab_reading_function[unit](vocab_file_path)
    vocab_to_learn = vocab_to_learn_function[unit](body, vocabulary, desired_score)
    with open(Path(output_path) / f"{unit}_vocab_learn.txt", "w") as fp:
        for entry in vocab_to_learn:
            fp.write(f"{entry}\n")
    logger.success(f"Wrote {len(vocab_to_learn)} {unit} to learn to {output_path}.")


if __name__ == "__main__":
    typer.run(main)
