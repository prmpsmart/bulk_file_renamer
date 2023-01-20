# def change_destination(filenames: list[str], destination_folder: str):
#     ...


# def change_base_name(filename: str, new_base_name: str):
#     ...


# def auto_indexing(
#     filenames: list[str],
#     separator: str = "",
#     before: bool = True,
#     start_index: int = 0,
#     step: int = 1,
#     zero_padding: int = 0,
# ):
#     ...


# def capitalization(
#     filenames: list[str],
#     lower: bool = False,
#     upper: bool = False,
#     sentence: bool = False,
# ):
#     ...


# def change_extension(filenames: list[str], extension: str):
#     ...


# def add_prefix(filenames: list[str], prefix: str):
#     ...


# def add_suffix(filenames: list[str], suffix: str):
#     ...


# def add_date(
#     filenames: list[str],
#     before: bool = False,
#     separator: str = "-",
#     formats: list[str] = [],
# ):
#     ...


# def add_characters(
#     filenames: list[str], characters: str, position: int, start: bool = False
# ):
#     ...


# def trim_whitespaces(filenames: list[str], start_end: bool = False, all: bool = False):
#     ...


# def remove_characters(filenames: list[str], characters: str):
#     ...


# def remove_multiple_characters(filenames: list[str], characters_list: list[str]):
#     for characters in characters_list:
#         filenames = remove_characters(filenames)
#     return filenames


# def remove_characters_by_type(
#     filenames: list[str],
#     all_numbers: bool = False,
#     all_letters: bool = False,
#     all_non_numerics: bool = False,
#     all_non_letters: bool = False,
# ):
#     ...


# def remove_characters_at_position(
#     filenames: list[str],
#     first: int = 0,
#     last: int = 0,
#     range: bool = False,
#     range_start: int = 0,
#     range_end: int = 0,
# ):
#     ...


# def replace_characters(filenames: list[str], characters: str, replacement: str):
#     ...
