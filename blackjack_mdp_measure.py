import random

def init_deck(deck, nb_paquets):
    for i in range(nb_paquets):
        for j in range(1,14):
            for k in range(4):
                deck.append(j)
    random.shuffle(deck)

## DEALER PROBABILITY OF WINNING ##

# Probability of dealer winning are known above 17:
# dealer draw if <= 16, stop otherwise. Hence if dealer >= 17
# and dealer < player dealer loses, and if dealer >= 17 and dealer
# < player dealer wins
# Probablity of dealer winning also known below 11: we must draw ?
def init_pr_dealer(score_to_beat):
    Pr_dealer = [0 for i in range(22)]
    for i in range(17, max(17, score_to_beat)): Pr_dealer[i] = 0
    for i in range(max(17, score_to_beat), 22): Pr_dealer[i] = 1
    return Pr_dealer

def compute_admissible_cards(current_score):
    admissible_cards = []
    for e in range(1,14):
        if (current_score + card_value(e)) <= 21: admissible_cards.append(e)
    return admissible_cards

def card_value(card):
    return min(card, 10)

def compute_proba_card(card, deck):
    return deck.count(card)/len(deck)

def compute_proba_value(value, deck):
    if value <= 9: return compute_proba_card(value)
    prob = 0
    for i in range(10, 14): prob += compute_proba_card(i, deck)
    return prob

def compute_proba_dealer_win(initial_dealer_score, score_to_beat, deck):
    if score_to_beat > 21: return 1 # We are above 21, dealer win
    Pr_dealer = init_pr_dealer(score_to_beat)
    admissible_cards = []
    value = 0
    for i in range(16, initial_dealer_score-1, -1): # Dealer draw at 16 or less
        admissible_cards = compute_admissible_cards(i)
        for card in admissible_cards:
            value = card_value(card)
            Pr_dealer[i] += Pr_dealer[i + value]*compute_proba_card(card, deck)
    return Pr_dealer[initial_dealer_score]


## OPTIMAL PLAY POLICY ##

def reward(current_hand_value, dealer_hand_value, bet, deck):
    #if current_hand_value > 21: return 0
    return bet*(2*(1-compute_proba_dealer_win(dealer_hand_value, current_hand_value, deck))-1)


def compute_proba_transition(x, y, deck):
    if (y <= x): return 0
    distance = y-x
    if distance > 10: return 0
    if distance <= 9: return compute_proba_card(distance, deck)
    return sum(compute_proba_card(card, deck) for card in range(10,14))


def compute_mean(V, current_hand_value, dealer_hand_value, deck, bet, action):
    if action == 1: return reward(current_hand_value, dealer_hand_value, bet, deck)
    mean = 0
    for y in range(current_hand_value+1, 30):
        mean += compute_proba_transition(current_hand_value, y, deck)*V[y]
    return mean

def compute_optimal_policy(dealer_hand_value, current_hand_value, bet, main_deck):
    V = [-1 for x in range(0, 30)]
    for i in range(21, 30):
        V[i] = reward(i, dealer_hand_value, bet, main_deck)
    policy = [-1 for i in range(0,30)]

    for x in range(20, current_hand_value-1, -1):
        mean_draw = compute_mean(V, x, dealer_hand_value, main_deck, bet, 0)
        mean_stay = compute_mean(V, x, dealer_hand_value, main_deck, bet, 1)
        V[x] = max(mean_stay, mean_draw)
        policy[x] = 0 if mean_draw > mean_stay else 1

    where_draw = []
    where_stay = []
    for i in range(len(policy)):
        if policy[i] == 0: where_draw.append(i)
        if policy[i] == 1: where_stay.append(i)
    choice = [where_draw, where_stay]
    return choice

if __name__ == '__main__':

    measures = [[0 for x in range(11)] for y in range(22)] # measures[myHand][dealerHand]
    measures_double = [[0 for x in range(11)] for y in range(22)] # measures[myHand][dealerHand]
    nbIter = 1000

    for myHand in range(2, 22):
        for dealerHand in range(1, 11):
            for i in range(nbIter):
                main_deck = []
                init_deck(main_deck, 6)
                r = random.randint(100,100)
                for i in range(r):
                    main_deck.pop(0)

                bet = 10
                dealer_hand_value = dealerHand
                current_hand_value = myHand

                V = [-1 for x in range(0, 30)]
                for i in range(21, 30):
                    V[i] = reward(i, dealer_hand_value, bet, main_deck)
                policy = [-1 for i in range(0,30)]

                V_double_bet = 0
                for y in range(0, 30):
                    V_double_bet += compute_proba_transition(current_hand_value, y, main_deck)*reward(y, dealer_hand_value, 2*bet, main_deck)

                for x in range(20, current_hand_value-1, -1):
                    mean_draw = compute_mean(V, x, dealer_hand_value, main_deck, bet, 0)
                    mean_stay = compute_mean(V, x, dealer_hand_value, main_deck, bet, 1)
                    V[x] = max(mean_stay, mean_draw)
                    policy[x] = 0 if mean_draw > mean_stay else 1

                if policy[myHand] == 0: measures[myHand][dealerHand] += 1
                if V_double_bet > V[current_hand_value]: measures_double[myHand][dealerHand] += 1

    matrix_str = ""
    matrix_str_double = ""
    for myHand in range(2, 22):
        for dealerHand in range(1, 11):
            measures[myHand][dealerHand] /= (nbIter/100)
            matrix_str += str(round(measures[myHand][dealerHand], 2))
            matrix_str += "  "
            measures_double[myHand][dealerHand] /= (nbIter/100)
            matrix_str_double += str(round(measures_double[myHand][dealerHand], 3))
            matrix_str_double += "  "
        matrix_str += "\n"
        matrix_str_double += "\n"

    print(matrix_str)
    print("\n\n")
    print(matrix_str_double)
