import constants

class Passenger(object):

    def __init__(self, start, end, start_time):
        self.start = start
        self.end = end
        self.start_time = start_time
        self.time_waited = 0
        self.on_elevator = False
