import os
import timeit

start = timeit.default_timer()

fullDict = "words(466k).txt"
fullDict = "large(143k).txt"
fullDict = "words_alpha.txt"
fullDict = 'allWordleWords.txt'


wordList = []

# os.chdir("Random Shite/Wordle Solver/dictionaries")
os.chdir("dictionaries")

with open(fullDict, "r") as file:
    words = file.readlines()
    for word in words:
        if len(word) == 6:
            if not('\'' in word):
                wordList.append(word[0:5])

greens = {}
yellows = {}
greys = []

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


possibilites = []
print("possible words: ")

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

for word in possibilites:
    print(word)



print(str(len(possibilites)) + " possibilities found")
print(greens)
print(yellows)
print(greys)

# hates - round - climb

stop = timeit.default_timer()

print('Time: ', stop - start)