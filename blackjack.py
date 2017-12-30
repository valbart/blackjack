import random
import os
import math
import blackjack_mdp

def init_deck(deck, nb_paquets):
    for i in range(nb_paquets):
        for j in range(1,14):
            for k in range(4):
                deck.append(j)
    random.shuffle(deck)

def draw_card(deck):
    return deck.pop(0)

# def value(deck):
#     val = 0
#     for e in deck:
#         if e != 1 : val += min(e, 10)
#     nb_as = deck.count(1)
#     if val > 10: val += nb_as
#     if nb_as > 0:
#         val += 11
#         for i in range(1, nb_as): val += 1
#         if val > 21:
#             val -= 11
#             for i in range(1, nb_as): val -= 1
#             val += nb_as
#     return val

def value(deck):
    val = 0
    for e in deck: val += min(e, 10)
    return val

def begin_turn(main_deck, dealer_deck, player_deck, card_count):
    player_deck.append(draw_card(main_deck))
    dealer_deck.append(draw_card(main_deck))
    player_deck.append(draw_card(main_deck))
    for c in player_deck: card_count.append(c)
    for c in dealer_deck: card_count.append(c)


def dealer_play(main_deck, dealer_deck):
    while(value(dealer_deck) < 17):
        if len(main_deck) == 0: return
        dealer_deck.append(draw_card(main_deck))

def print_situation(dealer_deck, player_deck):
    print("First card of dealer: " + str(dealer_deck[0]) + "\n")
    print("Your deck " + str(player_deck) + " has value " + str(value(player_deck)) + "\n")

def print_final_situation(dealer_deck, player_deck):
    print("Dealer deck " + str(dealer_deck) + " has value " + str(value(dealer_deck)) + "\n")
    print("Your deck " + str(player_deck) + " has value " + str(value(player_deck)) + "\n")

def play_turn(main_deck, dealer_deck, player_deck, card_count):
    dealer_deck.clear()
    player_deck.clear()
    begin_turn(main_deck, dealer_deck, player_deck, card_count)
    print_situation(dealer_deck, player_deck)
    auto_play(main_deck, player_deck, dealer_deck, card_count)
    #player_play(main_deck, player_deck, card_count)
    #auto_play_mdp(main_deck, player_deck, dealer_deck, 10)
    if (value(player_deck) > 21) :
        print("You lose\n")
        return -1
    print_situation(dealer_deck, player_deck)
    dealer_play(main_deck, dealer_deck)
    for c in dealer_deck[2:]: card_count.append(c)
    print_final_situation(dealer_deck, player_deck)
    if (value(dealer_deck) > 21):
        print("Dealer is above 21, you win")
        return 1
    if (value(player_deck) > value(dealer_deck)):
        print("You win\n")
        return 1
    elif (value(player_deck) < value(dealer_deck)):
        print("You lose\n")
        return -1
    else:
        print("It's a draw\n")
        return 0

def play_game(main_deck, dealer_deck, player_deck, money, betting_unit):
    card_count = []
    while(len(main_deck) >= 10 and money > 0):
        print("Your current balance: " + str(money) + "\n")
        #bet = int(input("How much to bet? "))
        #bet = auto_bet(main_deck, card_count, money, betting_unit)
        bet = 10
        if bet > money:
            bet = money
        res = play_turn(main_deck, dealer_deck, player_deck, card_count)
        money += res*bet
        print("Current TC: " + str(compute_tc(main_deck, card_count)) + "\n")
    if money == 0:
        print("You lost the game\n")
    print ("\n\n Final balance: " + str(money))
    return money

def player_play(main_deck, player_deck, card_count):
    choice = 'd'
    while (value(player_deck) < 21):
        if len(main_deck) == 0: return
        print("Your current deck: " + str(player_deck) + " has value " + str(value(player_deck)) + "\n")
        choice = input("Next move? ")

        if (choice == 'd'):
            card = draw_card(main_deck)
            card_count.append(card)
            print("Current TC: " + str(compute_tc(main_deck, card_count)) + "\n")
            player_deck.append(card)
            print("You draw card " + str(card) + "\n")
        else:
            break

