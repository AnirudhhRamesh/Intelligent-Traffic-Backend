#Direction enum class
from enum import Enum

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    
    def toString(self):
        if self == Direction.UP:
            return "^"
        if self == Direction.DOWN:
            return "V"
        if self == Direction.LEFT:
            return "<"
        else:
            return ">"
