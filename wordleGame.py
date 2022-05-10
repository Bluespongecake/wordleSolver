from decimal import HAVE_THREADS
import os
import random

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

greens = {}
yellows = {}
greys = []
guesses = []

answer = wordList[random.randrange(0, len(wordList))]

for i in range(0, 6):
    guess = ''
    while len(guess) != 5:
        guess = input("Enter your guess: ")

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
        print("Congrats, you won! In " + str(i) + " tries")
        break


print(answer)