def create_transformer_with_subject_number(subject_number_to_use):
    def transform_number(number_to_transform):
        return (number_to_transform * subject_number_to_use) % 20201227

    return transform_number


card_public_key = 5290733
door_public_key = 15231938

# card_public_key = 5764801
# door_public_key = 17807724

secret_loop_size = 0

initial_number = 1
initial_transformer = create_transformer_with_subject_number(7)
while initial_number != card_public_key and initial_number != door_public_key:
    initial_number = initial_transformer(initial_number)
    # print(subject_number)
    secret_loop_size += 1

# print(secret_loop_size, initial_number)
# 9886057 too high
if initial_number == card_public_key:
    i = 0

    transformer_secondary = create_transformer_with_subject_number(door_public_key)
    secondary_initial_number = 1
    for _ in range(secret_loop_size):
        i += 1
        secondary_initial_number = transformer_secondary(secondary_initial_number)
    print(secondary_initial_number)
else:
    transformer_secondary = create_transformer_with_subject_number(card_public_key)
    secondary_initial_number = 1

    for _ in range(secret_loop_size):
        secondary_initial_number = transformer_secondary(secondary_initial_number)
    print(secondary_initial_number)
