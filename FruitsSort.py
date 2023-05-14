import sys
from heapq import heappush, heappop
from itertools import permutations

# Defined a class called 'Fruits' with a constructor and a less than method
class Fruits:
    def __init__(self, type, size):
        self.type = type
        self.size = size

    def __lt__(self, other):
        return self.size < other.size

# Defined a function to print the data
def printData(data):
    for row in data:
        for val in row:
            print(str(val.type)+ str(val.size), end=" ")
        print()

# Defined a heuristic function
def heuristic(state, goal_state):
    total_distance = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            goal_i, goal_j = next((x, y) for x in range(len(goal_state)) for y in range(len(goal_state[x])) if goal_state[x][y].type == state[i][j].type and goal_state[x][y].size == state[i][j].size)
            total_distance += abs(i - goal_i) + abs(j - goal_j) # Manhattan distance calculated
    return total_distance

# Define a function to get the neighboring swapped states
def neighbors(state):
    neighbor_states = []
    for i in range(len(state)):
        for j in range(len(state[i])):
            # Swap vertically with the cell below
            if i + 1 < len(state):
                new_state = [list(row) for row in state]
                new_state[i][j], new_state[i + 1][j] = new_state[i + 1][j], new_state[i][j]
                neighbor_states.append((tuple(tuple(row) for row in new_state), 1))
                
            # Swap horizontally with the cell to the right
            if j + 1 < len(state[i]):
                new_state = [list(row) for row in state]
                new_state[i][j], new_state[i][j + 1] = new_state[i][j + 1], new_state[i][j]
                neighbor_states.append((tuple(tuple(row) for row in new_state), 1))
                
    return neighbor_states

# Defined a function to sort the fruits
def FruitsSort(start_state):
    letters = list({fruit.type for row in start_state for fruit in row})  # Create a list of unique fruit types
    print(letters) 
    permutations_list = list(permutations(letters))  # Create a list of all permutations of the unique fruit types
    goal_state = [] 

    for _ in permutations_list:
        goal_state.append([]) 
    
    for idx, perm in enumerate(permutations_list):  # For each permutation in the list of permutations
        # Create a goal state by sorting the fruits by type and size
        goal_state[idx] = [
            sorted([fruit for row in start_state for fruit in row if fruit.type == perm[i]], key=lambda x: x.size)
            for i in range(len(letters))
        ]
        print("Goal state "+str(idx+1)+":") 
        printData(goal_state[idx]) 
    
    solution_swaps = []  #
    for _ in goal_state:  
        solution_swaps.append(float('inf'))  # Append infinity to the list of solution swaps

    for idx, goal in enumerate(goal_state):  # For each goal state
        solution_swaps[idx] = Solution(start_state, goal)  # Set the solution swap at the index to the cost of the solution for that goal state
        print(solution_swaps[idx]) 
    
    min_solution = min(solution_swaps)  # Set the minimum solution to the minimum solution swap
    if min_solution == float('inf'): 
        return -1  
    else: 
        return min_solution  # Return the minimum solution

# Defined a function to find the solution    
def Solution(start_state, goal_state):
    frontier = [(0, start_state, 0)]
    visited = set()

    while frontier:
        _, state, cost_so_far = heappop(frontier)

        # Check if the state is the goal state
        if state == goal_state:
            return cost_so_far

        # Convert the state to a hashable representation
        state_tuple = tuple(tuple(row) for row in state)

        if state_tuple in visited:
            continue

        visited.add(state_tuple)

        # Generate neighboring states and calculate their costs
        for next_state, cost in neighbors(state):
            new_cost = cost_so_far + cost
            heuristic_cost = heuristic(next_state, goal_state)
            total_cost = new_cost + heuristic_cost

            heappush(frontier, (total_cost, next_state, new_cost))

    return float('inf')  # Solution not found

# Defined a function to get the data from a file
def getData(filename):
    fruits = []
    with open(filename, 'r') as f:
        for line in f:
            row = []
            fruit_vals = line.strip().split()
            for val in fruit_vals:
                fruit = Fruits(val[0], int(val[1:])) # type and size
                row.append(fruit)
            fruits.append(row)
    fruits_data = tuple(tuple(row) for row in fruits)
    print("Fruits Current Arrangement:")
    printData(fruits_data)
    return fruits_data

# Defined the main function
def main():
    if len(sys.argv) <= 1:
        return
    else:
        filename = sys.argv[1]
        if ".txt" in filename:
            if len(sys.argv) < 2:
                return
            else:
                print("Solution : ",FruitsSort(getData(filename)))

if __name__ == '__main__':
    main()