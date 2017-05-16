# WEC 2017 Spring - Programming Competition
## Problem Statement
Create an application that routes the path for the elevators of an apartment building in order to satisfy demands from tenants. A JSON file will be provided that includes the number of floors, `f`, the number of elevators, `e`, and a list that gives the call time, entry floor and exit floor for a number of people. The primary goal of the application is to minimize passenger waiting time, where the waiting time for each person is the number of seconds elapsed between the call time and the time the elevator carrying the person stops at the destination floor.

An elevator takes `3` seconds to move between floors and `10` seconds to stop at a floor. When an elevator is stopped, any number of people may enter or exit, but each elevator can hold a maximum of `5` people. All elevators start at floor 0.

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

## Main Algorithm
To optimize this problem, it makes sense to first create an algorithm for only 1 elevator and k floors. The problem gets much harder when we parallelize the elevators. I will also solve the problem given that it takes 1 second to change floors and 3 seconds to open/close the elevator doors since these numbers are easier to work with and it should be straightforward to apply the algorithm using different numbers. 

We notice that when there is a long amount of time between requests, the elevator simply fulfills requests in a FIFO order.
The tricky part is when we get overlapping requests and the elevator has to make tradeoffs. Consider the following test data:

| Time| Request|
| ----|:-------|
| 4   | (1, 7) |
| 7   | (7, 9) |
| 18  | (4, 5) |
| 21  | (0, 3) |
| 31  | (9, 7) |
| 35  | (4, 7) |
| 41  | (3, 6) |
| 47  | (1, 3) |
| 55  | (1, 5) |
| 60  | (3, 8) |

The optimal path of the elevator is `1 --> 7 --> 9 --> 0 --> 3 --> 4 --> 5 --> 9 --> 7 --> 1 --> 3 --> 5 --> 6 --> 8`, completing all 10 requests with 80 seconds of waiting time. If the requests were fulfilled in order, it would take 166 seconds.

There are a couple of observations from this test case:
* We know it is disadvantageous to prioritize people that make their requests earlier, since that often results in backtracking and extra stops. We assume that all passengers are in it for the greater good. 
* We saved time by dropping off two people on floor 7 at the same time. In general, we can reduce the waiting time by picking up more people on a floor. For a situation where you have 4 people on floor 4, and one person on floor 5, 6, and 7, it is ideal to pick up all the people on floor 4 (going in the same direction) and ignoring the loner floors. 
* It seems that we want to choose a route that maximizes distance travelled in one direction and that doesn't change direction unless it needs to. This may not be the case once we have a higher number of floors e.g. elevator going from floor 5 --> 100, and then it gets a request at floor 4. 
* All passengers in an elevator should be travelling in the same direction. The elevator should be able to pick up the other passengers when it returns in the opposite direction. There may be edge cases that contradict this, but as the number of passengers scales up, this seems like a fair assumption to make. 
