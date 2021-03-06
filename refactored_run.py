import argparse
import ast
from collections import namedtuple
import json

import constants
from elevator import Direction, Elevator
from passenger import Passenger

def get_next_events(events, event_times, current_time):
    """Gets the next event(s) in the JSON file at the specified
    time and returns them."""
    if event_times == []:
        return []

    curr_events = []
    while event_times[0] == current_time:
        curr_events.append(events[0])
        events.pop(0)
        event_times.pop(0)

    return curr_events

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

        if (len(elevator.people_carried) + len(elevator.people_scheduled)) == 0:
            elevator = elevator._replace(direction="stop")
    # If elevator is moving up or down a floor
    else:
        elevator = elevator._replace(stopped = False)
        elevator = elevator._replace(current_floor = elevator.next_event_floor)
        elevator = elevator._replace(next_event_time_left = 3)

    if elevator.next_stopped_floor - elevator.current_floor > 0:
        elevator = elevator._replace(next_event_floor = elevator.current_floor + 1)
    elif elevator.next_stopped_floor - elevator.current_floor < 0:
        elevator = elevator._replace(next_event_floor = elevator.current_floor - 1)

    return elevator

def process_person_movement(waiting_people):
    "Iterates through a list of people and increments one to their waiting time."

    for person in range(len(waiting_people)):
        waiting_people[person] = waiting_people[person]._replace(time_waited=waiting_people[person].time_waited + 1)

def convert_event_to_person(event):
    """Converts a event with dictionary type into a person with namedtuple type"""
    start_floor = event['start']
    end_floor = event['end']
    if end_floor - start_floor > 0:
        direction = "up"
    else:
        direction = "down"
    return _person(start_floor, end_floor, direction, 0, 0)

def calculate_pick_up(elevator,waiting_person):
    total_time = 0

    for person in elevator.people_carried:
        total_time += person.waiting_time
        total_time += get_extra_waiting_time(elevator, person, waiting_person)

    for person in elevator.people_scheduled:
        total_time += person.waiting_time
        total_time += get_extra_waiting_time(elevator, person, waiting_person)

    total_time += waiting_person.time_waited
    return total_time

def get_extra_waiting_time(elevator, person, waiting_person):
    distance = elevator.current_floor - waiting_person.start_floor
    time = 0
     #if opposite direction
    if (distance > 0 and  elevator.direction == "up") or (distance < 0 and elevator.direction == "down"):
        time = abs(distance) * 6 + 10
    #elif the person stop exceeds the waiting_person entry point, then add 10
    elif (person.end_floor > waiting_person.start_floor and elevator.direction == "up") or (person.end_floor < waiting_person.start_floor and elevator.direction == "down"):
        time = 10
    #if the waiting person's stop is before the person in elevator's stop
    if (person.end_floor > waiting_person.end_floor and elevator.direction == "up") or (person.end_floor < waiting_person.end_floor and elevator.direction == "down"):
        time += 10

    return time

def calculate_not_pick_up(elevator, waiting_person):
    total_time = 0
    stops = []
    for person in elevator.people_carried:
        total_time += person.waiting_time
        if person.end_floor not in stops:
            stops.append(person.end_floor)

    for person in elevator.people_scheduled:
        total_time += person.waiting_time
        if person.end_floor not in stops:
            stops.append(person.end_floor)

    total_time += waiting_person.time_waited

    total_time += len(stops) * 10

    if elevator.direction == "up":
        total_time += abs(max(stops) - waiting_person.start_floor) * 3
    elif elevator.direction == "down":
        total_time += abs( waiting_person.start_floor - min(stops) ) * 3
    return total_time

