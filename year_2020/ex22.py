def play_battle_round(deck_one, deck_two):
    card_deck_one = deck_one.pop(0)
    card_deck_two = deck_two.pop(0)

    if card_deck_one > card_deck_two:
        deck_one.extend((card_deck_one, card_deck_two))
    else:
        deck_two.extend((card_deck_two, card_deck_one))


def compute_unique_str_config(deck_one, deck_two):
    deck_one_unique_str = "".join([str(num_card) for num_card in deck_one])
    deck_two_unique_str = "".join([str(num_card) for num_card in deck_two])
    return deck_one_unique_str + " " + deck_two_unique_str


def play_recursive_battle_round(deck_one, deck_two, set_found_conf):
    unique_str = compute_unique_str_config(deck_one, deck_two)
    if unique_str in set_found_conf:
        return True
    set_found_conf.add(unique_str)

    card_deck_one = deck_one.pop(0)
    card_deck_two = deck_two.pop(0)

    if card_deck_one <= len(deck_one) and card_deck_two <= len(deck_two):
        player_one_won = play_recursive_battle_game(deck_one[:card_deck_one], deck_two[:card_deck_two])
    else:
        player_one_won = card_deck_one > card_deck_two

    if player_one_won:
        deck_one.extend((card_deck_one, card_deck_two))
    else:
        deck_two.extend((card_deck_two, card_deck_one))

    return False


def play_recursive_battle_game(deck_one, deck_two):
    set_found_conf = set()

    while len(deck_one) != 0 and len(deck_two) != 0:
        has_player_one_won = play_recursive_battle_round(deck_one, deck_two, set_found_conf)
        if has_player_one_won:
            break

    return len(deck_one) != 0


def compute_deck_score(deck):
    score = 0
    for idx_card, card_value in enumerate(reversed(deck)):
        score += (idx_card + 1) * card_value
    return score


with open("data.txt") as f:
    content = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line
deck_player_one = []
deck_player_two = []
to_fill_deck = deck_player_one

for line in content[1:]:
    if line == "":
        continue
    elif line[0] == "P":
        to_fill_deck = deck_player_two
    else:
        to_fill_deck.append(int(line))

play_recursive_battle_game(deck_player_one, deck_player_two)

#34095 too low
if len(deck_player_one) == 0:
    print(compute_deck_score(deck_player_two))
else:
    print(compute_deck_score(deck_player_one))
