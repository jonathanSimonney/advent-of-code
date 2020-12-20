import collections
import math


def rotate_matrice(matrice_to_rotate):
    rotated_matrice = ['' for _ in matrice_to_rotate]

    for row in matrice_to_rotate:
        for idx, char in enumerate(row):
            rotated_matrice[idx] += char

    for idx, row in enumerate(rotated_matrice):
        rotated_matrice[idx] = row[::-1]

    return rotated_matrice


def flip_matrice_top_down(matrice_to_flip):
    flipped_matrice = ['' for _ in matrice_to_flip]
    for idx, row in enumerate(matrice_to_flip):
        flipped_matrice[-idx - 1] = row
    return flipped_matrice


def flip_matrice_right_left(matrice_to_flip):
    for idx, row in enumerate(matrice_to_flip):
        matrice_to_flip[idx] = row[::-1]

class Tile:
    up = ""
    down = ""
    left = ""
    right = ""
    id = 0
    image_matrice = []

    def __init__(self, image_matrice, id_tile):
        unbordered_image_matrice = []
        left_str = ""
        right_str = ""
        for line_image in image_matrice:
            unbordered_image_matrice.append(line_image[1:-1])
            left_str += line_image[0]
            right_str += line_image[-1]
        self.up = image_matrice[0]
        self.down = image_matrice[-1]
        self.left = left_str
        self.right = right_str
        self.image_matrice = unbordered_image_matrice[1:-1]
        self.id = id_tile

    # rotate a tile on the right
    def rotate_tile(self):
        old_up = self.up
        self.up = self.left[::-1]
        self.left = self.down
        self.down = self.right[::-1]
        self.right = old_up
        self.image_matrice = rotate_matrice(self.image_matrice)

    def flip_tile_top_down(self):
        old_up = self.up
        self.up = self.down
        self.left = self.left[::-1]
        self.right = self.right[::-1]
        self.down = old_up
        self.image_matrice = flip_matrice_top_down(self.image_matrice)

    def flip_tile_right_left(self):
        old_left = self.left
        self.left = self.right
        self.up = self.up[::-1]
        self.down = self.down[::-1]
        self.right = old_left
        flip_matrice_right_left(self.image_matrice)

    def orientate_tile_so_left_border_match(self, left_border_to_match):
        while self.left != left_border_to_match and self.left[::-1] != left_border_to_match:
            self.rotate_tile()
        if self.left != left_border_to_match:
            self.flip_tile_top_down()

    def orientate_tile_so_top_border_match(self, up_border_to_match):
        while self.up != up_border_to_match and self.up[::-1] != up_border_to_match:
            self.rotate_tile()
        if self.up != up_border_to_match:
            self.flip_tile_right_left()

    def _get_borders_set(self):
        return {self.left, self.right, self.up, self.down}


def add_tile_right_of_tile(matrice_tiles_to_fill, row_num, col_num):
    tile_left = matrice_tiles_to_fill[row_num][col_num]
    border_to_check = tile_left.right
    list_candidates_tiles = dict_borders[border_to_check]
    if list_candidates_tiles[0].id == tile_left.id:
        tile_to_add = list_candidates_tiles[1]
    else:
        tile_to_add = list_candidates_tiles[0]
    tile_to_add.orientate_tile_so_left_border_match(border_to_check)
    matrice_tiles_to_fill[row_num].append(tile_to_add)


def add_tile_bottom_of_tile(matrice_tiles_to_fill, row_num, col_num):
    tile_up = matrice_tiles_to_fill[row_num][col_num]
    border_to_check = tile_up.down
    list_candidates_tiles = dict_borders[border_to_check]
    if list_candidates_tiles[0].id == tile_up.id:
        tile_to_add = list_candidates_tiles[1]
    else:
        tile_to_add = list_candidates_tiles[0]
    tile_to_add.orientate_tile_so_top_border_match(border_to_check)
    matrice_tiles_to_fill[row_num + 1].append(tile_to_add)


def count_sea_monsters_in_matrice(matrice_to_search):
    acc = 0
    for row_idx, row in enumerate(matrice_to_search):
        for col_idx, char in enumerate(row):
            try:
                if row_idx > 0 \
                        and char == "#" \
                        and matrice_to_search[row_idx+1][col_idx+1] == "#" \
                        and matrice_to_search[row_idx+1][col_idx+4] == "#" \
                        and matrice_to_search[row_idx][col_idx+5] == "#" \
                        and matrice_to_search[row_idx][col_idx+6] == "#" \
                        and matrice_to_search[row_idx+1][col_idx+7] == "#" \
                        and matrice_to_search[row_idx+1][col_idx+10] == "#" \
                        and matrice_to_search[row_idx][col_idx+11] == "#" \
                        and matrice_to_search[row_idx][col_idx+12] == "#"  \
                        and matrice_to_search[row_idx+1][col_idx+13] == "#" \
                        and matrice_to_search[row_idx+1][col_idx+16] == "#" \
                        and matrice_to_search[row_idx][col_idx+17] == "#" \
                        and matrice_to_search[row_idx][col_idx+18] == "#" \
                        and matrice_to_search[row_idx][col_idx+19] == "#" \
                        and matrice_to_search[row_idx - 1][col_idx+18] == "#":
                    matrice_to_search[row_idx][col_idx] = "O"
                    matrice_to_search[row_idx+1][col_idx+1] = "O"
                    matrice_to_search[row_idx+1][col_idx+4] = "O"
                    matrice_to_search[row_idx][col_idx+5] = "O"
                    matrice_to_search[row_idx][col_idx+6] = "O"
                    matrice_to_search[row_idx+1][col_idx+7] = "O"
                    matrice_to_search[row_idx+1][col_idx+10] = "O"
                    matrice_to_search[row_idx][col_idx+11] = "O"
                    matrice_to_search[row_idx][col_idx + 12] = "O"
                    matrice_to_search[row_idx + 1][col_idx + 13] = "O"
                    matrice_to_search[row_idx + 1][col_idx + 16] = "O"
                    matrice_to_search[row_idx][col_idx + 17] = "O"
                    matrice_to_search[row_idx][col_idx + 18] = "O"
                    matrice_to_search[row_idx][col_idx + 19] = "O"
                    matrice_to_search[row_idx - 1][col_idx + 18] = "O"
                    acc += 1
            except IndexError:
                continue
    return acc

