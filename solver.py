import os
fullDict = "allwordlewords.txt"



wordList = []

os.chdir("dictionaries")
with open(fullDict, "r") as file:
    words = file.readlines()
    for word in words:
        if len(word) == 6:
            wordList.append(word)

guesses = []
greens = {}
yellows = []

for i in range(0, 5):
    guess = input("Enter Guess no. " + str(i + 1) + ":")
    guesses.append(guess)
    for i in range(0, 5):
        green = '00'
        while len(green) != 1 and len(green) != 0:
            green = input("Enter a Green letter in this word: ")
        if green == '':
            break
        greenPos = input("Enter position of this green: ")
        greens[green] = int(greenPos)

    yellow = input("Enter yellows in this word (letters)")
    if yellow == "":
        continue
    for letter in yellow:
        if letter not in yellows:
            yellows.append(letter)
    yellow = ''

    possibilites = []
    print("possible words: ")
    for word in wordList:
        c = 0
        for letter in yellows:
            if letter in word:
                c += 1
        if c == len(yellows):
            c = 0
            for green in greens:
                if word[greens[green]] == green:
                    c += 1
            if c == len(greens):
                possibilites.append(word)
    
    for word in possibilites:
        print(word)
            
        
print(greens)
print()
print(yellows)