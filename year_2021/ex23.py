import copy
from enum import Enum
from typing import Union


class AmphipodsTypes(Enum):
    A = 1
    B = 10
    C = 100
    D = 1000
    EMPTY_SPACE = 0


idx_left_room_a = 1
idx_left_room_b = 2
idx_left_room_c = 3
idx_left_room_d = 4


list_rooms_idx_moving_leftwards = [
            idx_left_room_d,
            idx_left_room_c,
            idx_left_room_b,
            idx_left_room_a
        ]

list_rooms_idx_moving_rightwards = [
            idx_left_room_d + 1,
            idx_left_room_c + 1,
            idx_left_room_b + 1,
            idx_left_room_a + 1
        ]


class AmphipodBurrow:
    room_a: list[AmphipodsTypes]
    room_b: list[AmphipodsTypes]
    room_c: list[AmphipodsTypes]
    room_d: list[AmphipodsTypes]
    hallway: list[AmphipodsTypes]

    def is_burrow_tidied(self) -> bool:
        return self.room_a == [AmphipodsTypes.A, AmphipodsTypes.A] \
               and self.room_b == [AmphipodsTypes.B, AmphipodsTypes.B] \
               and self.room_c == [AmphipodsTypes.C, AmphipodsTypes.C] \
               and self.room_d == [AmphipodsTypes.D, AmphipodsTypes.D]

    def debug_print(self):
        print("#############")
        print(f"#{self.hallway[0]}{self.hallway[1]}.{self.hallway[2]}.{self.hallway[3]}.{self.hallway[4]}.{self.hallway[5]}{self.hallway[6]}#")
        print(f"###{self.room_a[0]}#{self.room_b[0]}#{self.room_c[0]}#{self.room_d[0]}###")
        print(f"  #{self.room_a[1]}#{self.room_b[1]}#{self.room_c[1]}#{self.room_d[1]}#  ")
        print("  #########  ")


class BurrowMove:
    arrival_state: AmphipodBurrow
    move_cost: int

    def __init__(self, arrival_state: AmphipodBurrow, move_cost: int):
        self.arrival_state = arrival_state
        self.move_cost = move_cost


def compute_list_move_from_one_room_specific_pos(
        attribute_room_considered: str,
        type_amphipods_considered: AmphipodsTypes,
        nb_move_to_leave_room: int,
        idx_directly_left_of_room: int,
        starting_burrow: AmphipodBurrow
) -> list[BurrowMove]:
    acc_list: list[BurrowMove] = []

    nb_move_done: int = nb_move_to_leave_room

    for idx_move in range(idx_directly_left_of_room, -1, -1):
        if starting_burrow.hallway[idx_move] != AmphipodsTypes.EMPTY_SPACE:
            break
        nb_move_done += 1
        # should count properly the moves when passing in front of a room
        if idx_move != idx_directly_left_of_room and idx_move in list_rooms_idx_moving_leftwards:
            nb_move_done += 1

        local_burrow = copy.deepcopy(starting_burrow)
        local_burrow.hallway[idx_move] = type_amphipods_considered
        getattr(local_burrow, attribute_room_considered)[nb_move_to_leave_room - 1] = AmphipodsTypes.EMPTY_SPACE
        move_cost: int = nb_move_done * type_amphipods_considered.value

        acc_list.append(BurrowMove(local_burrow, move_cost))

    nb_move_done = nb_move_to_leave_room
    for idx_move in range(idx_directly_left_of_room + 1, 7):
        if starting_burrow.hallway[idx_move] != AmphipodsTypes.EMPTY_SPACE:
            break
        nb_move_done += 1
        # should count properly the moves when passing in front of a room
        if idx_move != idx_directly_left_of_room + 1 and idx_move in list_rooms_idx_moving_rightwards:
            nb_move_done += 1

        local_burrow = copy.deepcopy(starting_burrow)
        local_burrow.hallway[idx_move] = type_amphipods_considered
        getattr(local_burrow, attribute_room_considered)[nb_move_to_leave_room - 1] = AmphipodsTypes.EMPTY_SPACE
        move_cost: int = nb_move_done * type_amphipods_considered.value

        acc_list.append(BurrowMove(local_burrow, move_cost))

    return acc_list


