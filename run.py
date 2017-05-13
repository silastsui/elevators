import argparse
import ast
from collections import namedtuple
import json

import config
import constants

def get_parameters(filename):
    """Parses through a .json file and returns the data
    as a dictionary. This function assumes the .json file is valid."""

    with open(filename) as f:
        elev = ast.literal_eval(f.read())
    return elev

def get_next_event(event_list, event_time_list, current_time):
    """Gets the next event(s) in the JSON file at the specified
    time and returns them."""
    event_num = event_time_list.count(current_time)
    events = []
    for event in range(event_num):
        events.append(event_list[event])
    for event in range(event_num):
        event_list.pop(0)
        event_time_list.pop(0)

    return events

if __name__ == "__main__":

    #Process command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help="relative path of .json file")
    args = parser.parse_args()

    #Process constant variables
    data = get_parameters(args.filename)

    floor_count = data['floors']
    elevator_count = data['elevators']

    event_list = data['events']
    event_time_list = [event['time'] for event in event_list]
    current_events = []

    elevator = namedtuple("elevator", ["direction_up", "current_floor",
                                       "next_event_floor","next_event_time_left",
                                       "people"])

    elevators = []
    for _ in range(elevator_count):
        elevators.append(elevator(True, 0, 0, 0, []))

    total_waiting_time = 0

    #Program Main Loop
    for current_time in range(constants.max_time):
        #Get new events
        new_events = get_next_event(event_list, event_time_list, current_time)
        for event in new_events:
            current_events.append(event)

        #Process new events
        if new_events:

            process where elevators are going

        # for elevator in elevators
