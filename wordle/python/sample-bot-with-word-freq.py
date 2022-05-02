# sample-bot.py

# sample bot to play wordle. see wordle.py for how to play.


import random
from filterHelpers import filter_words, matrix_best_set_of_words, find_most_frequent

FN_WORDLIST = 'wordlist.txt'

g_wordlist = None


def get_wordlist():
    global g_wordlist
    if None == g_wordlist:
        g_wordlist = []
        for i in open(FN_WORDLIST).readlines():
            i = i[:-1]
            g_wordlist.append(i)
    return g_wordlist


# this has lots of false positives, only pay attention to 3s
#
def could_match(target, guess, feedback):
    for i, ch in enumerate(feedback):
        if '3' == ch:
            if target[i] != guess[i]:
                return False
        else:
            if target[i] == guess[i]:
                return False
    return True


second_guess_cache = {}
## avg for 1000 m2       4.774 , 4.738, 4.722
## avg for 1000 m3       4.638 , 4.659, 4.512
## avg for 10000  m2     4.779 , 4.762, 4.731
## avg for 10000  m3     4.701 , 4.645  , 4.573
start_word_options = ["arose", "serai", "tares", "salet", "buzzy", "qajaq"]

# returns a guess
def play(state):
    # 3 is good
    # state looks like: "-----:00000,arose:31112,amend:31211"
    if len(state) <= 11:
        return start_word_options[2]
    possible = get_wordlist()
    og_wordlist = get_wordlist()
    previous_guesses = state.split(',')
    for pair in previous_guesses:
        guess, feedback = pair.split(':')
        possible = filter_words(feedback, guess, possible)

    if (state[-5:].count('3') == 4) & (state[-5:].count('1') == 1) & (len(possible) > 2):
        placeOfOne = state[-5:].find('1')
        possibleLettersInTheOnePosition = []
        for word in possible:
            possibleLettersInTheOnePosition.append(word[placeOfOne])
        bestWord = 0
        maxWantedLettersInWord = 0
        for word in og_wordlist:
            lettersInWord = 0
            for letter in possibleLettersInTheOnePosition:
                if word.find(letter) != -1:
                    lettersInWord += 1
            if lettersInWord > maxWantedLettersInWord:
                maxWantedLettersInWord = lettersInWord
                bestWord = word
        return bestWord

    if (state[-5:].count('3') == 3) & (state[-5:].count('1') == 2) & (len(possible) > 2):
        placeOfFirstOne = state[-5:].find('1')
        placeOfSecondOne = state[-5:].rfind('1')
        possibleLettersInTheOnePosition = []
        for word in possible:
            possibleLettersInTheOnePosition.append(word[placeOfFirstOne])
            possibleLettersInTheOnePosition.append(word[placeOfSecondOne])
        bestWord = 0
        maxWantedLettersInWord = 0
        for word in og_wordlist:
            lettersInWord = 0
            for letter in possibleLettersInTheOnePosition:
                if word.find(letter) != -1:
                    lettersInWord += 1
            if lettersInWord > maxWantedLettersInWord:
                maxWantedLettersInWord = lettersInWord
                bestWord = word
        return bestWord

    first_guess_feedback = previous_guesses[1].split(":")[1]

    if len(previous_guesses) == 2 and first_guess_feedback in second_guess_cache:
        return find_most_frequent(second_guess_cache[first_guess_feedback])

    best_options = matrix_best_set_of_words(possible, 10)

    if len(previous_guesses) == 2 and first_guess_feedback not in second_guess_cache:
        second_guess_cache[first_guess_feedback] = best_options

    return find_most_frequent(best_options)
