from enum import Enum


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


def compute_list_allowed_move(starting_burrow: AmphipodBurrow) -> list[BurrowMove]:
    pass


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


def main():
    pass


if __name__ == "__main__":
    main()
