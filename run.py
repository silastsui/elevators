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

def process_elevator_moment(elevator):
    """Processes elevator movement across one second of time"""

    if elevator.direction == :

def process_lobby_person_movement(lobby_people):
    "Iterates through a list of people and increments one to their waiting time."

    for person in lobby_people:
        person.time_waited += 1

if __name__ == "__main__":

    #Process command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help="relative path of .json file")
    args = parser.parse_args()

    #Process constant variables from data
    data = get_parameters(args.filename)
    floor_count = data['floors']
    elevator_count = data['elevators']

    #Initialize elevator variables
    elevator = namedtuple("elevator", ["direction", "current_floor", "target_floor"
                                       "next_event_floor","next_event_time_left", "stopped"
                                       "people_carried", "people_scheduled"])

    elevators = []
    for _ in range(elevator_count):
        elevators.append(elevator("up", 0, 0, 0, 0, False, [], []))

    #Initialize people variables
    person = namedtuple("person", ["start_floor", "end_floor",
                                   "time_waited", "waiting_time"])
    lobby_people = []

    #Initialize event lists
    event_list = data['events']
    event_time_list = [event['time'] for event in event_list]
    current_events = []

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

        for elevator in elevators:
