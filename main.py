import sys
import os
import re


def is_file_valid(filepath: str) -> bool:
    '''
    Check if the file exists and is a .map file.
    :param filepath: The path to the file.
    '''
    if not filepath.endswith(".map"):
        print(f"File {filepath} is not a .map file.")
        return False

    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return False
    return True


def find_variable(filepath: str, variable_name: str) -> str:
    '''
    Find the address of a variable in the .map file.
    :param filepath: The path to the file.
    :param variable_name: The name of the variable.
    :return: The address of the variable.
    '''
    with open(filepath, "r") as file:
        text = file.read()

    SECTION_START_CAPTION: str = "Linker script and memory map"
    SECTION_END_CAPTION: str = "Symbol"

    index_start = text.find(SECTION_START_CAPTION)
    index_end = text.find(SECTION_END_CAPTION)

    index_start = index_start + len(SECTION_START_CAPTION) if index_start != -1 else 0

    if index_end == -1:
        index_end = len(text)

    PATTERN = r'\s*(0x[0-9a-fA-F]{1,16})\s+' + re.escape(variable_name) + r'\s*\n'
    result = re.search(PATTERN, text[index_start:index_end])

    if result is None:
        return ''

    return result.group(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Invalid number of arguments.")
        print("Usage: python main.py <input_file> <variable_name>")
        sys.exit(1)

    FILENAME: str = sys.argv[1]
    VARIABLE_NAME: str = sys.argv[2]

    if not is_file_valid(FILENAME):
        sys.exit(1)

    found_variable = find_variable(FILENAME, VARIABLE_NAME)
    if found_variable:
        print(found_variable)
    else:
        print(f"Variable {VARIABLE_NAME} not found.")
        sys.exit(1)
