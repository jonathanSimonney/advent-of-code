def parse_image_in_layers(str_image, width_image, height_image):
    image_str_len = len(str_image)
    layers_list = []
    image_str_idx = 0
    while True:
        current_layer = []
        for height_idx in range(height_image):
            next_image_idx = image_str_idx + width_image
            current_layer.append(str_image[image_str_idx:next_image_idx])
            image_str_idx = next_image_idx
        layers_list.append(current_layer)
        if image_str_len == image_str_idx:
            break

    return layers_list


def count_str_in_layer(layer_to_search, str_to_count):
    acc = 0
    for row in layer_to_search:
        acc += row.count(str_to_count)
    return acc


def recursive_compute_resulting_image(array_layers, current_image):
    for row_idx, row in enumerate(current_image):
        current_row = list(row)
        for col_idx, col_char in enumerate(current_row):
            if col_char == '2':
                current_row[col_idx] = array_layers[0][row_idx][col_idx]
        current_image[row_idx] = "".join(current_row)

    if len(array_layers) == 1:
        return current_image
    return recursive_compute_resulting_image(array_layers[1:], current_image)


def ascii_print_image(image_to_print):
    for row in image_to_print:
        print(row.replace('0', '.').replace('1', '#'))


with open("data.txt") as f:
    content = f.readlines()[0]

width = 25
height = 6

parsed_image = parse_image_in_layers(content, width, height)

min_nb_0_found = None
layer_with_min_nb_0 = None
for layer in parsed_image:
    candidate_min_nb_0_found = count_str_in_layer(layer, '0')
    if min_nb_0_found is None or candidate_min_nb_0_found < min_nb_0_found:
        layer_with_min_nb_0 = layer
        min_nb_0_found = candidate_min_nb_0_found

print(count_str_in_layer(layer_with_min_nb_0, '1') * count_str_in_layer(layer_with_min_nb_0, '2'))

single_layer_image = recursive_compute_resulting_image(parsed_image, parsed_image[0])
print(single_layer_image)
# CFCUS isn't right
ascii_print_image(single_layer_image)
