import cell


class Passenger:
    """
    Initializes a passenger instance
    ---
    start: Start cell where passenger is located
    goal: Goal cell where passenger wishes to be dropped off
    """
    def __init__(self, start:cell.Cell, goal:cell.Cell):
        self.start = start
        self.goal = goal