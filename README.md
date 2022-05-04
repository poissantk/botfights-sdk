# botfights-sdk
SDK for botfights

# CS4100 Final Project
To run our bot using the final algorithm:
1. Enter the wordle/python folder
2. Run the command "python wordle.py katiebot wordlist.txt sample-bot-with-word-freq.play 106"

To run our bot using the average matrix algorithm:
1. Enter the wordle/python folder
2. Run the command "python wordle.py katiebot wordlist.txt sample-bot.play 106"

To run our bot using the worst case matrix algorithm:
1. Enter the wordle/python folder
2. Change line 98 in sample-bot.py to "best_options = matrix_start_word_approach2(possible)"
3. Run the command "python wordle.py katiebot wordlist.txt sample-bot.play 106"
