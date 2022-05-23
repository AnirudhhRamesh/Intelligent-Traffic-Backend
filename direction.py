#Direction enum class
from enum import Enum
from pickletools import UP_TO_NEWLINE
from turtle import up

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4