with open("data.txt") as f:
    content = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

dict_images = {}

current_image_matrice = []
current_image_num = None
for line in content:
    if line == "":
        dict_images[current_image_num] = Tile(current_image_matrice, current_image_num)
        current_image_matrice = []
        current_image_num = None
    elif line[:4] == "Tile":
        tile_number = line.replace("Tile ", "").replace(":", "")
        current_image_num = int(tile_number)
    else:
        current_image_matrice.append(line)

dict_borders = collections.defaultdict(lambda:  [])
dict_borders_not_reverted = collections.defaultdict(lambda:  [])

for tile in dict_images.values():
    dict_borders[tile.up].append(tile)
    dict_borders[tile.down].append(tile)
    dict_borders[tile.left].append(tile)
    dict_borders[tile.right].append(tile)
    dict_borders_not_reverted[tile.up].append(tile)
    dict_borders_not_reverted[tile.down].append(tile)
    dict_borders_not_reverted[tile.left].append(tile)
    dict_borders_not_reverted[tile.right].append(tile)

    dict_borders[tile.up[::-1]].append(tile)
    dict_borders[tile.down[::-1]].append(tile)
    dict_borders[tile.left[::-1]].append(tile)
    dict_borders[tile.right[::-1]].append(tile)

set_corners_borders = set()

for border_str, list_tile_with_border in dict_borders.items():
    if len(list_tile_with_border) == 1:
        set_corners_borders.add(border_str)
    elif len(list_tile_with_border) > 2:
        print(len(list_tile_with_border), "we're doomed")


acc = 1
for tile_number, tile in dict_images.items():
    nb_corner_borders = 0
    if tile.right in set_corners_borders:
        nb_corner_borders += 1
    if tile.left in set_corners_borders:
        nb_corner_borders += 1
    if tile.up in set_corners_borders:
        nb_corner_borders += 1
    if tile.down in set_corners_borders:
        nb_corner_borders += 1
    if nb_corner_borders == 2:
        top_left_tile = tile
        # list_corners_tiles.append(tile)
        acc *= tile_number

nb_tile_per_side = int(math.sqrt(len(dict_images)))
matrice_tiles_ordered = [[] for _ in range(nb_tile_per_side)]

# for data.txt
top_left_tile.rotate_tile()
top_left_tile.rotate_tile()
top_left_tile.rotate_tile()
print(top_left_tile.up in set_corners_borders)
print(top_left_tile.left in set_corners_borders)

matrice_tiles_ordered[0].append(top_left_tile)
nb_tile_placed = 1
is_first_col_image = False

while nb_tile_placed != len(dict_images):
    row_to_place_image = math.trunc(nb_tile_placed / nb_tile_per_side)
    idx_to_place_image = int(nb_tile_placed % nb_tile_per_side)

    # print(row_to_place_image, idx_to_place_image)
    if idx_to_place_image == 0:
        add_tile_bottom_of_tile(matrice_tiles_ordered, row_to_place_image - 1, idx_to_place_image)
    else:
        add_tile_right_of_tile(matrice_tiles_ordered, row_to_place_image, idx_to_place_image - 1)

    nb_tile_placed += 1

end_gigantic_picture = ["" for i in range(nb_tile_per_side * 8)]
for idx_tile, list_tile in enumerate(matrice_tiles_ordered):
    for tile in list_tile:
        for idx_row, row in enumerate(tile.image_matrice):
            end_gigantic_picture[idx_tile * 8 + idx_row] += row

print(end_gigantic_picture)

# with open("imageEx20.txt") as f:
#     end_gigantic_picture = [x.strip() for x in f.readlines()]

# time to hunt sea monsters!!!
nb_sea_monsters = 0
nb_rotation = 0
while nb_sea_monsters == 0:
    for idx, row in enumerate(end_gigantic_picture):
        end_gigantic_picture[idx] = list(row)
    nb_sea_monsters = count_sea_monsters_in_matrice(end_gigantic_picture)
    end_gigantic_picture = rotate_matrice(end_gigantic_picture)
    nb_rotation += 1
    if nb_rotation == 4:
        end_gigantic_picture = flip_matrice_top_down(end_gigantic_picture)
    elif nb_rotation == 8:
        flip_matrice_right_left(end_gigantic_picture)
    elif nb_rotation == 12:
        end_gigantic_picture = flip_matrice_top_down(end_gigantic_picture)

    print("no sea monster found, maybe next time")
# 1219738198528098269379786367298173288497601326951432780641990755655922159729765337025708168820859112058599727637563627856118899885436743410344367667608975095259197872956516315525558472469984367395933 too high
print(nb_sea_monsters, end_gigantic_picture)

sea_roughness = 0
for row in end_gigantic_picture:
    for char in row:
        if char == "#":
            sea_roughness += 1

print(sea_roughness)