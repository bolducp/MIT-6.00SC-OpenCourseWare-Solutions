from problem_set_3_A import *
from perm import *

#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    hand_length = 0
    for v in hand.values():
        hand_length += v

    word_choices = []

    for num in range(1, hand_length + 1):
        num_perms = get_perms(hand, num)
        for perm in num_perms:
            if perm in word_list:
                word_choices.append(perm)

    comp_word = ''

    for word in word_choices:
        score = get_word_score(word, hand_length)
        if score > get_word_score(comp_word, hand_length):
            comp_word = word

    return comp_word


# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """

    hand_score = 0
    hand_length = calculate_handlen(hand)

    while comp_choose_word(hand, word_list) != '':
        print "Current Hand:",
        display_hand(hand)

        comp_word = comp_choose_word(hand, word_list)

        word_score = get_word_score(comp_word, hand_length)
        hand_score += word_score
        print "'%s' earned %d points. Total: %d" % (comp_word, word_score, hand_score)
        print
        hand = update_hand(hand, comp_word)

    print "No more available moves. Total score: %d" % hand_score



# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    hand = deal_hand(HAND_SIZE)

    while True:
        game = raw_input("\nEnter 'n' to play a new game. Enter 'r' to replay your last game. Enter 'e' to exit. \n")

        if game == "n":
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), word_list)
        elif game == "r":
            play_hand(hand.copy(), word_list)
        elif game == "e":
            print "Game ended."
            break
        else:
            print "Please enter a valid command."
            return play_game(word_list)

        comp_game = raw_input(("\nEnter 'u' to play a new game. Enter 'c' to have the computer play a game."))

        while comp_game != "u" and comp_game != "c":
            print "Please enter a valid command."
            comp_game = raw_input(("\nEnter 'u' to play a new game. Enter 'c' to have the computer play a game. "))

        if comp_game == "u":
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), word_list)
        elif comp_game == "c":
            hand = deal_hand(HAND_SIZE)
            comp_play_hand(hand.copy(), word_list)


# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    HAND_SIZE = 7
    word_list = load_words()
    play_game(word_list)

    