def hilo_value(card):
    if card in [7,8,9]: return 0
    if card in [1, 10, 11, 12, 13]: return -1
    return 1

def compute_tc(main_deck, card_count):
    RC = 0
    for c in card_count: RC+= hilo_value(c)
    if len(main_deck) == 0: return RC
    return RC/(math.ceil(len(main_deck)/52))

def basic_strategy(player_deck, dealer_deck):
    if (value(player_deck) >= 17): return 0
    if (value(player_deck) >= 13):
        if (dealer_deck[0] <= 6): return 0
        return 1
    if (value(player_deck) == 12):
        if (dealer_deck[0] in [4,5,6]): return 0
    return 1

# def basic_strategy(player_deck, dealer_deck):
#     while(value(player_deck) < 17): return 1
#     return 0

def auto_play(main_deck, player_deck, dealer_deck, card_count):
    while (value(player_deck) < 21 and basic_strategy(player_deck, dealer_deck) != 0):
        print("Your current deck: " + str(player_deck) + " has value " + str(value(player_deck)) + "\n")
        if len(main_deck) == 0: return
        card = draw_card(main_deck)
        card_count.append(card)
        player_deck.append(card)
        print("You draw card " + str(card) + "\n")

def auto_play_mdp(main_deck, player_deck, dealer_deck, bet):
    choice = blackjack_mdp_pdf.compute_optimal_policy(value(dealer_deck), value(player_deck), bet, main_deck)
    while (value(player_deck) < 21 and value(player_deck) not in choice[1]):
        print("Your current deck: " + str(player_deck) + " has value " + str(value(player_deck)) + "\n")
        if len(main_deck) == 0: return
        card = draw_card(main_deck)
        card_count.append(card)
        player_deck.append(card)
        choice = blackjack_mdp_pdf.compute_optimal_policy(value(dealer_deck), value(player_deck), bet, main_deck)
        print("You draw card " + str(card) + "\n")

def auto_bet(main_deck, card_count, money, betting_unit):
    tc = compute_tc(main_deck, card_count)
    if tc < 3: return 1
    return 100
    #if tc-1 <= 0: return 1
    #return (tc-1)*betting_unit

def heat_deck(main_deck, card_count):
    while (compute_tc(main_deck, card_count) < 3):
        if len(main_deck) == 0: return
        card_count.append(main_deck.pop(0))

if __name__ == '__main__':
    main_deck = []
    player_deck = []
    dealer_deck = []
    final_balance = []
    card_count = []
    played_games = 0
    win = 0
    draw = 0
    lose = 0

    ## TEST OF MDP POLICY
    for i in range(100):
        main_deck = []
        player_deck = []
        dealer_deck = []
        final_balance = []
        card_count = []
        init_deck(main_deck, 6)
        for t in range(len(main_deck) - 10):
            main_deck.pop(0)
        while len(main_deck) >= 10:
            played_games += 1
            game = play_turn(main_deck, dealer_deck, player_deck, card_count)
            if game == 1: win += 1
            if game == 0: draw += 1
            if game == -1: lose += 1

    print(str(win))
    print(str(draw))
    print(str(lose))
    print(str(played_games))
    print(str(round(win/played_games, 2)))


    ## TEST OF HI-LO COUNTING :
    ## Heat deck to reach hi-tc
    ## See if higher chance of winning
    # for i in range(10000):
    #     main_deck = []
    #     player_deck = []
    #     dealer_deck = []
    #     final_balance = []
    #     card_count = []
    #     init_deck(main_deck, 6)
    #     heat_deck(main_deck, card_count)
    #     if len(main_deck) != 0 and len(main_deck) <= 3*52:
    #         played_games += 1
    #         game = play_turn(main_deck, dealer_deck, player_deck, card_count)
    #         if game == 1: win += 1
    #         if game == 0: draw += 1
    #         if game == -1: lose += 1
    #
    # print(str(win))
    # print(str(draw))
    # print(str(lose))
    # print(str(played_games))
    # print(str(round(win/played_games, 2)))
