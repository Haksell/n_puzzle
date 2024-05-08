from enum import IntEnum


class Move(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opposite(self):
        return Move(self.value ^ 2)