def add_to_elevator(elevators, waiting_person):
    use_elevator = -1
    total_time_of_pickup_elevator = 10000 * len(elevators)
    added = False
    for i, elevator in enumerate(elevators):

        total_time = total_time_of_pickup_elevator
        if elevator.direction == "stop":
            total_time = (elevator.current_floor - waiting_person.start_floor)*3 + 10
            if total_time_of_pickup_elevator > total_time:
                use_elevator = i
                total_time_of_pickup_elevator = total_time
        #If the direction is the same and the elevator has less than 5 ppl
        elif elevator.direction == waiting_person.direction and len(elevator.people_carried)+len(elevator.people_scheduled) < 5:
            pickup = calculate_pick_up(elevator, waiting_person)
            not_pickup = calculate_not_pick_up(elevator, waiting_person)
            total_time = pickup
            if pickup < not_pickup:
                for i1, elevator1 in enumerate(elevators):
                    if i1 != i:
                        for person in elevator1.people_carried:
                            total_time += person.waiting_time
                        for person in elevator1.people_scheduled:
                            total_time += person.waiting_time

                if total_time_of_pickup_elevator > total_time:
                    use_elevator = i
                    total_time_of_pickup_elevator = total_time

    if use_elevator >= 0:
        elevator = elevators[use_elevator]
        waiting_person = waiting_person._replace(waiting_time = 0)
        if elevator.direction == "stop":
            if (waiting_person.end_floor > waiting_person.start_floor):
                elevators[use_elevator] = elevators[use_elevator]._replace(direction = "up")
            else:
                elevators[use_elevator] = elevators[use_elevator]._replace(direction = "down")

        for person in elevator.people_carried:
            person = person._replace(waiting_time=person.waiting_time + get_extra_waiting_time(elevator, person, waiting_person))
            if (waiting_person.end_floor > person.end_floor and elevator.direction == "up" or waiting_person.end_floor < person.end_floor and elevator.direction == "down"):
                waiting_person = waiting_person._replace(waiting_time = waiting_person.waiting_time + 10)

        for person in elevator.people_scheduled:
            person = person._replace(waiting_time=person.waiting_time + get_extra_waiting_time(elevator, person, waiting_person))
            if (waiting_person.end_floor > person.end_floor and elevator.direction == "up" or waiting_person.end_floor < person.end_floor and elevator.direction == "down"):
                waiting_person = waiting_person._replace(waiting_time = waiting_person.waiting_time + 10)

        waiting_person = waiting_person._replace(waiting_time = waiting_person.time_waited + 10)
        elevator = elevator._replace(people_scheduled = elevator.people_scheduled.append(waiting_person))
        added = True
    return added

def transfer_people_into_elevator(elevator):
    "Transfers people inside elevator to their destination"
    enter_people = [person for person in elevator.people_scheduled if person.start_floor == elevator.current_floor]
    for person in enter_people:
        elevator.people_scheduled.remove(person)
        elevator.people_carried.append(person)

def transfer_people_out_elevator(elevator):
    global total_waiting_time
    "Transfers people from people_scheduled into elevator"
    exit_people = [person for person in elevator.people_carried if person.end_floor == elevator.current_floor]
    for person in exit_people:
        elevator.people_carried.remove(person)
        total_waiting_time += person.time_waited

    return total_waiting_time

if __name__ == "__main__":
    #Process command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help="relative path of .json file")
    args = parser.parse_args()

    with open(constants.TEST_CASES + args.filename) as f:
        data = json.loads((f.read()))

    floor_count = data['floors']
    elevator_count = data['elevators']
    events = data['events']
    event_times = [event['time'] for event in events]

    passengers = []
    elevators = []

    for elevator in range(elevator_count):
        elevators.append(Elevator())

    #Program main loop
    total_waiting_time = 0
    for time in range(constants.END_TIME):
        # Get new passengers
        for event in get_next_events(events, event_times, time):
            passengers.append(Passenger(event['start'], event['end'], event['time']))

        #Assign new people to elevator or keep them in waiting_people
        if waiting_people:
            new_waiting_people = []
            for person in waiting_people:
                if not add_to_elevator(elevators, person):
                    new_waiting_people.append(person)
            waiting_people = new_waiting_people

        #Adjust elevator path based on new scheduled people
        for elevator in range(len(elevators)):
            destinations = [people.end_floor for people in elevators[elevator].people_carried]
            destinations += [people.start_floor for people in elevators[elevator].people_scheduled]
            if destinations != []:
                if elevators[elevator].direction == "up":
                    next_floor = min(destinations)
                    elevators[elevator] = elevators[elevator]._replace(next_stopped_floor=next_floor)
                else:
                    next_floor = max(destinations)
                    elevators[elevator] = elevators[elevator]._replace(next_stopped_floor=next_floor)


        #Process waiting time and elevator movement
        process_person_movement(waiting_people)
        for elevator in range(len(elevators)):
            elevators[elevator] = process_elevator_movement(elevators[elevator])
            process_person_movement(elevators[elevator].people_carried)
            process_person_movement(elevators[elevator].people_scheduled)

        # Log elevator statuses
        with open("output.txt", "a") as f:
            text = ""
            for elevator in elevators:
                text += "({}, {}) ".format(elevator.current_floor, len(elevator.passengers))
            f.write("{}: {} \n".format(current_time, text))

    #Reporting
    print(total_waiting_time)
