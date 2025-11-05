import tkinter as tk
from tkinter import ttk, messagebox
import string
import os

# Ensure the word list file is in the same directory as this script
fullDict = "dictionaries/allWordleWords.txt"

def letterFrequency():
    '''Returns a dictionary of letters and their corresponding frequency in the given dictionary'''
    if not os.path.exists(fullDict):
        messagebox.showerror("File Error", f"The word list file '{fullDict}' was not found.")
        return {}
    with open(fullDict, 'r') as file:
        words = file.readlines()

    alphabet = list(string.ascii_lowercase)
    letterDict = {}
    for letter in alphabet:
        letterDict[letter] = 0
    for word in words:
        word = word.strip()
        for letter in word:
            if letter in alphabet:
                letterDict[letter] += 1

    return letterDict

def letterFrequencyLoc():
    '''Returns a dictionary of letters and their corresponding frequency in each position of each word in the given 5-letter word dictionary'''
    if not os.path.exists(fullDict):
        messagebox.showerror("File Error", f"The word list file '{fullDict}' was not found.")
        return {}
    with open(fullDict, 'r') as file:
        words = file.readlines()

    alphabet = list(string.ascii_lowercase)
    letterDict = {}

    for letter in alphabet:
        letterDict[letter] = [0, 0, 0, 0, 0]
    for word in words:
        word = word.strip()
        for i in range(0, 5):
            if word[i] in alphabet:
                letterDict[word[i]][i] += 1

    return letterDict

def possibilities(yellows, greens, greys):
    '''Selects all possible words from the given dictionary that fit the constraints'''
    if not os.path.exists(fullDict):
        messagebox.showerror("File Error", f"The word list file '{fullDict}' was not found.")
        return []
    with open(fullDict, 'r') as file:
        wordList = file.readlines()

    possibilites = []

    for word in wordList:
        word = word.strip()
        wordPossible = True

        # Check yellow letters
        for Yeletter in yellows:
            if Yeletter not in word:
                wordPossible = False
                break
            for place in yellows[Yeletter]:
                if word[place] == Yeletter:
                    wordPossible = False
                    break
            if not wordPossible:
                break

        if not wordPossible:
            continue

        # Check grey letters
        for greyLetter in greys:
            if greyLetter in word:
                wordPossible = False
                break
        if not wordPossible:
            continue

        # Check green letters
        for green in greens:
            if word[greens[green]] != green:
                wordPossible = False
                break

        if wordPossible:
            possibilites.append(word)

    return possibilites

def wordRanking(guesses=[], lettersToEliminate=list(string.ascii_lowercase)):
    '''Assigns a ranking to each word based on letter frequency and position'''
    rankingDict = {}
    guessedLetters = []

    for guess in guesses:
        for letter in guess:
            if letter not in guessedLetters:
                guessedLetters.append(letter)

    alphabet = list(string.ascii_lowercase)

    letterFreq = letterFrequency()
    letterFreqL = letterFrequencyLoc()
    if not letterFreq or not letterFreqL:
        return {}

    with open(fullDict, 'r') as file:
        wordList = file.readlines()

    for word in wordList:
        word = word.strip()
        score = 0
        lettersScored = []

        for index, letter in enumerate(word):
            if (letter not in guessedLetters
                and letter in alphabet
                and letter in lettersToEliminate):

                if letter not in lettersScored:
                    score += letterFreq[letter.lower()]  # Score letters only once

                score += letterFreqL[letter.lower()][index]

                lettersScored.append(letter)

        rankingDict[word] = score

    return rankingDict

def compute():
    guesses = []
    greens = {}  # Letter: position
    yellows = {}  # Letter: list of positions they can't be in
    greys = []
    lettersToEliminate = []

    # Letters that have been guessed (to avoid double counting)
    guessed_letters = []

    for i in range(6):
        word = guess_entries[i].get().strip().lower()
        if len(word) == 5 and all(c in string.ascii_lowercase for c in word):
            guesses.append(word)
            colors = color_menus[i]
            for j in range(5):
                color = colors[j].get()
                letter = word[j]
                if color == 'green':
                    greens[letter] = j
                elif color == 'yellow':
                    if letter in yellows:
                        yellows[letter].append(j)
                    else:
                        yellows[letter] = [j]
                elif color == 'grey':
                    greys.append(letter)
                # Collect guessed letters
                if letter not in guessed_letters:
                    guessed_letters.append(letter)
        elif word == '':
            # Skip empty guesses
            continue
        else:
            messagebox.showerror("Input Error", f"Guess {i+1} is invalid. Please enter a 5-letter word.")
            return  # Exit the function

    # Compute possible words
    possible_words = possibilities(yellows, greens, greys)

    # Determine letters to eliminate
    for possibility in possible_words:
        for letter in possibility.strip():
            if (letter not in greens
                and letter not in yellows
                and letter not in greys
                and letter not in lettersToEliminate):
                lettersToEliminate.append(letter)

    # Compute rankings
    rankings = wordRanking(guesses, lettersToEliminate)

    # Display results
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, "Possible words:\n")
    for word in possible_words:
        result_text.insert(tk.END, word.strip() + "\n")
    result_text.insert(tk.END, f"\n{len(possible_words)} possible words found.\n")

    result_text.insert(tk.END, f"\nEliminate letters: {lettersToEliminate}\n")
    result_text.insert(tk.END, "Top ten guesses:\n")

    sortedRankings = {k: v for k, v in sorted(rankings.items(), key=lambda item: item[1])}
    lenSR = len(sortedRankings) - 1
    wordListSorted = list(sortedRankings.keys())
    for i in range(lenSR, lenSR - 10, -1):
        if i >= 0:
            result_text.insert(tk.END, f"{wordListSorted[i].strip()}  Score: {sortedRankings[wordListSorted[i]]}\n")

# Create the main window
root = tk.Tk()
root.title("Wordle Solver Assistant")

# Frame for guesses
guesses_frame = ttk.Frame(root)
guesses_frame.pack(padx=10, pady=10)

guess_entries = []  # List of Entry widgets for the guesses
color_menus = []    # List of lists containing the color dropdowns for each letter

for i in range(6):  # Up to 6 guesses
    # Frame for each guess
    guess_row = ttk.Frame(guesses_frame)
    guess_row.pack(pady=5)

    # Label for guess number
    guess_label = ttk.Label(guess_row, text=f"Guess {i+1}:")
    guess_label.pack(side=tk.LEFT)

    # Entry widget for guessed word
    guess_entry = ttk.Entry(guess_row, width=7)
    guess_entry.pack(side=tk.LEFT, padx=5)
    guess_entries.append(guess_entry)

    # Dropdown menus for each letter's color feedback
    letter_colors = []
    for j in range(5):
        color_var = tk.StringVar(value="grey")
        color_menu = ttk.OptionMenu(guess_row, color_var, "grey", "grey", "yellow", "green")
        color_menu.pack(side=tk.LEFT)
        letter_colors.append(color_var)
    color_menus.append(letter_colors)

# Compute button
compute_button = ttk.Button(root, text="Compute", command=compute)
compute_button.pack(pady=10)

# Text widget to display results
result_text = tk.Text(root, height=20, width=50)
result_text.pack(pady=10)

root.mainloop()