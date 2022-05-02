from wordle import evaluate_word
from textFileProcessing import get_word_frequencies


# string input list database
def contains(input, database):
    howManyContainInput = 0
    for word in database:
        if input in word:
            howManyContainInput += 1
    return howManyContainInput


# string input list database int place
def containsInPlace(input, database, place):
    howManyContainInput = 0
    for word in database:
        # each numer is zero indexed
        if word.index(input) == place:
            howManyContainInput += 1
    return howManyContainInput


# string input list database
def filterContains(input, database):
    # print("words must contain " + input)
    newDatabase = []
    for word in database:
        if input in word:
            newDatabase.append(word)
    return newDatabase


# string input list database
def filterNotContains(input, database):
    # print("words must not contain " + input)
    newDatabase = []
    for word in database:
        if input not in word:
            newDatabase.append(word)
    return newDatabase


# string input list database int place
def filterInPlace(input, database, place):
    # print("words now must contain " + input + " in the position " + str(place))
    newDatabase = []
    for word in database:
        # each numer is zero indexed
        if input in word:
            if word[place] == input:
                newDatabase.append(word)
    return newDatabase


# string input list database int place
def filterNotInPlace(input, database, place):
    # print("words now must not contain " + input + " in the position " + str(place))
    newDatabase = []
    for word in database:
        # each numer is zero indexed
        if input in word:
            if word[place] != input:
                newDatabase.append(word)
        else:
            newDatabase.append(word)
    return newDatabase


# filters the list for strings with the letter duplicated more times than the count allows for
def filter_words_with_dup_letter(word_list, letter, how_many_times_can_it_be_present):
    return list(filter(lambda word: word.count(letter) <= how_many_times_can_it_be_present, word_list))


def filter_words(feedback, guess, possible):
    duplicate_letters_filtered = set([])
    for number in range(len(guess)):
        if feedback[number] == '2':
            possible = filterContains(guess[number], possible)
            possible = filterNotInPlace(guess[number], possible, number)
        elif feedback[number] == '3':
            possible = filterInPlace(guess[number], possible, number)
        elif (guess[number] not in guess[0:number]) & (feedback[number] == '1'):
            placesWithCurrentLetter = []
            for letterNumber in range(5):
                if guess[letterNumber] == guess[number]:
                    placesWithCurrentLetter.append(letterNumber)
            # no dups
            if len(placesWithCurrentLetter) == 1:
                possible = filterNotContains(guess[number], possible)
            # else there are dups
            else:
                # filter words in current place
                possible = filterNotInPlace(guess[number], possible, number)
                for letterNumberToFilter in range(5):
                    if letterNumberToFilter not in placesWithCurrentLetter:
                        # filter other places that don't have the current letter
                        possible = filterNotInPlace(guess[number], possible, letterNumberToFilter)
        ## if we come across a 1 at this point, it means there's duplicate letters
        elif (feedback[number] == '1') and guess[number] not in duplicate_letters_filtered:
            duplicate_letters_filtered.add(guess[number])
            placesWithCurrentLetter = []
            for letterNumber in range(5):
                if guess[letterNumber] == guess[number]:
                    placesWithCurrentLetter.append(letterNumber)
            how_much_is_letter_present = len(placesWithCurrentLetter) - [feedback[index] for index in
                                                                         placesWithCurrentLetter].count('1')
            possible = filter_words_with_dup_letter(possible, guess[number], how_much_is_letter_present)
            possible = filterNotInPlace(guess[number], possible, number)

    return possible


def matrix_start_word_approach(word_list):
    # this will be a list of lists, where the index is the count and the value
    # is an array of the words with that count
    remaining_words_after_guess = {}

    for guess in word_list:
        guess_filter_count = []
        seen_vals = set([])
        for answer in word_list:
            eval_result = evaluate_word(answer, guess)
            if eval_result not in seen_vals:
                guess_filter_count.append(len(filter_words(eval_result, guess, word_list)))
                seen_vals.add(eval_result)
        highest_filter_count = max(guess_filter_count)
        if highest_filter_count in remaining_words_after_guess:
            remaining_words_after_guess[highest_filter_count].append(guess)
        else:
            remaining_words_after_guess[highest_filter_count] = [guess]
    return remaining_words_after_guess[min(remaining_words_after_guess.keys())]


def matrix_start_word_approach2(word_list):
    # this will be a list of lists, where the index is the count and the value
    # is an array of the words with that count
    remaining_words_after_guess = {}

    for guess in word_list:
        eval_to_possible_answers = {}
        for answer in word_list:
            eval_result = evaluate_word(answer, guess)
            if eval_result not in eval_to_possible_answers:
                eval_to_possible_answers[eval_result] = [answer]
            else:
                eval_to_possible_answers[eval_result].append(answer)
        highest_filter_count = max(
            [len(words_for_this_eval) for words_for_this_eval in eval_to_possible_answers.values()])
        if highest_filter_count in remaining_words_after_guess:
            remaining_words_after_guess[highest_filter_count].append(guess)
        else:
            remaining_words_after_guess[highest_filter_count] = [guess]
    return remaining_words_after_guess[min(remaining_words_after_guess.keys())]


def matrix_start_word_approach3(word_list):
    # this will be a list of lists, where the index is the count and the value
    # is an array of the words with that count
    remaining_words_after_guess = {}

    for guess in word_list:
        eval_to_possible_answers = {}
        for answer in word_list:
            eval_result = evaluate_word(answer, guess)
            if eval_result not in eval_to_possible_answers:
                eval_to_possible_answers[eval_result] = [answer]
            else:
                eval_to_possible_answers[eval_result].append(answer)
        avg_filter_count = sum(
            [len(words_for_this_eval) for words_for_this_eval in eval_to_possible_answers.values()]) / len(
            eval_to_possible_answers.values())
        if avg_filter_count in remaining_words_after_guess:
            remaining_words_after_guess[avg_filter_count].append(guess)
        else:
            remaining_words_after_guess[avg_filter_count] = [guess]
    return remaining_words_after_guess[min(remaining_words_after_guess.keys())]


def matrix_best_set_of_words(word_list, best_x_words):
    remaining_words_after_guess = {}
    for guess in word_list:
        eval_to_possible_answers = {}
        for answer in word_list:
            eval_result = evaluate_word(answer, guess)
            if eval_result not in eval_to_possible_answers:
                eval_to_possible_answers[eval_result] = [answer]
            else:
                eval_to_possible_answers[eval_result].append(answer)
        avg_filter_count = sum(
            [len(words_for_this_eval) for words_for_this_eval in eval_to_possible_answers.values()]) / len(
            eval_to_possible_answers.values())
        if avg_filter_count in remaining_words_after_guess:
            remaining_words_after_guess[avg_filter_count].append(guess)
        else:
            remaining_words_after_guess[avg_filter_count] = [guess]
    keys = list(remaining_words_after_guess.keys())
    keys.sort()
    best_answers = []
    for key in keys[:best_x_words]:
        best_answers += remaining_words_after_guess[key]
    return best_answers


def find_most_frequent(options):
    word_freq = get_word_frequencies()
    zipped_freqs = list(zip(word_freq.values(), word_freq.keys()))
    zipped_freqs.sort()
    sorted_words = [word for freq, word in zipped_freqs]
    sorted_options = list(filter(lambda word: word in options, sorted_words))
    return sorted_options[-1]