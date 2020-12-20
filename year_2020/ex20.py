import collections


class Tile:
    up = ""
    down = ""
    left = ""
    right = ""
    image_matrice = []

    def __init__(self, image_matrice):
        left_str = ""
        right_str = ""
        for line_image in image_matrice:
            left_str += line_image[0]
            right_str += line_image[-1]
        self.up = image_matrice[0]
        self.down = image_matrice[-1]
        self.left = left_str
        self.right = right_str
        self.image_matrice = image_matrice

    # rotate a tile on the right
    def rotate_tile(self):
        old_up = self.up
        self.up = self.left
        self.left = self.down
        self.down = self.right
        self.right = old_up
        new_image_matrice = ['' for _ in self.image_matrice]
        for row in self.image_matrice:
            for idx, char in enumerate(row):
                new_image_matrice[idx] += char
        self.image_matrice = new_image_matrice

    def flip_tile(self):
        # flip reverse the borders!!!
        old_up = self.up
        self.up = self.down
        self.left = self.left[::-1]
        self.right = self.right[::-1]
        self.down = old_up
        new_image_matrice = ['' for _ in self.image_matrice]
        for idx, row in enumerate(self.image_matrice):
            new_image_matrice[-idx] = row
        self.image_matrice = new_image_matrice


with open("data.txt") as f:
    content = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

# image format : {"up": str_border_up, "down": str_border_down, "left": str_border_left, "right": str_border_right, "whole_image": str_entire_image}
dict_images = {}

current_image_matrice = []
current_image_num = None
for line in content:
    if line == "":
        dict_images[current_image_num] = Tile(current_image_matrice)
        current_image_matrice = []
        current_image_num = None
    elif line[:4] == "Tile":
        tile_number = line.replace("Tile ", "").replace(":", "")
        current_image_num = int(tile_number)
    else:
        current_image_matrice.append(line)

dict_borders = collections.defaultdict(lambda: 0)

for tile in dict_images.values():
    dict_borders[tile.up] += 1
    dict_borders[tile.down] += 1
    dict_borders[tile.left] += 1
    dict_borders[tile.right] += 1
    dict_borders[tile.up[::-1]] += 1
    dict_borders[tile.down[::-1]] += 1
    dict_borders[tile.left[::-1]] += 1
    dict_borders[tile.right[::-1]] += 1

set_corners_borders = set()

for border_str, nb_occurence_border in dict_borders.items():
    if nb_occurence_border == 1:
        set_corners_borders.add(border_str)

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
        acc *= tile_number

# 1219738198528098269379786367298173288497601326951432780641990755655922159729765337025708168820859112058599727637563627856118899885436743410344367667608975095259197872956516315525558472469984367395933 too high
print(acc)
