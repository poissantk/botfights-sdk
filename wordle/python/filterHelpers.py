
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

def filter_words(feedback, guess, possible):

    for number in range(len(guess) - 1):
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
    return possible
