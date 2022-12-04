def split_str_in_half(str_to_split: str) -> list[str]:
    # copypasted from https://stackoverflow.com/a/4789617/7059810
    firstpart, secondpart = str_to_split[:len(str_to_split) // 2], str_to_split[len(str_to_split) // 2:]
    return [firstpart, secondpart]
