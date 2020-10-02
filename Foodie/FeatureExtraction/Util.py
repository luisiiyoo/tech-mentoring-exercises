from typing import List, Dict, Set, Union
from termcolor import colored, cprint


class Color:
    REGISTERS = 'red'
    NO_REQUEST = 'yellow'
    REQUEST = 'blue'
    ATTEND_REQUEST = 'green'
    NO_ATTEND_REQUEST = 'magenta'


def printColored(data: Dict[str, Union[str, int]]) -> None:
    keys_list = ['Date', 'Day', 'Diet', 'TotalPeople',
                 'TotalRequests', 'Request', 'Attend']
    colors_list = ['white', 'white', 'magenta', 'red', 'blue', 'cyan', 'green']
    COLORS = dict(zip(keys_list, colors_list))
    cad: str = ''
    for key in keys_list:
        val = colored(data[key], COLORS[key])
        cad += f' {val:^24s} '
    print(cad)


DIETS = ['Regular', 'Vegetarian', 'Light', 'Vegan']
