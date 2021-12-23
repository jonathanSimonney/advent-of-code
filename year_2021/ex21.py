from typing import TypedDict


class PlayerDict(TypedDict):
    player_score: int
    player_pos: int


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


def roll_deterministic_dice() -> int:
    global deterministic_dice_next_roll

    val_to_ret = deterministic_dice_next_roll
    deterministic_dice_next_roll = (deterministic_dice_next_roll + 1) % 100

    return 100 if val_to_ret == 0 else val_to_ret


deterministic_dice_next_roll = 1


def main():
    player_one: PlayerDict = {
        'player_pos': 3,
        'player_score': 0
    }

    player_two: PlayerDict = {
        'player_pos': 7,
        'player_score': 0
    }

    nb_turn_played = 0
    is_player_one_turn = True
    while True:
        nb_turn_played += 1
        ongoing_player: PlayerDict = player_one if is_player_one_turn else player_two
        play_turn_one_player(ongoing_player)
        if ongoing_player['player_score'] >= 1000:
            loosing_player: PlayerDict = player_two if is_player_one_turn else player_one
            break
        is_player_one_turn = not is_player_one_turn

    print(loosing_player['player_score'] * nb_turn_played * 3)


if __name__ == "__main__":
    main()