def compute_move_to_one_room_specific_pos(
        attribute_room_considered: str,
        type_amphipods_considered: AmphipodsTypes,
        nb_move_to_reach_room_bottom: int,
        nb_move_to_reach_room_entrance: int,
        idx_hallway_from: int,
        starting_burrow: AmphipodBurrow
) -> BurrowMove:
    local_burrow = copy.deepcopy(starting_burrow)
    local_burrow.hallway[idx_hallway_from] = AmphipodsTypes.EMPTY_SPACE
    getattr(local_burrow, attribute_room_considered)[nb_move_to_reach_room_bottom - 1] = type_amphipods_considered
    move_cost: int = (nb_move_to_reach_room_bottom + nb_move_to_reach_room_entrance) * type_amphipods_considered.value

    return BurrowMove(local_burrow, move_cost)


def compute_list_move_from_and_to_one_room(
        attribute_room_considered: str,
        type_amphipods_considered: AmphipodsTypes,
        idx_directly_left_of_room: int,
        starting_burrow: AmphipodBurrow
) -> list[BurrowMove]:
    acc_list: list[BurrowMove] = []

    room_considered = getattr(starting_burrow, attribute_room_considered)

    if room_considered != [type_amphipods_considered, type_amphipods_considered]:
        if room_considered != [AmphipodsTypes.EMPTY_SPACE, type_amphipods_considered] and \
                room_considered != [AmphipodsTypes.EMPTY_SPACE, AmphipodsTypes.EMPTY_SPACE]:
            if room_considered[0] != AmphipodsTypes.EMPTY_SPACE:
                acc_list.extend(
                    compute_list_move_from_one_room_specific_pos(
                        attribute_room_considered,
                        type_amphipods_considered,
                        1,
                        idx_directly_left_of_room,
                        starting_burrow
                    )
                )
            else:
                acc_list.extend(
                    compute_list_move_from_one_room_specific_pos(
                        attribute_room_considered,
                        type_amphipods_considered,
                        2,
                        idx_directly_left_of_room,
                        starting_burrow
                    )
                )
        else:
            nb_move_to_reach_room_bottom = 2 if room_considered[1] == AmphipodsTypes.EMPTY_SPACE else 1

            nb_rooms_passed = 0
            for nb_move, amphipod in enumerate(starting_burrow.hallway[idx_directly_left_of_room::-1]):
                current_hallway_idx = idx_directly_left_of_room - nb_move
                if current_hallway_idx in list_rooms_idx_moving_leftwards:
                    nb_rooms_passed += 1

                if amphipod != AmphipodsTypes.EMPTY_SPACE:
                    if amphipod == type_amphipods_considered:
                        acc_list.append(compute_move_to_one_room_specific_pos(
                            attribute_room_considered,
                            type_amphipods_considered,
                            nb_move_to_reach_room_bottom,
                            nb_move + nb_rooms_passed,
                            current_hallway_idx,
                            starting_burrow
                        ))
                    break

            nb_rooms_passed = 0
            for nb_move, amphipod in enumerate(starting_burrow.hallway[idx_directly_left_of_room+1:]):
                current_hallway_idx = idx_directly_left_of_room + 1 + nb_move
                if current_hallway_idx in list_rooms_idx_moving_rightwards:
                    nb_rooms_passed += 1

                if amphipod != AmphipodsTypes.EMPTY_SPACE:
                    if amphipod == type_amphipods_considered:
                        acc_list.append(compute_move_to_one_room_specific_pos(
                            attribute_room_considered,
                            type_amphipods_considered,
                            nb_move_to_reach_room_bottom,
                            nb_move + nb_rooms_passed,
                            current_hallway_idx,
                            starting_burrow
                        ))
                    break

    return acc_list


