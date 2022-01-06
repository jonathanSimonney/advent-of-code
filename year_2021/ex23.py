import copy
from enum import Enum
from typing import Union


class AmphipodsTypes(Enum):
    A = 1
    B = 10
    C = 100
    D = 1000
    EMPTY_SPACE = 0


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

        local_burrow = copy.deepcopy(starting_burrow)
        local_burrow.hallway[idx_move] = type_amphipods_considered
        getattr(local_burrow, attribute_room_considered)[0] = AmphipodsTypes.EMPTY_SPACE
        move_cost: int = nb_move_done * type_amphipods_considered.value

        acc_list.append(BurrowMove(local_burrow, move_cost))

    nb_move_done = nb_move_to_leave_room
    for idx_move in range(idx_directly_left_of_room + 1, 7):
        if starting_burrow.hallway[idx_move] != AmphipodsTypes.EMPTY_SPACE:
            break
        nb_move_done += 1

        local_burrow = copy.deepcopy(starting_burrow)
        local_burrow.hallway[idx_move] = type_amphipods_considered
        getattr(local_burrow, attribute_room_considered)[0] = AmphipodsTypes.EMPTY_SPACE
        move_cost: int = nb_move_done * type_amphipods_considered.value

        acc_list.append(BurrowMove(local_burrow, move_cost))

    return acc_list


def compute_list_move_from_one_room(
        attribute_room_considered: str,
        type_amphipods_considered: AmphipodsTypes,
        idx_directly_left_of_room: int,
        starting_burrow: AmphipodBurrow
) -> list[BurrowMove]:
    acc_list: list[BurrowMove] = []

    room_considered = getattr(starting_burrow, attribute_room_considered)

    if room_considered != [type_amphipods_considered, type_amphipods_considered] and \
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

    return acc_list


def compute_list_allowed_move(starting_burrow: AmphipodBurrow) -> list[BurrowMove]:
    acc_list: list[BurrowMove] = []

    idx_left_room_a = 1
    idx_left_room_b = 2
    idx_left_room_c = 3
    idx_left_room_d = 4

    acc_list.extend(compute_list_move_from_one_room('room_a', AmphipodsTypes.A, idx_left_room_a, starting_burrow))
    acc_list.extend(compute_list_move_from_one_room('room_b', AmphipodsTypes.B, idx_left_room_b, starting_burrow))
    acc_list.extend(compute_list_move_from_one_room('room_c', AmphipodsTypes.C, idx_left_room_c, starting_burrow))
    acc_list.extend(compute_list_move_from_one_room('room_d', AmphipodsTypes.D, idx_left_room_d, starting_burrow))

    #todo add the moves from hallway to rooms then

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


def recursively_compute_possibles_move_list_to_tidied_burrow(starting_burrow: AmphipodBurrow) -> list[list[BurrowMove]]:
    while not starting_burrow.is_burrow_tidied():
        list_candidates_burrows_move = compute_list_allowed_move(starting_burrow)
        for burrow_move in list_candidates_burrows_move:
            # check if move makes a tidied burrow, if yes, stop and add it to the list candidates full move, else
            # back in recursion
            pass
    pass


def main():
    starting_burrow = get_test_amphipod_burrow_start()
    # starting_burrow = get_real_amphipod_burrow_start()

    valid_moves_list = recursively_compute_possibles_move_list_to_tidied_burrow(starting_burrow)

    candidate_lower_cost = Union[None, int]
    for list_moves in valid_moves_list:
        cost_total_moves: int = sum([move.move_cost for move in list_moves])
        if candidate_lower_cost is None or cost_total_moves < candidate_lower_cost:
            candidate_lower_cost = cost_total_moves

    print(candidate_lower_cost)




if __name__ == "__main__":
    main()
