
import random


class Pond():
    def __init__(self):
        self.coats = ("C", "S", "H", "D")
        self.card_numbers = ("2", "3", "4", "5", "6", "7", "8",
                             "9", "10", "J", "Q", "K", "A")
        self.create_deck()

    def print(self):
        print_str = ""
        for each in self.deck:
            print(each)
            print_str += self.deck[each]
            return print_str

    def create_deck(self):
        self.deck = []
        for card_number in self.card_numbers:
            for coat in self.coats:
                self.deck.append((card_number, coat))
        random.shuffle(self.deck)


class Player():
    def __init__(self, size_of_hands, pond, player_number, number_of_players) -> None:

        self.memory = [set() for i in range(0, number_of_players)]

        self.player_number = player_number
        if player_number == 0:
            self.player_name = "Player"
        else:
            self.player_name = "Computer " + str(player_number)

        self.hand = []
        self.create_hand(size_of_hands, pond)

    def print_hand(self):
        print(self.player_name, "hand:", self.hand)

    def print_memory(self):
        print(self.player_name, ":", self.memory)

    def create_hand(self, size_of_hands, pond):
        for i in range(0, size_of_hands):
            self.hand.append(pond.deck.pop())

    def sort_hand(self):
        self.hand.sort()

    def check_for_matches(self, selected_card):
        matched_cards = []
        for each in self.hand:
            if (selected_card in each):
                matched_cards.append(each)
        return matched_cards

    # TODO: refactor this, not good to return 2 values from method
    def check_memory(self, players, current_player, testing):
        for each in self.hand:
            for player in self.memory:
                for card_number in player:
                    if card_number in each and self.memory.index(player) != current_player:
                        if testing:
                            print("Found current player card {0} in memory for player {1}.".format(
                                card_number, self.memory.index(player)))
                        return [self.memory.index(player), card_number]
        return None

    def remove_card_from_all_memory(self, four_of_kind_card):
        for player in self.memory:
            if four_of_a_kind_check in player:
                player.remove(four_of_kind_card)


def wait_for_player():
    while True:
        input("Press enter to continue...")
        break


def get_number_of_players(manual=None):
    if manual:
        return manual
    while True:
        number_of_players = int(
            input("How many computer players would you like (1-3): "))
        if number_of_players in range(1, 4):
            number_of_players += 1  # because input is for computer players
            break
        print("That is not a valid selection")
    return number_of_players


def get_hand_size(manual=None):
    if manual:
        return manual
    while True:
        size_of_hands = int(
            input("What hand size would you like each player to start with (5-7): "))
        if size_of_hands in range(5, 8):
            break
        print("That is not a valid selection")
    return size_of_hands


def get_card_from_user(card_numbers, hand):

    cards_in_hand = []
    for each in hand:
        cards_in_hand.append(each[0])

    while True:
        selected_card = input(
            "Which card number would you like to guess (2 to A)?: ")
        selected_card = selected_card.upper()
        cards_in_hand
        if (selected_card in card_numbers) and (selected_card in cards_in_hand):
            return selected_card
        print("Input must be a valid card and in your hand.")


def get_selected_player_from_user(number_of_players, current_player):
    while True:
        selected_player = int(input(
            "Which player would you like to fish from (1 to {0})?:  ".format(number_of_players - 1)))
        if selected_player in range(1, number_of_players) and selected_player != current_player:
            return selected_player
        print("That is an invalid player number")


def get_largest_hand_player(players, current_player):
    largest_hand_player = 0
    largest_hand = 0
    for each in players:
        if len(each.hand) >= largest_hand and players.index(each) != current_player:
            largest_hand_player = each.player_number
            largest_hand = len(each.hand)
    return largest_hand_player


def four_of_a_kind_check(players, current_player):
    previous_card = None
    matcher = None
    for each in players[current_player].hand:
        if each[0] == previous_card:
            matcher += 1
            previous_card = each[0]
        else:
            matcher = 0
            previous_card = each[0]

        if matcher == 3:
            print("Player {0} has 4 X {1}'s!".format(
                current_player, each[0]))
            remove_four_of_kind(players, current_player, each[0])
            return each[0]


def remove_four_of_kind(players, current_player, four_of_kind_card):
    j = len(players[current_player].hand)
    i = 0
    # could not use list remove method because it would remove and shift to the next, skipping card checks
    while i != j and (len(players[current_player].hand) != 0):
        if players[current_player].hand[i][0] == four_of_kind_card:
            players[current_player].hand.remove(
                players[current_player].hand[i])
            j -= 1
        else:
            i += 1
    for player in players:
        player.remove_card_from_all_memory(four_of_kind_card)


def check_win_condition(players, current_player):
    if len(players[current_player].hand) == 0:
        print("Player {0} has no cards left and wins the game!".format(
            current_player))
        # wait_for_player()
        return True
    return False


def go_fish_action(pond, players, current_player):
    if len(pond.deck) != 0:
        print("No Match! Go fish!")
        fished_card = pond.deck.pop()
        if current_player == 0:
            print("{1} fished a {0}".format(fished_card,
                                            players[current_player].player_name))
        players[current_player].hand.append(fished_card)
    else:
        print("No Match! No more cards in the pond!")


def swap_cards_action(selected_player, selected_card, current_player, matched_cards, players):
    print("Player {0} gave Player {1}".format(
        selected_player, current_player), ":", len(matched_cards), "X", selected_card, "'s")
    for match in matched_cards:
        players[current_player].hand.append(match)
        players[selected_player].hand.remove(match)
    # add remove card from memory
    for player in players:
        if selected_card in player.memory[selected_player]:
            player.memory[selected_player].remove(selected_card)
