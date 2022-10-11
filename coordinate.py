
"""\
This module provides functions that allows users to process move coordinates.

Functions:
parse_coordinate() -- parse strings to coordinates of integers
"""

from typing import Tuple


def parse_coordinate(coordinate_str: str) -> Tuple[int, int]:
    '''Parse input of strings to coordinates of integers.

    Args:
        coordinate_str: A string represents coordinates of the slot

    Returns:
        A tuple with two integers represents the coordinates of the slot
    '''
    coordinate_list = coordinate_str.split(',')
    if len(coordinate_list) != 2:    # The coordinate list is valid only when it's length equal to 2
        return -1, -1

    coordinate_list[0] = coordinate_list[0].strip()
    coordinate_list[1] = coordinate_list[1].strip()

    if not coordinate_list[0].isdigit() or not coordinate_list[1].isdigit():    # The coordinate list is valid only when it's made up of digits
        return -1, -1

    coordinate_x = int(coordinate_list[0])
    coordinate_y = int(coordinate_list[1])

    return coordinate_x, coordinate_y

