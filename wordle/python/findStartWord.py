from textFileProcessing import get_word_list
from wordle import evaluate_word
from filterHelpers import filterContains, filterNotInPlace, filterInPlace, filterNotContains


def matrix_start_word_approach():
    word_list = get_word_list()
    # this will be a list of lists, where the index is the count and the value
    # is an array of the words with that count
    remaining_words_after_guess = {}

    for guess in word_list:
        guess_filter_count = []
        for answer in word_list:
            eval_result = evaluate_word(answer, guess)


