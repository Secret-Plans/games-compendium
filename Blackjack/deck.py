"""
Card Deck Simulation
Damon Jones
"""

# Imports
import random


# Card Deck class (Rest of file)
class Deck:
    """Simulates a deck of cards.

    This class is made to be more modular than is needed for Blackjack, as I may use
    this for other games in this internal and possibly other projects outside of
    class.
    """

    def __init__(self, letter_values : dict = {"A": "1", "J": "11", "Q": "12", "K": "13"}, include_jokers : bool = False) -> None:
        self.cards = []
        self.letter_values = letter_values #The intger values that aces and picture cards represent
        self.include_jokers = include_jokers #Whether or not the deck contains jokers

        self.card_front = [
            "┌─────────┐",
            "│V        │",
            "│         │",
            "│    S    │",
            "│         │",
            "│        V│",
            "└─────────┘"
        ] #Texture for the card's front

        self.card_back = [
            "┌─────────┐",
            "│▒▒▒▒▒▒▒▒▒│",
            "│▒▒▒▒▒▒▒▒▒│",
            "│▒▒▒▒▒▒▒▒▒│",
            "│▒▒▒▒▒▒▒▒▒│",
            "│▒▒▒▒▒▒▒▒▒│",
            "└─────────┘"
        ] #Texture for the card's back

        self.make_deck()
    
    def make_deck(self) -> None:
        """Initializes the deck of cards.
        """
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] #The values on the cards
        suits = ["S", "H", "D", "C"] #The suits of the cards (Spades, Hearts, Diamonds, Clubs)
        
        cards = []

        for suit in suits:
            for value in values:
                cards.append(f"{value}:{suit}")
        
        if self.include_jokers:
            cards.append("T:B") #Black Joker (identifier means Trump Black)
            cards.append("T:R") #Red Joker   (identifier means Trump Red)

        random.shuffle(cards)
        self.cards = cards


    def translate_card_value(self, value : str) -> int:
        """Translates the string value of a card into it's actual integer value.

        

        Args:
            value (str): The value to be translated.

        Returns:
            int: The actual integer value of the card.
        """

        if value in self.letter_values:
            return self.letter_values[value]
        return int(value)


    def get_card_value(self, card : str) -> str:
        """Gets the value of the card.

        The value returned by the function is not the actual value, but rather the
        string representation of it, i.e: A King would return 'K' rather than its
        actual integer value. Number cards such as '2' will still return a string of
        that number rather than its integer value.

        Args:
            card (str): The card to get the value from.

        Returns:
            str: The card value.
        """

        split_card_values = card.split(":")
        return split_card_values[0]
    

    def get_card_suit(self, card : str) -> str:
        """Gets the suit of the card.

        The value returned by the function is not the actual value, but rather the
        string representation of it, i.e: A Spades would return "S" rather than the
        correct character. Get card visuals automatically prints the correct character
        using a dictionary with the unicode card suit characters.

        Args:
            card (str): The card to get the value from.

        Returns:
            str: The card suit.
        """

        split_card_values = card.split(":")
        return split_card_values[1]


    def get_card_visible(self, card : str) -> bool:
        """Gets whether the card is visible or not.

        Used to determine whether to print the card back texture or card front texture.

        Args:
            card (str): The card to get the value from.

        Returns:
            bool: Whether or not the front is visible.
        """

        split_card_values = card.split(":")
        if split_card_values[2] == "Y":
            return True
        return False


    def get_card_visuals(self, hand, show_full_cards : bool = False, all_cards_visible : bool = False) -> list:
        """Returns a list of strings to be printed based off of the deck of cards.

        Args:
            show_full_cards (bool, optional): Whether or not to show the full texture of every card. Defaults to False.
            all_cards_visible (bool, optional): Whether or not to show all cards as being turned or not.

        Returns:
            list: List of strings to be printed representing a hand of cards.
        """

        suit_visuals = {"S": "♠", "H": "♥", "D": "♦", "C": "♣", "B": "☻", "R": "☺"}
        lines = []
        for i in range(7):
            s = ""
            for card_index in range(len(hand)):
                strlen = 11
                temp_s = ""
                if card_index != len(hand) - 1 and not show_full_cards:
                    strlen = 5
                
                if not self.get_card_visible(hand[card_index]) and not all_cards_visible:
                    temp_s = self.card_back[i]
                else:
                    temp_s = self.card_front[i]

                    if "V" in self.card_front[i]:
                        temp_s = temp_s.replace("V ", self.get_card_value(hand[card_index]).ljust(2, " "))
                        temp_s = temp_s.replace(" V", self.get_card_value(hand[card_index]).rjust(2, " "))
                    
                    elif "S" in self.card_front[i]:
                        temp_s = temp_s.replace("S", suit_visuals[self.get_card_suit(hand[card_index])])

                s += temp_s[:strlen]

            lines.append(s)
        return lines

    
    def deal_card(self, card_visible : bool = True) -> str:
        """Pops the top card off the deck.

        Args:
            card_visible (bool, optional): Whether or not the card's front is visible. Defaults to True.

        Returns:
            str: A str representing the card's data (value:suit:visible).
        """
        card = self.cards.pop()
        if card_visible:
            return card + ":" + "Y"
        return card + ":" + "N"

    
    def get_hand_total(self, hand : list) -> int:
        """Calculates the total integer value of a hand.

        Args:
            hand (list): The hand to be calculated.

        Returns:
            int: The total value of the hand.
        """
        total = 0
        for item in hand:
            total += self.translate_card_value(self.get_card_value(item))
        return total