def compute_list_allowed_move(starting_burrow: AmphipodBurrow) -> list[BurrowMove]:
    acc_list: list[BurrowMove] = []

    global idx_left_room_a
    global idx_left_room_b
    global idx_left_room_c
    global idx_left_room_d

    acc_list.extend(
        compute_list_move_from_and_to_one_room('room_a', AmphipodsTypes.A, idx_left_room_a, starting_burrow)
    )
    acc_list.extend(
        compute_list_move_from_and_to_one_room('room_b', AmphipodsTypes.B, idx_left_room_b, starting_burrow)
    )
    acc_list.extend(
        compute_list_move_from_and_to_one_room('room_c', AmphipodsTypes.C, idx_left_room_c, starting_burrow)
    )
    acc_list.extend(
        compute_list_move_from_and_to_one_room('room_d', AmphipodsTypes.D, idx_left_room_d, starting_burrow)
    )

    return acc_list


def get_test_amphipod_burrow_start() -> AmphipodBurrow:
    burrow_to_ret = AmphipodBurrow()

    burrow_to_ret.room_a = [AmphipodsTypes.B, AmphipodsTypes.A]
    burrow_to_ret.room_b = [AmphipodsTypes.C, AmphipodsTypes.D]
    burrow_to_ret.room_c = [AmphipodsTypes.B, AmphipodsTypes.C]
    burrow_to_ret.room_d = [AmphipodsTypes.D, AmphipodsTypes.A]
    burrow_to_ret.hallway = [AmphipodsTypes.EMPTY_SPACE for _ in range(7)]

    return burrow_to_ret


def get_real_amphipod_burrow_start() -> AmphipodBurrow:
    burrow_to_ret = AmphipodBurrow()

    burrow_to_ret.room_a = [AmphipodsTypes.C, AmphipodsTypes.D]
    burrow_to_ret.room_b = [AmphipodsTypes.A, AmphipodsTypes.C]
    burrow_to_ret.room_c = [AmphipodsTypes.B, AmphipodsTypes.A]
    burrow_to_ret.room_d = [AmphipodsTypes.D, AmphipodsTypes.B]
    burrow_to_ret.hallway = [AmphipodsTypes.EMPTY_SPACE for _ in range(7)]

    return burrow_to_ret


def recursively_compute_possibles_move_list_to_tidied_burrow(
        list_move_to_current_burrow: list[BurrowMove]
) -> list[list[BurrowMove]]:
    list_burrow_moves_to_ret: list[list[BurrowMove]] = []
    starting_burrow = list_move_to_current_burrow[-1].arrival_state

    starting_burrow.debug_print()

    list_candidates_burrows_move = compute_list_allowed_move(starting_burrow)
    for burrow_move in list_candidates_burrows_move:
        local_move_list: list[BurrowMove] = list_move_to_current_burrow + [burrow_move]

        if burrow_move.arrival_state.is_burrow_tidied():
            list_burrow_moves_to_ret.append(local_move_list)
        else:
            list_burrow_moves_to_ret.extend(
                recursively_compute_possibles_move_list_to_tidied_burrow(list_move_to_current_burrow + [burrow_move])
            )
    return list_burrow_moves_to_ret


def main():
    starting_burrow = get_test_amphipod_burrow_start()
    # starting_burrow = get_real_amphipod_burrow_start()

    valid_moves_list = recursively_compute_possibles_move_list_to_tidied_burrow([BurrowMove(starting_burrow, 0)])

    candidate_lower_cost = Union[None, int]
    for list_moves in valid_moves_list:
        cost_total_moves: int = sum([move.move_cost for move in list_moves])
        if candidate_lower_cost is None or cost_total_moves < candidate_lower_cost:
            candidate_lower_cost = cost_total_moves

    print(candidate_lower_cost)


if __name__ == "__main__":
    main()
