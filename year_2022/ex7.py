import collections
from dataclasses import dataclass
from typing import Dict, Set, List, Union, Optional


@dataclass(frozen=True)
class File:
    size: int
    name: str

    def compute_size(self) -> int:
        return self.size


class Folder:
    childs: List[Union[File, 'Folder']]
    name: str
    _size: Optional[int] = None

    def __init__(self, childs: List[Union[File, 'Folder']], name: str):
        self.childs = childs
        self.name = name

    def compute_size(self) -> int:
        if self._size is not None:
            return self._size
        return sum([elem.compute_size() for elem in self.childs])


class FileSystem:
    root: Folder = Folder([], '/')
    _current_loc: Folder
    _parent_loc: List[Folder]

    _folder_size_dict: Dict[str, int] = {}

    def apply_cd(self, to: str):
        if to == '..':
            self._move_to_parent()
        elif to == '/':
            self._move_to_root()
        else:
            self._move_to_child(to)

    def _move_to_root(self):
        self._current_loc = self.root
        self._parent_loc = []

    def _move_to_parent(self):
        if len(self._parent_loc) == 0:
            raise AssertionError("no parent defined")
        self._current_loc = self._parent_loc.pop()

    def _move_to_child(self, to):
        for elem in self._current_loc.childs:
            if isinstance(elem, Folder) and elem.name == to:
                self._parent_loc.append(self._current_loc)
                self._current_loc = elem
                break

    def apply_ls(self, childs_as_str: List[str]):
        list_childs: List[Union[File, 'Folder']] = [
            self._parse_str_to_file_or_folder(single_child) for single_child in childs_as_str
        ]
        self._current_loc.childs = list_childs

    @staticmethod
    def _parse_str_to_file_or_folder(str_to_parse: str) -> Union[File, Folder]:
        splitted_str = str_to_parse.split(' ')
        if splitted_str[0] == 'dir':
            return Folder([], splitted_str[1])

        return File(int(splitted_str[0]), splitted_str[1])

    def get_result_part_1(self) -> int:
        self._fill_dict_folder_size(self.root, '/')

        acc: int = 0
        for folder_size in self._folder_size_dict.values():
            if folder_size <= 100000:
                acc += folder_size

        return acc

    def get_result_part_2(self) -> int:
        self._fill_dict_folder_size(self.root, '/')

        total_space_taken = self._folder_size_dict['/']
        unused_space = 70000000 - total_space_taken
        needed_space_to_delete = 30000000 - unused_space

        # print(total_space_taken, unused_space, needed_space_to_delete)
        # print(self.root.childs)
        # print(self._folder_size_dict)
        # # print(self._folder_size_dict['/a'])
        # # print(self._folder_size_dict['/'])
        # # print(self._folder_size_dict['/'])

        deletion_size_candidate = total_space_taken

        for folder_size in self._folder_size_dict.values():
            if needed_space_to_delete <= folder_size < deletion_size_candidate:
                deletion_size_candidate = folder_size

        return deletion_size_candidate

    def _fill_dict_folder_size(self, folder_to_parse: Folder, folder_path: str):
        for elem in folder_to_parse.childs:
            if isinstance(elem, Folder):
                self._fill_dict_folder_size(elem, folder_path + '/' + elem.name)
        if folder_path not in self._folder_size_dict:
            self._folder_size_dict[folder_path] = folder_to_parse.compute_size()


with open("data.txt") as f:
    content = f.read().splitlines()

fs: FileSystem = FileSystem()

buffer_strs_to_ls: List[str] = []
is_in_ls: bool = False

for line in content:
    splitted_line = line.split(' ')
    if splitted_line[0] == '$':
        if is_in_ls:
            is_in_ls = False
            fs.apply_ls(buffer_strs_to_ls)
            buffer_strs_to_ls = []

        if splitted_line[1] == 'cd':
            fs.apply_cd(splitted_line[2])
        elif splitted_line[1] == 'ls':
            is_in_ls = True
        else:
            raise AssertionError('unknown command')
    else:
        buffer_strs_to_ls.append(line)

fs.apply_ls(buffer_strs_to_ls)
buffer_strs_to_ls = []
# 2319218 too low
print(fs.get_result_part_2())
