# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    return set(secret_word).issubset(set(letters_guessed))



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    result = ''
    
    for c in secret_word:
        if c in letters_guessed:
            result += c
        else:
            result += '_ '

    return result



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    ascii_lowercase_set = set(string.ascii_lowercase)
    letters_guessed_set = set(letters_guessed)
    return "".join(sorted(ascii_lowercase_set.difference(letters_guessed_set)))
    
def get_unique_letters(word):
    return len(set(word))

def decrease_warning_count(cause_msg, guessed_word, warnings_remaining, guesses_remaining):
    if warnings_remaining == 0:
        warnings_remaining = 3
        guesses_remaining -= 1

        if guesses_remaining > 0:
            print(f"Oops! {cause_msg}. You have no warnings left so you lose one guess: {guessed_word}")
    else:
        warnings_remaining -= 1
        print(f"Oops! {cause_msg}. You have {warnings_remaining} warnings left: {guessed_word}")

    return (warnings_remaining, guesses_remaining)

def print_run_out_of_guesses_message(secret_word):
    print(f"Sorry, you ran out of guesses. The word was {secret_word}")

def print_separator():
    print("-------------")

def print_welcome_message(secret_word, warnings_remaining):
    print("Welcome to the game Hangman!")
    print(f"I'm thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warnings_remaining} warnings left.")
    print_separator()

def print_win_message(secret_word, guesses_remaining):
    score = guesses_remaining * get_unique_letters(secret_word)

    print(f"Congratulations, you won! Your total score for this game is: {score}")

VOWELS = ['a', 'e', 'i', 'o', 'u']

def get_guesses_lose_per_letter(letter):
    return 2 if letter in VOWELS else 1

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    guesses_remaining = 6
    warnings_remaining = 3
    valid_letters = string.ascii_lowercase
    letters_guessed = []

    print_welcome_message(secret_word, warnings_remaining)
    
    while True:
        print(f"You have {guesses_remaining} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        letter = input("Please guess a letter: ").lower()

        guessed_word = get_guessed_word(secret_word, letters_guessed)

        if letter not in valid_letters:
            warnings_remaining, guesses_remaining = decrease_warning_count(
                "That is not a valid letter", guessed_word, warnings_remaining, guesses_remaining
            )
        elif letter in letters_guessed:
            warnings_remaining, guesses_remaining = decrease_warning_count(
                "You've already guessed that letter", guessed_word, warnings_remaining, guesses_remaining
            )
        elif letter in secret_word:
            letters_guessed.append(letter)
            print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
        else: 
            guesses_remaining -= get_guesses_lose_per_letter(letter)
            letters_guessed.append(letter)

            print(f"Oops! That letter in not in my word: {get_guessed_word(secret_word, letters_guessed)}")

        print_separator()
        if is_word_guessed(secret_word, letters_guessed):
            print_win_message(secret_word, guesses_remaining)

            break
        elif guesses_remaining <= 0:
            print_run_out_of_guesses_message(secret_word)

            break


def word_len_with_gaps(word):
    result = 0
    index = 0
    word_len = len(word)

    while index < word_len:
        result += 1

        if word[index] == '_' and word[index + 1] == ' ':
            index += 2
        else:
            index += 1

    return result

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    other_word_index = 0
    my_word_index = 0
    my_word_len = len(my_word)
   
    if word_len_with_gaps(my_word) != len(other_word):
        return False

    while my_word_index < my_word_len:
        # Skip a gap if we found it
        if my_word[my_word_index] == '_' and my_word[my_word_index + 1] == ' ':
            my_word_index += 2
            other_word_index += 1
        else:
            if my_word[my_word_index] != other_word[other_word_index]:
                return False
            
            my_word_index += 1
            other_word_index += 1

    return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    match_count = 0
    for word in wordlist:
        if match_with_gaps(my_word, word):
            match_count += 1
            print(word, end = " ")

    if match_count == 0:
        print("No matches found")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
   
    guesses_remaining = 6
    warnings_remaining = 3
    valid_letters = string.ascii_lowercase
    letters_guessed = []

    print_welcome_message(secret_word, warnings_remaining)
    
    while True:
        print(f"You have {guesses_remaining} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        letter = input("Please guess a letter: ").lower()

        guessed_word = get_guessed_word(secret_word, letters_guessed)

        if letter == '*':
            print("Possible word matches are: ", end = "")
            show_possible_matches(guessed_word)
            print()
        elif letter not in valid_letters:
            warnings_remaining, guesses_remaining = decrease_warning_count(
                "That is not a valid letter", guessed_word, warnings_remaining, guesses_remaining
            )
        elif letter in letters_guessed:
            warnings_remaining, guesses_remaining = decrease_warning_count(
                "You've already guessed that letter", guessed_word, warnings_remaining, guesses_remaining
            )
        elif letter in secret_word:
            letters_guessed.append(letter)
            print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
        else: 
            guesses_remaining -= get_guesses_lose_per_letter(letter)
            letters_guessed.append(letter)

            print(f"Oops! That letter in not in my word: {get_guessed_word(secret_word, letters_guessed)}")

        print_separator()
        if is_word_guessed(secret_word, letters_guessed):
            print_win_message(secret_word, guesses_remaining)

            break
        elif guesses_remaining <= 0:
            print_run_out_of_guesses_message(secret_word)

            break

if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman("else")
    #hangman_with_hints(secret_word)
