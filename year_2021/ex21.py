import collections
from typing import TypedDict


class PlayerDict(TypedDict):
    player_score: int
    player_pos: int


class Universe(TypedDict):
    player_one: PlayerDict
    player_two: PlayerDict


class ResultDict(TypedDict):
    nb_victory_player_one: int
    nb_victory_player_two: int


def play_turn_one_player(player: PlayerDict):
    acc_dice_result = 0
    # probably this is where I'll need to optimise for part 2
    for _ in range(3):
        acc_dice_result += roll_deterministic_dice()

    new_player_pos = get_pos_after_moving_n(acc_dice_result, player['player_pos'])
    player['player_score'] += new_player_pos
    player['player_pos'] = new_player_pos


def get_pos_after_moving_n(nb_moved: int, original_pos: int) -> int:
    result_pos = (nb_moved + original_pos) % 10

    return 10 if result_pos == 0 else result_pos


deterministic_dice_next_roll = 1


def roll_deterministic_dice() -> int:
    global deterministic_dice_next_roll

    val_to_ret = deterministic_dice_next_roll
    deterministic_dice_next_roll = (deterministic_dice_next_roll + 1) % 100

    return 100 if val_to_ret == 0 else val_to_ret


def compute_result_3_dirac_dices() -> dict[int, int]:
    dict_sum_result_to_nb_universe_concerned: dict[int, int] = collections.defaultdict(lambda : 0)

    for dice_1 in range(1, 4):
        for dice_2 in range(1, 4):
            for dice_3 in range(1, 4):
                dict_sum_result_to_nb_universe_concerned[dice_1 + dice_2 + dice_3] += 1

    return dict_sum_result_to_nb_universe_concerned


result_3_dirac_dices = compute_result_3_dirac_dices()


def play_turn_one_player_quantic(universe: Universe, is_turn_player_one: bool) -> ResultDict:
    possible_results = result_3_dirac_dices

    key_ongoing_player_dict = 'player_one' if is_turn_player_one else 'player_two'
    key_not_ongoing_player_dict = 'player_two' if is_turn_player_one else 'player_one'
    ongoing_player_dict: PlayerDict = universe[key_ongoing_player_dict]

    nb_victory_player_one = 0
    nb_victory_player_two = 0

    for sum_dice, nb_universe_concerned in possible_results.items():
        new_player_pos = get_pos_after_moving_n(sum_dice, ongoing_player_dict['player_pos'])

        new_universe_player_score = ongoing_player_dict['player_score'] + new_player_pos
        new_universe_player_pos = new_player_pos

        if new_universe_player_score >= 21:
            if is_turn_player_one:
                nb_victory_player_one += nb_universe_concerned
            else:
                nb_victory_player_two += nb_universe_concerned
            continue
        universe_player_dict: PlayerDict = {
            'player_pos': new_universe_player_pos,
            'player_score': new_universe_player_score
        }

        new_universe: Universe = {
            key_ongoing_player_dict: universe_player_dict,
            key_not_ongoing_player_dict: universe[key_not_ongoing_player_dict]
        }

        result_universe_local: ResultDict = play_turn_one_player_quantic(new_universe, not is_turn_player_one)

        nb_victory_player_one += result_universe_local['nb_victory_player_one'] * nb_universe_concerned
        nb_victory_player_two += result_universe_local['nb_victory_player_two'] * nb_universe_concerned

    return {'nb_victory_player_one': nb_victory_player_one, 'nb_victory_player_two': nb_victory_player_two}


def main():
    player_one: PlayerDict = {
        'player_pos': 3,
        'player_score': 0
    }

    player_two: PlayerDict = {
        'player_pos': 7,
        'player_score': 0
    }

    # nb_turn_played = 0
    # is_player_one_turn = True
    # while True:
    #     nb_turn_played += 1
    #     ongoing_player: PlayerDict = player_one if is_player_one_turn else player_two
    #     play_turn_one_player(ongoing_player)
    #     if ongoing_player['player_score'] >= 1000:
    #         loosing_player: PlayerDict = player_two if is_player_one_turn else player_one
    #         break
    #     is_player_one_turn = not is_player_one_turn
    #
    # print(loosing_player['player_score'] * nb_turn_played * 3)

    universe: Universe = {'player_one': player_one, 'player_two': player_two}

    # 70279471379670 too low
    print(play_turn_one_player_quantic(universe, True))


if __name__ == "__main__":
    main()
