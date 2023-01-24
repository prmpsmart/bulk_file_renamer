from os import path, rename
from shutil import move
from string import ascii_letters, digits
from time import ctime, strptime, strftime

__all__ = ["bulk_file_renamer", "renamer"]
date_formats = dict(
    year="%Y",
    month="%m",
    day="%d",
    hour="%H",
    minute="%M",
    second="%S",
)


def bulk_file_renamer(
    filenames: list[str],
    new_basename: str = "",
    # change_destination
    destination_folder: str = "",
    # change_extension
    extension: str = "",
    # capitalization
    lower: bool = False,
    upper: bool = False,
    sentence: bool = False,
    # add_characters
    add_characters: str = "",
    add_position: int = 0,
    add_to_start: bool = False,
    # replace_characters
    replace_characters: str = "",
    characters_replacement: str = "",
    # remove_characters
    remove_characters: str = "",
    # remove_multiple_characters
    remove_multiple_characters: list[str] = [],
    # remove_whitespaces
    remove_whitespaces_start_n_end: bool = False,
    remove_whitespaces_all: bool = False,
    # remove_characters_by_type
    remove_all_numbers: bool = False,
    remove_all_letters: bool = False,
    remove_all_non_numerics: bool = False,
    remove_all_non_letters: bool = False,
    # add_prefix
    add_prefix: str = "",
    # add_suffix
    add_suffix: str = "",
    # add_date
    add_date: bool = False,
    add_date_separator: str = "",
    add_date_formats: list[str] = [],
    add_date_before: bool = False,
    # remove_characters_at_position
    remove_characters_at_first_position: int = 0,
    remove_characters_at_last_position: int = 0,
    remove_characters_at_range: bool = False,
    remove_characters_at_range_start: int = 0,
    remove_characters_at_range_end: int = 0,
    # auto_indexing
    auto_indexing: bool = False,
    auto_indexing_start_index: int = 0,
    auto_indexing_step: int = 1,
    auto_indexing_separator: str = "",
    auto_indexing_before: bool = True,
    auto_indexing_zero_padding: int = 0,
) -> list[tuple]:
    new_filenames: list[tuple] = []

    for index, filename in enumerate(filenames):

        basename = path.basename(filename)
        name, ext = path.splitext(basename)

        # change_extension
        ext = extension or ext
        if not ext.startswith("."):
            ext = "." + ext

        # add_characters
        if add_characters:
            if add_to_start:
                add_index = add_position
            else:
                add_index = len(name) - add_position
            name = name[:add_index] + add_characters + name[add_index:]

        # remove_whitespaces
        if remove_whitespaces_start_n_end:
            name = name.strip()
        elif remove_whitespaces_all:
            name = name.replace(" ", "")

        # replace_characters
        if replace_characters:
            name = name.replace(replace_characters, characters_replacement)

        # remove_characters
        if remove_characters:
            name = name.replace(remove_characters, "")

        # remove_multiple_characters
        if remove_multiple_characters:
            for chars in remove_multiple_characters:
                name = name.replace(chars, "")

        # remove_characters_by_type
        if remove_all_numbers:
            for digit in digits:
                name = name.replace(digit, "")
        elif remove_all_non_numerics:
            _name = name
            for n in _name:
                if n not in digits:
                    name = name.replace(n, "")

        if remove_all_letters:
            for letter in ascii_letters:
                name = name.replace(letter, "")
        elif remove_all_non_letters:
            _name = name
            for n in _name:
                if n not in ascii_letters:
                    name = name.replace(n, "")

        # capitalization
        if lower:
            name = name.lower()
        elif upper:
            name = name.upper()
        elif sentence:
            name = name.title()

        # remove_characters_at_position
        if remove_characters_at_first_position:
            name = name[remove_characters_at_first_position:]
        elif remove_characters_at_last_position:
            name = name[:remove_characters_at_last_position]
        elif remove_characters_at_range:
            if (
                remove_characters_at_range_start >= 0
                and remove_characters_at_range_end > remove_characters_at_range_start
            ):
                name = (
                    name[:remove_characters_at_range_start]
                    + name[remove_characters_at_range_end:]
                )

        # change_base_name
        if new_basename:
            name = new_basename

        # add_prefix
        if add_prefix:
            name = add_prefix + name

        # add_suffix
        if add_suffix:
            name += add_suffix

        # add_date
        if add_date:
            time_obj = strptime(ctime(path.getmtime(filename)))
            date = add_date_separator.join(
                [strftime(format, time_obj) for format in add_date_formats]
            )

            if add_date_before:
                name = date + name
            else:
                name += date

        # auto_indexing
        if auto_indexing:
            index *= auto_indexing_step
            index += auto_indexing_start_index
            index = str(index).zfill(auto_indexing_zero_padding)

            if auto_indexing_before:
                name = index + auto_indexing_separator + name
            else:
                name += auto_indexing_separator + index

        name += ext

        # change_destination
        destination_folder = destination_folder or path.dirname(filename)

        name = path.join(destination_folder, name)

        new_filenames.append((filename, name))

    return new_filenames


def renamer(filenames: list[str], **kwargs):
    lists = bulk_file_renamer(filenames, **kwargs)
    for filename, new_filename in lists:
        rename(filename, new_filename)
