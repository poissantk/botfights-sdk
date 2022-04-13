def get_word_list():
    words = []
    with open("wordlist.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words


def get_word_list_6():
    words = []
    with open("wordlist6.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words


def get_word_list_big():
    words = []
    with open("wordlist-big.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words
