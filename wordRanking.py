# aim here is to take a list of possibilities, and a list of words that have been guessed
# and rank the possible words based on how many other letters they will eliminate. 
# This will only be effective assuming the answer word is randomised and not subject to human choice

import os
import string

# os.chdir("Random Shite/Wordle Solver/")
os.chdir("dictionaries")

fullDict = "allWordleWords.txt"


def letterFrequency():
    '''Returns a dictionary of letters and their corresponding frequency in the 
    given dictionary'''
    with open(fullDict, 'r') as file:
        words = file.readlines()

    alphabet = list(string.ascii_lowercase)
    letterDict = {}
    for letter in alphabet:
        letterDict[letter] = 0
    for word in words:
        for letter in word:
            if letter in alphabet:
                letterDict[letter] += 1

    return letterDict


def letterFrequencyLoc():
    '''Returns a dictionary of letters and their corresponding frequency in 
    each position of each word in the given dictionary'''
    
    with open(fullDict, 'r') as file:
        words = file.readlines()

    alphabet = list(string.ascii_lowercase)
    letterDict = {}

    for letter in alphabet:
        letterDict[letter] = [0,0,0,0,0]
    for word in words:
        for i in range(0, 5):                
            if word[i] in alphabet:
                letterDict[word[i]][i] += 1

    return letterDict


def possibilities(yellows, greens, greys):
    '''Given a list of yellows and greens (and corresponding locations
    and list of greys, this function selects all possible words from the given 
    dictionary that fit the constraints'''

    with open(fullDict, 'r') as file:
        wordList = file.readlines()
        
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


def wordRanking(guesses=[], lettersToEliminate=list(string.ascii_lowercase)):
    '''returns a dictionary of every word in the dictionary, assigning a ranking to each
    scores are based on frequecy and location of letters that have not already been guessed'''
    rankingDict = {}
    guessedLetters = []

    for guess in guesses:
        for letter in guess:
            if not letter in guessedLetters:
                guessedLetters.append(letter)

    alphabet = list(string.ascii_lowercase)

    letterFreq = letterFrequency()
    letterFreqL = letterFrequencyLoc()

    with open(fullDict, 'r') as file:
        wordList = file.readlines()

    for word in wordList:
        score = 0
        lettersScored = []

        for index, letter in enumerate(word):
            if (letter not in guessedLetters 
                and letter in alphabet                              #make sure letter is alpha
                and letter in lettersToEliminate):

                if (letter not in lettersScored):
                    score += letterFreq[letter.lower()]             #make sure letters are not double scored

                score += letterFreqL[letter.lower()][index]

            lettersScored.append(letter)

        rankingDict[word] = score

    # for word in rankingDict:
    #     print(word[0:5] + '; ' + str(rankingDict[word]))

    return rankingDict


def getCols():
    '''prompt user for coloured letters'''
    guesses = []
    greens = {}
    yellows = {}
    greys = []

    for i in range(0, 6):
        guess = '00'
        while len(guess) != 5 and len(guess) != 0:
            guess = input("Enter guesses: ")
        if guess == '':
            break
        guesses.append(guess)

    for i in range(0, 5):
        green = '00'
        while len(green) != 1 and len(green) != 0:
            green = input("Enter a Green letter: ")
        if green == '':
            break
        greenPos = input("Enter position of this green: ")
        greens[green] = int(greenPos)

    for i in range(0, 25):
        yellow = '00'
        while len(yellow) != 1 and len(yellow) != 0:
            yellow = input("Enter a yellow letter: ")
        if yellow == '':
            break
        yellowPos = input("Enter position of this yellow: ")
        if yellow in yellows:
            yellows[yellow].append(int(yellowPos))
        else:
            yellows[yellow] = [int(yellowPos)]

    for i in range(0, 1):
        grey = input("Enter greys (letters)")
        if grey == "":
            continue
        for letter in grey:
            if letter not in greys:
                greys.append(letter)
        grey = ''

    return guesses, greens, yellows, greys


guesses, greens, yellows, greys = getCols()

possibilities = possibilities(yellows, greens, greys)

lettersToEliminate = []

for possibility in possibilities:
    for letter in possibility[0:5]:
        if (letter not in greens 
            and letter not in yellows
            and letter not in greys
            and letter not in lettersToEliminate):
            lettersToEliminate.append(letter)

print(lettersToEliminate)

rankings = wordRanking(guesses, lettersToEliminate)

print("Possible words:")
for word in possibilities:
    print(word)

print(str(len(possibilities)) + " possible words found")

print()
print("Elminiate: " + str(lettersToEliminate))
print("Top ten guesses:")

sortedRankings = {k: v for k, v in sorted(rankings.items(), key=lambda item: item[1])}
lenSR = len(sortedRankings) - 1
wordListSorted = list(sortedRankings.keys())
for i in range(lenSR, lenSR - 10, -1):
    print(wordListSorted[i][0:5] + " " + str(sortedRankings[wordListSorted[i]]))