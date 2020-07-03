"""
Blackjack
Damon Jones

for 11PRG 1.8
"""

# Imports
from deck import Deck
from smart_input import s_input
import os
import random


# Functions

def clear_screen() -> None:
    """Clears the console screen. Works on Windows, MacOS and Linux

    It should be noted that this won't work in some IDE's that don't output to the
    OS' standard terminal. This is confirmed to work on Windows in repl.it, Visual
    Studio Code and when the code is ran in the command line.

    While I probably could use curses, I'd rather use what's in the standard
    library.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def menu() -> None:
    pass


def game() -> None:
    """One game of blackjack is played inside of this function. Part of the main game loop.
    """
    letter_values = {
        "A": 11, #Ace
        "J": 10, #Jack
        "Q": 10, #Queen
        "K": 10  #King
    }

    cards = Deck(letter_values)


    hand = []
    for i in range(2):
        hand.append(cards.deal_card())

    blackjack = False
    if cards.get_hand_total(hand) == 21:
        blackjack = True


    dealer_hand = []
    dealer_hand.append(cards.deal_card(False)) #Adds the dealer's turned card
    dealer_hand.append(cards.deal_card()) #Adds the dealer's up card

    dealer_blackjack = False
    if cards.get_hand_total(dealer_hand) == 21:
        dealer_blackjack = True


    hit = True
    while hit:
        clear_screen()
        print("Blackjack\n")
        print("Dealer Hand:")
        for item in cards.get_card_visuals(dealer_hand):
            print(item)
        dealer_total = cards.get_hand_total(dealer_hand)
        print("Total: ???\n\n")

        print("Player Hand:")
        for item in cards.get_card_visuals(hand):
            print(item)
        total = cards.get_hand_total(hand)
        print(f"Total: {total}\n\n")

        if dealer_blackjack or blackjack or dealer_total > 21 or total > 21:
            break
        
        # Gets whether the player wants to hit or not
        hit_string = s_input(prompt="Do you want to [H]it or [S]tand? ", accepted_inputs=["h", "s"], fail_message="Please input 'h' or 's' for hit or stand.\n")
        if hit_string == "s":
            hit = False
        else:
            hand.append(cards.deal_card())

    # Dealer hits as long as their hand total is less than 17
    while dealer_total < 17:
        dealer_hand.append(cards.deal_card())
        dealer_total = cards.get_hand_total(dealer_hand)

    clear_screen()
    print("Blackjack\n")

    # Print Dealer Hand
    print("Dealer Hand:")
    for item in cards.get_card_visuals(dealer_hand, show_full_cards=True, all_cards_visible=True):
        print(item)
    print(f"Total: {dealer_total}\n\n")

    # Print Player Hand
    print("Player Hand:")
    for item in cards.get_card_visuals(hand, show_full_cards=True):
        print(item)
    print(f"Total: {total}\n\n")

    # Print whoever wins
    if total > 21 or (dealer_total >= total and dealer_total < 22):
        print("Dealer Wins!")
    else:
        print("You Win!")





playing = True
while playing:
    game()
    user_input = s_input("Play Again? [Y/N] ", ["y", "n"])
    playing = user_input == "y"