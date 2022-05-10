import os
import string

os.chdir("Random Shite/Wordle Solver/")
os.chdir("dictionaries")

fullDict = "allWordleWords.txt"

def generateDict():
    outDict = "5 Letter Dictionary - longer.txt"

    wordlist = []
    with open(fullDict, "r") as file:
        words = file.readlines()
        for word in words:
            if len(word) == 6:
                wordlist.append(word)


    with open(outDict, "w") as file:
        for word in wordlist:
            if '\'' not in word:
                file.write(word)
            if 'o' in word and 't' in word and 'h' in word and word[3] == 't':
                if not ('a' in word
                        or 'u' in word 
                        or 'd' in word 
                        or 'i' in word 
                        or 'e' in word 
                        or 'r' in word
                        or 's' in word
                        or word[1] == 'of'):
                    print(word)

def letterFrequency():
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

        print(letterDict)

letterFrequency()