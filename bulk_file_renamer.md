**Mentor -> @prmpsmart**

# **Bulk File Renamer**
A bulk file renamer project with the following features. All these features may be used at the same time or not.

## **0. Destination**
- Specify the destination directory.
```python
def change_destination(filenames: list[str], destination_folder: str):
    ...
```
<br>

## **1. Change base name**
Set a new base name for all the files. This will replace the original base names.
```python
def change_base_name(filename: str, new_base_name: str):
    ...
```
<br>

## **2. Auto-indexing**
Add an auto-incremented index before or after the base name of the files.
- Specify separator between the base name and the index e.g "-" in the case of "image-001".
- Specify the position (before, after).
- Specify the start index.
- Specify the step value.
- Specify the zero padding e.g if zero padding is 2, the indexing is 1 the value is 01, if padding is 4 and value is 234 then resulting value is 0234.
```python
def auto_indexing(filenames: list[str], separator: str='', before: bool=True, start_index: int=0, step: int=1, zero_padding: int=0):
    ...
```
<br>

## **3. Capitalization**
Change the capitalization of the entire name.
- All Lower Case.
- All Upper Case.
- Sentence Case.
```python
def capitalization(filenames: list[str], lower: bool=False, upper: bool=False, sentence: bool=False):
    ...
```
<br>

## **4. Change extension**
Change the extension of the files.
```python
def change_extension(filenames: list[str], extension: str):
    ...
```
<br>

## **5. Add prefix**
Add prefix before the base name.
```python
def add_prefix(filenames: list[str], prefix: str):
    ...
```
<br>

## **6. Add suffix**
Add suffix affer the base name.
```python
def add_suffix(filenames: list[str], suffix: str):
    ...
```
<br>

## **7. Add date**
Add last modified date.
- Specify the date position.
- Specify separator between the base name and the date.
- Specify date format with six possible values (year, month, day, hour, minute, second). All or some may be included.
```python
def add_date(filenames: list[str], before: bool=False, separator: str='-', formats: list[str]=[]):
    '''check the last modified date of the files and format the date
    examples of the "formats" parameter are:
        - [year, month, day, hour, minute, second]
        - [hour, minute, second]
        - [year, hour, minute, second, year]

        the maximum possible values is 6.
    '''
    ...
```
<br>

## **8. Add characters at position**
Add characters at specified position (starts with 0).
- Specify the characters to add.
- Specify the position to start counting from (start, end).
- Specify the position to add the characters.
```python
def add_characters(filenames: list[str], characters: str, position: int, start: bool=False):
    ...
```
<br>

## **9. Trim whitespaces**
Remove whitespaces from specified positions. Two options.
- Remove whitespaces from start and end.
- Remove all whitespaces.
```python
def trim_whitespaces(filenames: list[str], start_end: bool=False, all: bool=False):
    ...
```
<br>

## **10. Remove characters**
Remove characters or words from the name.
```python
def remove_characters(filenames: list[str], characters: str):
    ...
```
<br>

## **11. Remove multiple characters**
Remove multiple characters or words from the base name at once.
```python
def remove_multiple_characters(filenames: list[str], characters_list: list[str]):
    for characters in characters_list:
        filenames = remove_characters(filenames)
    return filenames
```
<br>

## **12. Remove characters by type**
Remove all characters of a chosen type.
- Remove all numbers.
- Remove all letters.
- Remove all non-numerics.
- Remove all non-letters.
```python
def remove_characters_by_type(filenames: list[str], all_numbers: bool=False, all_letters: bool=False, all_non_numerics: bool=False, all_non_letters: bool=False):
    ...
```
<br>

## **13. Remove characters at position**
Remove a number of character from the start, end or custom range.
- Specify the first number of characters to remove.
- Specify the last number of characters to remove.
- Specify the range of characters to remove e.g from the 5th to 9th character.
```python
def remove_characters_at_position(filenames: list[str], first: int=0, last: int=0, range: bool=False, range_start: int=0, range_end: int=0):
    ...
```
<br>

## **14. Replace characters**
Replace characters or words.
- Specify the characters or word to replace.
- Specify the characters to use in replacements.
```python
def replace_characters(filenames: list[str], characters: str, replacement: str):
    ...
```
<br>
