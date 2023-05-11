"""SIMPLE VIDEO POKER"""

import random as r


class Card(object):
    def __init__(self, name, value, suit, symbol):
        self.value = value
        self.suit = suit
        self.name = name
        self.showing = False
        self.symbol = symbol

    def __repr__(self):
        if self.showing:
            return self.symbol
        else:
            return "Card"


class Deck(object):
    def shuffle(self):
        r.shuffle(self.cards)
        print("Deck shuffled")

    #   Popping the top card from the list of cards hence dealing it
    def deal(self):
        return self.cards.pop(0)


class StandardDeck(Deck):
    def __init__(self):
        self.cards = []
        suits = {"Hearts": "♥", "Spades": "♠", "Diamonds": "♦", "Clubs": "♣"}
        # 11 to 14 are the face cards 'J,Q,K,A' respectively
        values = {"2": 2, "3": 3, "4": 4,
                  "5": 5, "6": 6, "7": 7,
                  "8": 8, "9": 9, "10": 10,
                  "J": 11, "Q": 12, "K": 13,
                  "A": 14}
        for name in values:
            for suit in suits:
                symbol_icon = suits[suit]
                if values[name] < 11:
                    symbol = str(values[name]) + symbol_icon
                else:
                    symbol = name + symbol_icon
                self.cards.append(Card(name, values[name], suit, symbol))

    def __repr__(self):
        return f"Standard deck of cards: {len(self.cards)} remaining"


class Player(object):
    def __init__(self):
        self.cards = []

    def no_of_cards(self):
        return len(self.cards)

    def addCard(self, card):
        self.cards.append(card)


class Scorer(object):
    def __init__(self, cards):
        # # Number of cards
        # if not len(cards) == 5:
        #     return 'Error! Wrong number of cards'
        self.cards = cards

    def flush(self):
        suits = [card.suit for card in self.cards]
        if len(set(suits)) == 1:
            return True
        else:
            return False

    def straight(self):
        values = [card.value for card in self.cards]
        values.sort()

        if not len(set(values)) == 5:
            return False

        # If it's an ace low straight, highest value= 5
        if values[4] == 14 and values[0] == 2 and values[1] == 3 and values[2] == 4 and values[3] == 5:
            return 5

        else:
            if not values[0] + 1 == values[1]:
                return False
            if not values[1] + 1 == values[2]:
                return False
            if not values[2] + 1 == values[3]:
                return False
            if not values[3] + 1 == values[4]:
                return False

        return values[4]

    def highCard(self):
        values = [card.value for card in self.cards]
        high_card = None
        for card in self.cards:
            if high_card is None:
                high_card = card
            elif high_card.value < card.value:
                high_card = card

        return high_card

    def highestCount(self):
        count = 0
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) > count:
                count = values.count(value)
        return count

    def pairs(self):
        pairs = []
        values = [card.value for card in self.cards]
        # Counting the number of each value
        for value in values:
            if values.count(value) == 2 and value not in pairs:
                pairs.append(value)

        return pairs

    def four_of_a_kind(self):
        values = [card.value for card in self.cards]
        # Counting the number of each value
        for value in values:
            if values.count(value) == 4:
                return True

    # Full house is aThree of a kind with a pair
    def fullHouse(self):
        two = False
        three = False
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) == 2:
                two = True
            elif values.count(value) == 3:
                three = True

        if two and three:
            return True
        else:
            return False


def displayHelp():
    rules = """        Video Poker Rules
              Standard "table" poker hands are used*
              You're dealt five starting cards.
              You can choose to hold or discard any or all of your cards.
              All cards you choose to discard will be replaced in a single random draw.
              If your hand now matches any of the qualifying poker hands, you win the corresponding prize.
              In this version of the game you enter the money you want to use to play. Each round, $5 is deducted as a 
              bet.
                                
              As you might have deduced, you must have at least a pair of Jacks to get paid.
              Any hand of inferior value to a pair of Jacks is worthless while any hand of superior value pays out based
              on a predetermined pay scale.
                                
              Here are the typical payouts for this version of the game (be sure to check the actual payouts on your 
              specific machine at the time of playing):
              Royal Flush - 250x (with bonuses of 4000x or more when betting max credits)
              Straight Flush - 50x
              Four of a Kind - 25x
              Full House - 9x
              Flush - 6x
              Straight - 4x
              Three of a Kind - 3x
              Two Pair - 2x
              Pair of Jacks or Better - 1x\n\n"""

    print(rules)


