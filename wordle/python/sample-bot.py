# sample-bot.py

# sample bot to play wordle. see wordle.py for how to play.


import random


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


# returns a guess
def play(state):
    # 3 is good
    # state looks like: "-----:00000,arose:31112,amend:31211"
    if len(state) == 11:
        return "arose"
    possible = get_wordlist()
    for pair in state.split(','):
        guess, feedback = pair.split(':')
        # possible = list(filter(lambda x: could_match(x, guess, feedback), possible))
        # print("elect" in possible)
        for number in range(4):
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
            # print("elect" in possible)
    return random.choice(possible)



