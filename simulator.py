import os
import random
import timeit
import string

start = timeit.default_timer()

fullDict = "words_alpha.txt"
fullDict = "large(143k).txt"
fullDict = "words(466k).txt"
fullDict = 'allWordleWords.txt'

wordList = []

os.chdir('dictionaries')

with open(fullDict, "r") as file:
    words = file.readlines()
    for word in words:
        if len(word) == 6:
            if not('\'' in word):
                wordList.append(word[0:5])


def guesser(yellows, greens, greys, prevGuesses):
    '''Given yellow and green letters (dict) and grey letters (list), this function
    attempts to guess the answer'''

    guesses = prevGuesses

    possibleWords = possibilities(yellows, greens, greys)

    # if theres only one possible word, guess that
    if len(possibleWords) == 1:
        return possibleWords[0]

    # if there are no possible words, a fatal error has occured, so close program
    elif len(possibleWords) == 0:
        print("ERROR: No possible words found")
        exit()

    # figure out what letters we want to eliminate
    lettersToEliminate = []

    for possibility in possibleWords:
        for letter in possibility[0:5]:
            if (letter not in greens 
                and letter not in yellows
                and letter not in greys
                and letter not in lettersToEliminate):
                lettersToEliminate.append(letter)

    print('eliminate: ' + str(lettersToEliminate))

    # if there are no more letters left unguessed
    # we should just take a shot at one of the possible words
    if (len(lettersToEliminate) == 0 or len(possibleWords) <= 3):
        return possibleWords[0]

    # get the highest ranked word and use that as our next guess
    rankings = wordRanking(guesses, lettersToEliminate)
    # sortedRankings = {k: v for k, v in sorted(rankings.items(), key=lambda item: item[1])}
    topRank = max(rankings.values())
    topRankedGuess = list(rankings.keys())[list(rankings.values()).index(topRank)]
    return topRankedGuess


def letterFrequency():
    '''Returns a dictionary of letters and their corresponding frequency in the 
    given dictionary'''
    # with open(fullDict, 'r') as file:
    #     words = file.readlines()

    alphabet = list(string.ascii_lowercase)
    letterDict = {}
    for letter in alphabet:
        letterDict[letter] = 0
    for word in wordList:
        for letter in word:
            if letter in alphabet:
                letterDict[letter] += 1

    return letterDict


def letterFrequencyLoc():
    '''Returns a dictionary of letters and their corresponding frequency in 
    each position of each word in the given dictionary'''
    
    # with open(fullDict, 'r') as file:
    #     words = file.readlines()

    alphabet = list(string.ascii_lowercase)
    letterDict = {}

    for letter in alphabet:
        letterDict[letter] = [0,0,0,0,0]
    for word in wordList:
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

    # with open(fullDict, 'r') as file:
    #     wordList = file.readlines()

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


def possibilities(yellows, greens, greys):
    '''Given a list of yellows and greens (and corresponding locations
    and list of greys, this function selects all possible words from the given 
    dictionary that fit the constraints'''

    possibilitesLi = []

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
            possibilitesLi.append(word)

    print(str(len(possibilitesLi)) + " possibilities found")

    ticker = 0
    for poss in possibilitesLi:
        if ticker == 10:
            print('...')
            break

        print (poss)
        ticker += 1
    return possibilitesLi


def gamePlayer(ans='rand'):

    greens = {}
    yellows = {}
    greys = []
    guesses = []
    if ans == 'rand':
        answer = wordList[random.randrange(0, len(wordList))]
    
    else:
        answer = wordList[ans]

    for i in range(0, 6):
        guess = guesser(yellows, greens, greys, guesses)
        guesses.append(guess)
        print("guess " + str(i + 1) + ": " + guess)


        for j in range(0, 5):
            if answer[j] == guess[j]:
                greens[guess[j]] = j
            elif guess[j] in answer:
                if guess[j] in yellows:
                    yellows[guess[j]].append(j)
                else:
                    yellows[guess[j]] = [j]
            else: greys.append(guess[j])
        
        print("greens: " + str(greens))
        print("yellows: " + str(yellows))
        print("grey: " + str(greys))
        if guess == answer:
            print("Congrats, you won! In " + str(i + 1) + " tries")
            stop = timeit.default_timer()
            break

    if guess != answer:
        i = 'fail'
        print("Failure")
        stop = timeit.default_timer()

    with open("noGuesses.csv", "a") as file:
        file.write(answer + "; " + str(i) + '\n')

    print("ans: " + answer)
    print('Time: ', stop - start)

for i in range(0, 100):
    print(str(i) + "-----------------------------------------------------------------")
    gamePlayer(i)

print(len(wordList))