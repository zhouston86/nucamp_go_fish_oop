import random
import go_fish_modules
import time

from go_fish_modules import Pond
from go_fish_modules import Player


def program():
    # set for testing/debug mode. Will show debug data and make user player into computer player. Set turn_rate for duration for each turn, or -1 to manually control turn end
    testing = False
    turn_rate = 0.0

    # set for demo of code, where you can see all players hands, but user is still playing'
    demo = False

    # initiate game by selecting number of cards in hand and number of players
    print("\n§~~~~ Welcome to Go Fish! ~~~~§")
    if testing:
        print("You are in testing mode")
    if demo:
        print("You are in demo mode")

    if testing:
        number_of_players = go_fish_modules.get_number_of_players(3)
        size_of_hands = go_fish_modules.get_hand_size(6)
    else:
        number_of_players = go_fish_modules.get_number_of_players()
        size_of_hands = go_fish_modules.get_hand_size()

    pond = Pond()
    # print(pond.deck)

    players = []

    # create list of players class objects
    for i in range(0, number_of_players):
        player = Player(size_of_hands, pond, i, number_of_players)
        players.append(player)

    # initalize some things
    matched_cards = []
    turn_counter = 0
    game_end = False
    current_player = 0

    for each in players:
        each.sort_hand()

    while game_end == False:
        turn_counter += 1

        selected_card = None
        has_memory = None
        matched_cards.clear()

        if testing or demo and current_player == 0:
            print("\ndebug: Current Players Hands")
            for each in players:
                each.print_hand()

        """If User Turn"""

        if current_player == 0 and not testing:

            print("\n§~~~~ Your Turn! ~~~~§")

            # added in case player hand emptied during other players turn
            if go_fish_modules.check_win_condition(players, current_player):
                print("Game finished in", turn_counter, "turns!")
                return True

            players[current_player].print_hand()

            for player in players:
                print(player.player_name, "has", len(player.hand), "cards.")

            selected_card = go_fish_modules.get_card_from_user(
                pond.card_numbers, players[current_player].hand)

            selected_player = go_fish_modules.get_selected_player_from_user(
                number_of_players, current_player)

        """If Computer Turn"""
        if current_player != 0 or testing:

            print("\n§~~~~ Computer Player {0}'s Turn! ~~~~§".format(
                current_player))

            # added in case player hand emptied during other players turn
            if go_fish_modules.check_win_condition(players, current_player):
                print("Game finished in", turn_counter, "turns!")
                return True

            has_memory = players[current_player].check_memory(
                players, current_player, testing)

            if has_memory is None:
                if testing:
                    print("no player cards found in memory.")
                selected_card = random.choice(
                    players[current_player].hand)[0]
                selected_player = go_fish_modules.get_largest_hand_player(
                    players, current_player)
            else:
                selected_player = has_memory[0]
                selected_card = has_memory[1]

        """Swap hands and go fish functions"""

        matched_cards = players[selected_player].check_for_matches(
            selected_card)

        print("Player {0} asks Player {1} for {2}'s".format(
            current_player, selected_player, selected_card))

        for each in players:
            each.memory[current_player].add(selected_card)

        if not matched_cards:
            go_fish_modules.go_fish_action(pond, players, current_player)
        else:
            go_fish_modules.swap_cards_action(
                selected_player, selected_card, current_player, matched_cards, players)

        if testing:
            players[current_player].print_memory()

        """End turn functions"""
        for each in players:
            each.sort_hand()

        four_of_kind_card = None
        four_of_kind_card = go_fish_modules.four_of_a_kind_check(
            players, current_player)

        if go_fish_modules.check_win_condition(players, current_player):
            print("Game finished in", turn_counter, "turns!")
            file = open("turn_counter.csv", "a")
            file.write("\n" + str(turn_counter))
            file.close()
            game_end = True

        if four_of_kind_card == None:
            current_player += 1
            if current_player >= number_of_players:
                current_player = 0
        elif not game_end:
            print("Player {0} sets down 4 of a kind and gets to go again!".format(
                current_player))

        if testing and turn_rate != -1:
            time.sleep(turn_rate)
        else:
            go_fish_modules.wait_for_player()


if __name__ == '__main__':
    program()
