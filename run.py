import argparse
import ast
from collections import namedtuple
import json

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

def process_elevator_movement(elevator):
    """Processes elevator movement across one second of time"""
    elevator = elevator._replace(next_event_time_left = elevator.next_event_time_left - 1)
    if elevator.next_event_time_left != 0:
        return elevator

    # If elevator is opening and closing its door
    if elevator.next_event_floor == elevator.current_floor and not elevator.stopped:
        elevator = elevator._replace(next_event_time_left = 10)
        elevator = elevator._replace(stopped = True)
        # Doors are open, so let people enter/exit
        transfer_people_out_elevator(elevator)
        transfer_people_into_elevator(elevator)
    # If elevator is moving up or down a floor
    else:
        elevator = elevator._replace(current_floor = elevator.next_event_floor)
        elevator = elevator._replace(next_event_time_left = 3)

    if elevator.target_floor - elevator.current_floor > 0:
        elevator = elevator._replace(next_event_floor = elevator.current_floor + 1)
    elif elevator.target_floor - elevator.current_floor < 0:
        elevator = elevator._replace(next_event_floor = elevator.current_floor - 1)

    return elevator

def process_person_movement(waiting_people):
    "Iterates through a list of people and increments one to their waiting time."

    for person in waiting_people:
        person = person._replace(time_waited = person.time_waited + 1)

def convert_event_to_person(event):
    """Converts a event with dictionary type into a person with namedtuple type"""
    start_floor = event['start']
    end_floor = event['end']
    if end_floor - start_floor > 0:
        direction = "up"
    else:
        direction = "down"
    return _person(start_floor, end_floor, direction, 0, 0)

def transfer_people_into_elevator(elevator):
    "Transfers people inside elevator to their destination"
    enter_people = [person for person in elevator.scheduled if person['start_floor'] == elevator.current_floor]
    for person in exit_people:
        elevator.people_scheduled.remove(person)
        elevator.people_carried.append(person)

def transfer_people_out_elevator(elevator):
    "Transfers people from people_scheduled into elevator"
    exit_people = [person for person in elevator.people_carried if person['end_floor'] == elevator.current_floor]
    for person in exit_people:
        elevator.people_carried.remove(person)
        total_waiting_time += person.time_waited

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
    _elevator = namedtuple("elevator", ["direction", "current_floor", "target_floor", "stopped",
                                       "next_stopped_floor", "next_event_floor","next_event_time_left",
                                       "people_carried", "people_scheduled"])

    elevators = []
    for _ in range(elevator_count):
        elevators.append(_elevator("up", 0, 6, False, 6, 1, 3, [], []))

    #Initialize people variables
    _person = namedtuple("person", ["start_floor", "end_floor", "direction",
                                   "time_waited", "waiting_time"])
    waiting_people = []

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
            waiting_people.append(convert_event_to_person(event))

        #Process new events
        for person in waiting_people:
            for elevator in range(len(elevators)):
                a = "A"
                #calculate the new waiting time if this elevator took it
            #make calculations about where to assign the person

            #Assign people to elevators
            fastest_elevator = 5
            elevators[fastest_elevator].people_scheduled.append(person)
            #process where elevators are going

        #Process waiting time and elevator movement
        process_person_movement(waiting_people)
        for elevator in range(len(elevators)):
            elevators[elevator] = process_elevator_movement(elevators[elevator])
            process_person_movement(elevators[elevator].people_carried)
            process_person_movement(elevators[elevator].people_scheduled)
