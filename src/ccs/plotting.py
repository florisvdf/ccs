from typing import List
import matplotlib.pyplot as plt

import numpy as np

from ccs.utils import count_words, count_characters, sort_dict_by_values


def plot_words_to_learn(media: str, vocabulary: List[str]) -> plt.Axes:
    word_counts = count_words(media)
    total_words = sum(word_counts.values())
    unknown_counts = {}
    for word, counts in word_counts.copy().items():
        if word not in vocabulary:
            unknown_counts.update({word: word_counts.pop(word)})

    total_words_known_hypothetical = sum(word_counts.values())
    scores = []
    unknown_counts = sort_dict_by_values(unknown_counts)
    for unknown_word, unknown_count in unknown_counts.items():
        total_words_known_hypothetical += unknown_count
        score = (total_words_known_hypothetical / total_words) * 100
        scores.append(score)

    amount = np.arange(len(scores))
    fig, ax = plt.subplots()
    ax.plot(amount, scores)
    xticks = np.arange(0, amount[-1] + 400, 400)
    ax.set_xticks(xticks)
    ax.tick_params(axis="x", labelrotation=45)
    ax.set_title("Number of words to learn to reach desired comprehension", fontsize=12)
    ax.set_xlabel("Amount of Extra Words", fontsize=10)
    ax.set_ylabel("Score Reached", fontsize=10)
    ax.xaxis.grid()
    ax.yaxis.grid()
    return ax


def plot_characters_to_learn(media: str, vocabulary: List[str]) -> plt.Axes:
    char_counts = count_characters(media)
    total_chars = sum(char_counts.values())
    unknown_counts = {}
    for char, counts in char_counts.copy().items():
        if char not in vocabulary:
            unknown_counts.update({char: char_counts.pop(char)})

    total_chars_known_hypothetical = sum(char_counts.values())
    scores = []
    unknown_counts = sort_dict_by_values(unknown_counts)
    for unknown_char, unknown_count in unknown_counts.items():
        total_chars_known_hypothetical += unknown_count
        score = (total_chars_known_hypothetical / total_chars) * 100
        scores.append(score)

    amount = np.arange(len(scores))
    fig, ax = plt.subplots()
    ax.plot(amount, scores)
    xticks = np.arange(0, amount[-1] + 400, 400)
    ax.set_xticks(xticks)
    ax.tick_params(axis="x", labelrotation=45)
    ax.set_title("Number of characters to learn to reach desired comprehension", fontsize=12)
    ax.set_xlabel("Amount of Extra Characters", fontsize=10)
    ax.set_ylabel("Score Reached", fontsize=10)
    ax.xaxis.grid()
    ax.yaxis.grid()
    return ax
