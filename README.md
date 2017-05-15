# WEC 2017 Spring - Programming Competition
## Problem Statement
Create an application that routes the path for the elevators of an apartment building in order to satisfy demands from tenants. A JSON file will be provided that includes the number of floors, the number of elevators, and a list that gives the call time, entry floor and exit floor for a number of people. The primary goal of the application is to minimize passenger waiting time, where the waiting time for each person is the number of seconds elapsed between the call time and the time the elevator carrying the person stops at the destination floor.

An elevator takes 3 seconds to move between floors and 10 seconds to stop at a floor. When an elevator is stopped, any number of people may enter or exit, but each elevator can hold a maximum of 5 people. All elevators start at floor 0.

The application should plan what direction the elevators are going and when they should stop. The application cannot use data about future events to make decisions. The application should run for 1000 seconds or until all people have reached their floors; whichever is longer. At each second, the application should display the state of the elevators in a GUI, as well as output the current state of the elevators into a text file.

### GUI Details
The GUI should portray the following:
* Direction each elevator is moving
* People entering, travelling in, and exiting the elevator
* The time it takes for each person to travel to their destination
* The number of people currently waiting (at a floor, and total)
* The cumulative waiting time at the current time

### Output File Details
The output file should output lines in the form `T, (F1, P1), (F2, P2), (F3, P3), ...`, where T is the current time, followed by N tuples of (F, P) where N is the number of elevators, F is the current floor the elevator is on, and P is the number of people in the elevator.
The final line should be a single integer with the total waiting time of all the people.

### Test Cases
The code for generating test cases can be found here: https://gist.github.com/csgregorian/aff8570369544a1e02adf5adfe6cadbc#file-testcases-py

