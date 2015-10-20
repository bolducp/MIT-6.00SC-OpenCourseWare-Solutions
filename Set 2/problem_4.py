# Problem Set 3, Problem 4

import random
import string


def get_word(filename):
    inFile = open(filename, 'r', 0)
    line = inFile.readline()
    wordlist = string.split(line)
    return random.choice(wordlist)


def print_board(word, guessed_letters):
    for letter in word:
        if letter in guessed_letters:
            print letter,
        else:
            print " _ ",
    print


def user_move(word, guessed_letters):
    available_letters(guessed_letters)
    print
    guess = raw_input("Guess a letter: ")
    print "\n"
    if guess in guessed_letters:
        print "You've already guessed that letter. Choose another."
        return user_move(word, guessed_letters)
    elif guess in word:
        print "Nice guess."
        return guess
    else:
        print "Sorry. There's no %s." % guess
        return guess


def available_letters(guessed_letters):
    alphabet = "abcdefghijklmnopqrstuvwxzy"
    print "\n", "Available letters: ",
    for letter in alphabet:
        if letter not in guessed_letters:
            print letter,


def guess_in_word(word, guess):
    return guess in word


def game_won(word, guessed_letters):
    for letter in word:
        if letter not in guessed_letters:
            return False
    print "You've won! You've solved the word: %s" % word
    return True


def check_no_moves_remaining(moves_remaining, word):
    if moves_remaining == 1:
        print "You have 1 move remaining."
        return False
    elif moves_remaining > 1:
        print "You have %d moves remaining." % moves_remaining
        print
        return False
    else:
        print "Sorry, you're out of moves! Game Over. The word was: %s" % word
        return True


def main():
    word = get_word("words.txt")
    guessed_letters = []
    moves_remaining = 12

    while not game_won(word, guessed_letters) and not check_no_moves_remaining(moves_remaining, word):
        print_board(word, guessed_letters)
        guess = user_move(word, guessed_letters)
        guessed_letters.append(guess)
        if not guess_in_word(word, guess):
            moves_remaining -= 1


if __name__ == "__main__":
    main()