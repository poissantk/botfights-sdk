from textFileProcessing import get_word_list
from wordle import evaluate_word
from filterHelpers import filter_words


def matrix_start_word_approach(word_list):
    # this will be a list of lists, where the index is the count and the value
    # is an array of the words with that count
    remaining_words_after_guess = {}

    for guess in word_list:
        guess_filter_count = []
        for answer in word_list:
            eval_result = evaluate_word(answer, guess)
            guess_filter_count.append(7)
        highest_filter_count = max(guess_filter_count)
        if highest_filter_count in remaining_words_after_guess:
            remaining_words_after_guess[highest_filter_count].append(guess)
        else:
            remaining_words_after_guess[highest_filter_count] = [guess]
    return remaining_words_after_guess[min(remaining_words_after_guess.keys())]

# print(filter_words("words", "aesir", get_word_list()))

# print(matrix_start_word_approach(["word", "word", "word"]))
