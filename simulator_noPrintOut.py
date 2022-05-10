import os
import random
import timeit

# note this is no fastre than the regular one with print out
start = timeit.default_timer()

fullDict = "words_alpha.txt"
fullDict = "large(143k).txt"
fullDict = "words(466k).txt"
fullDict = 'allWordleWords.txt'

wordList = []

os.chdir("Random Shite/Wordle Solver/dictionaries")

with open(fullDict, "r") as file:
    words = file.readlines()
    for word in words:
        if len(word) == 6:
            if not('\'' in word):
                wordList.append(word[0:5])


def guesser(yellows, greens, greys, runs):
    startingWords = ['round', 'hates', 'climb']

    if runs < len(startingWords):
        return startingWords[runs]
    else:
        possibleWords = possibilities(yellows, greens, greys)

    if len(possibleWords) == 1:
        return possibleWords[0]

    elif len(possibleWords) == 0:
        print("ERROR: No possible words found")
        exit()

    else: return possibleWords[0]


def possibilities(yellows, greens, greys):

    possibilites = []

    for word in wordList:
        wordPossible = True
        for Yeletter in yellows:
            if not (Yeletter in word):
                wordPossible = False
                continue
            for place in yellows[Yeletter]:
                if word[place] == Yeletter:
                    wordPossible = False

        for greyLetter in greys:
            if greyLetter in word:
                wordPossible = False
        
        for green in greens:
            if word[greens[green]] != green:
                wordPossible = False
        
        if wordPossible == True:
            possibilites.append(word)

    return possibilites


def gamePlayer():

    greens = {}
    yellows = {}
    greys = []
    guesses = []

    answer = wordList[random.randrange(0, len(wordList))]

    for i in range(0, 6):
        guess = guesser(yellows, greens, greys, i)

        for j in range(0, 5):
            if answer[j] == guess[j]:
                greens[guess[j]] = j
            elif guess[j] in answer:
                if guess[j] in yellows:
                    yellows[guess[j]].append(j)
                else:
                    yellows[guess[j]] = [j]
            else: greys.append(guess[j])
        
        if guess == answer:
            break

    if guess != answer:
        i = -1

    with open("noGuesses.txt", "a") as file:
        file.write(str(i) + '\n')

    

for i in range(0, 1000):
    gamePlayer()

stop = timeit.default_timer()
print('Time: ', stop - start)