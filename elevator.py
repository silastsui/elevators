from enum import Enum, auto
import constants

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    STOP = auto()

class Elevator(object):
    size = constants.ELEVATOR_SIZE

    def __init__(self):
        passengers = []
        direction = Direction.STOP
        current_floor = 0
        next_floor = 0
        floor_queue = []
        passenger_queue = []
