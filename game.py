# Imports
import random
from os import system, name
from time import sleep

# Global variables
players_count = 0
players_decks = []
players = []

open_pile = []
closed_pile = []
constraint = None

# Helper functions
def cinput(text, type):
    input_value = input('- ' + text + '\n> ')
    if type == 'int':
        return int(input_value)
    else:
        return input_value

def clear():
    if name == 'nt': # for windows
        _ = system('cls')
    else: # for mac and linux(here, os.name is 'posix')
        _ = system('clear')

# Game functions

def matches(last_card, card):
    global open_pile

    if last_card[0] == card[0] or last_card[1] == card[1]:
        open_pile.append(card)
        return True
    else:
        return False

def select_type():
    clear()
    print('You can choose a new card type!\n\n')
    print('These are your card options:\n')
    print('(1) ♥  (2) ♣  (3) ♦  (4) ♠')

    option = cinput('Choose', 'int')
    if option == 1:
        return 'hearts'
    elif option == 2:
        return 'clubs'
    elif option == 3:
        return 'diamonds'
    elif option == 4:
        return 'spades'

def special(card):
    if card[1] == 'A':
        return select_type()
    elif card[1] == '7':
        return 'take_two'
    elif card[1] == '8':
        return 'play_again'
    elif card[1] == '9':
        return 'skip'
    else:
        return 'none'

def fill_closed():
    global closed_pile
    global open_pile

    temp = open_pile.pop()
    closed_pile = open_pile
    open_pile = temp

def draw_card(p_deck):
    global closed_pile

    if len(closed_pile) < 1:
        fill_closed()

    card = closed_pile.pop()
    p_deck.append(card)

    return p_deck

def turn(p_name, p_deck):
    global open_pile
    global constraint

    clear()

    last_card = open_pile[-1]

    print('It\'s ' + p_name + '\'s turn!\n\n')
    print('Last Card: ' + last_card[0] + last_card[1])

    if constraint:
        print('Warning! There is a constraint caused by the previous player.\n')
        print('The new last card is: ' + constraint + last_card[1])

    print('\n\n')
    print('These are your card options:\n')

    options = []
    for i in range(len(p_deck)):
        options.append('(' + str(i+1) + ') ' + p_deck[i][0] + p_deck[i][1])

    print('(0) Draw a card from the closed pile')
    print('  '.join(options))

    print('\n')
    option = cinput('Choose', 'int')

    if option == 0:
        p_deck = draw_card(p_deck)
        o = len(options)
    else:
        o = option - 1

    card = p_deck[o]

    if constraint:
        last_card = (constraint, last_card[1], last_card[2])
        constraint = None

    if matches(last_card, card):
        p_deck.remove(card)

        action = special(card)

        if action == 'play_again':
            turn(p_name, p_deck)
        else:
            return [p_deck, action]
    else:
        clear()
        print('The selected card does not follow the game\'s sequence.\nPlease try again.')
        sleep(3)
        turn(p_name, p_deck)

def game():
    global players
    global players_count
    global players_decks
    global constraint

    prev_action = None

    for i in range(players_count):

        if prev_action == 'take_two':
            players_decks[i] = draw_card(players_decks[i])
            players_decks[i] = draw_card(players_decks[i])
            prev_action = None
        elif prev_action == 'skip':
            prev_action = None
            continue

        result = turn(players[i], players_decks[i])

        p_deck = result[0]
        action = result[1]

        players_decks[i] = p_deck

        if action == 'take_two' or action == 'skip':
            prev_action = action
        elif action == 'hearts':
            constraint = '♥'
        elif action == 'clubs':
            constraint = '♣'
        elif action == 'diamonds':
            constraint = '♦'
        elif action == 'spades':
            constraint = '♠'
        
    game()

def create_deck():
    deck = [
        ('♥', 'A', 11), ('♥', '2', 2), ('♥', '3', 3), ('♥', '4', 4), ('♥', '5', 5), ('♥', '6', 6), ('♥', '7', 7), ('♥', '8', 8), ('♥', '9', 9), ('♥', '10', 10), ('♥', 'J', 10), ('♥', 'Q', 10), ('♥', 'K', 10),
        ('♣', 'A', 11), ('♣', '2', 2), ('♣', '3', 3), ('♣', '4', 4), ('♣', '5', 5), ('♣', '6', 6), ('♣', '7', 7), ('♣', '8', 8), ('♣', '9', 9), ('♣', '10', 10), ('♣', 'J', 10), ('♣', 'Q', 10), ('♣', 'K', 10),
        ('♦', 'A', 11), ('♦', '2', 2), ('♦', '3', 3), ('♦', '4', 4), ('♦', '5', 5), ('♦', '6', 6), ('♦', '7', 7), ('♦', '8', 8), ('♦', '9', 9), ('♦', '10', 10), ('♦', 'J', 10), ('♦', 'Q', 10), ('♦', 'K', 10),
        ('♠', 'A', 11), ('♠', '2', 2), ('♠', '3', 3), ('♠', '4', 4), ('♠', '5', 5), ('♠', '6', 6), ('♠', '7', 7), ('♠', '8', 8), ('♠', '9', 9), ('♠', '10', 10), ('♠', 'J', 10), ('♠', 'Q', 10), ('♠', 'K', 10)
    ]
    random.shuffle(deck)
    return deck

def handle_deck():
    global players_count
    global players_decks
    global open_pile
    global close_pile

    deck = create_deck()
    for i in range(players_count):

        p_deck = []
        for i in range(7):
            p_deck.append(deck.pop())

        players_decks.append(p_deck)
    
    open_pile.append(deck.pop())
    closed_pile = deck

    game()

def start():
    global players_count
    global players

    clear()
    while players_count < 2 or players_count > 7:
        players_count = cinput('How many players will be playing?', 'int')
        if players_count < 2 or players_count > 7:
            print('\nThere must be at least 2 players and no more than 7 to play Agony.')
            sleep(2)
        clear()

    for i in range(players_count):
        players.append(cinput('Player #' + str(i+1) + ' name:', 'str'))
        clear()
    players.sort()
    handle_deck()

def main():
    print('Welcome to the Agony Game!\n\nAre you ready to play?')
    #sleep(2)
    start()

main()