def specialInput(prompt):
    action = input(prompt)
    if action == '--help' or action == '--HELP':
        print("         \nIT SEEMS LIKE YOU NEED HELP")
        # Show the help screen
        displayHelp()
        return specialInput(prompt)
    elif action == "--resume" or action == '--RESUME':
        print("         \nRESUMING GAME.....")
        # You can decide whether or not to do anything else here
        return specialInput(prompt)
    else:
        return action


help_prompt = "To use help enter '--help'. Enter '--resume' to continue the game"
print("\n\033[1m" + help_prompt + "\033[0m\n")
name = specialInput("Please enter your name: ")


def play():
    player = Player()

    print("\n\033[1m" + help_prompt + "\033[0m\n")

    # Initial amount of cash
    while True:
        try:

            cash = int(specialInput(f"{name}, Enter the money you want to use to play.(Minimum = $5): "))

            while cash < 5:
                cash = int(specialInput(f"{name}, the cash must be greater or equal to $5.PLease enter cash: "))

            break
        except ValueError:
            print("Please enter your value in numbers")

    # Cost per hand
    hand_cost = 5

    """For each round/hand we will need to shuffle cards, deal out cards, hold/pass, 
       score"""
    end = False

    print("\nVIDEO POKER\n")

    print(f"Welcome to Video Poker, {name}\n")

    while not end:

        print(f"{name}, You currently have ${cash}\n")

        # Each bet will be $5
        print("Bet placed, -$5\n")
        cash -= 5

        print(f"You now have : ${cash}\n")

        # discard = []
        deck = StandardDeck()
        deck.shuffle()
        print(" ")

        # Dealing out the cards
        for i in range(5):
            player.addCard(deck.deal())

        # Making the cards visible
        for card in player.cards:
            card.showing = True

        # Holding or passing
        valid_input = False

        while not valid_input:
            print("Your cards: \n")
            print(player.cards)
            print(" ")
            input_str = specialInput("Which cards do you want to discard? (i.e. 1, 2, 3...) \n *Just hit return to hold all: ")
            try:
                input_list = [int(i.strip()) for i in input_str.split(",") if i]

                print(f"You discarded the following cards: {input_list}\n")

                # for i in input_list:
                #     if i > 6:
                #         continue
                #     if i < 1:
                #         continue
                for i in input_list:
                    player.cards[i - 1] = deck.deal()
                    player.cards[i - 1].showing = True

                valid_input = True

            except:
                print("Input error! Remember to use commas to separate the cards you want to hold")

        print(player.cards)

        # Scores
        score = Scorer(player.cards)
        straight = score.straight()
        flush = score.flush()
        highest_count = score.highestCount()
        four_kind = score.four_of_a_kind()
        full_house = score.fullHouse()
        pairs = score.pairs()

        # Royal Flush

        if straight and flush and straight == 14:
            print("ROYAL FLUSH!!!")
            print("+$1250")
            cash += 1250
        # Straight Flush
        elif straight and flush:
            print("STRAIGHT FLUSH!")
            print("+$250")
            cash += 250
        # Four of a kind
        elif four_kind:
            print("FOUR OF A KIND!")
            print("+$125")
            cash += 125

        # Full House
        elif full_house:
            print("FULL HOUSE!")
            print("+$45")
            cash += 45
        # Flush
        elif flush:
            print("FLUSH!")
            print("+$30")
            cash += 30
        # Straight
        elif straight:
            print("STRAIGHT!")
            print("+$20")
            cash += 20
        # Three of a kind
        elif highest_count == 3:
            print("THREE OF A KIND!")
            print("+$15")
            cash += 15
        # Two pair
        elif len(pairs) == 2:
            print("TWO PAIR!")
            print("+$10")
            cash += 10
        # Jacks or better
        elif pairs and pairs[0] > 10:
            print("JACKS OR BETTER!")
            print("$+5")
            cash += 5

        else:
            print("\nYOU DIDN'T WIN THIS TIME!!")

        print(f"You now have: ${cash}")

        # Clearing the cards
        player.cards = []

        if cash < 5:
            print("Looks like you don't have any money to continue. Please enter some more cash")


        # Checking if the person wants to play again
        play_again = input("\nWould you like to play again? (Y/N): ").upper()

        if play_again == 'N':
            print(f"YOUR GO HOME WITH: {cash}")
            end = True

        print("\n")


play()
