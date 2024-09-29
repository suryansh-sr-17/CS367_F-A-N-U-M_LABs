from collections import deque

# Validity Check
def is_valid(state):
    missionaries, cannibals, boat = state
    if missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3:
        return False
    if missionaries > 0 and missionaries < cannibals:
        return False
    if 3 - missionaries > 0 and 3 - missionaries < 3 - cannibals:
        return False
    return True

# Successor generation from a given state
def get_successors(state):

    successors = []
    missionaries, cannibals, boat = state

    if boat == 1:  # Boat on the starting side
        moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
        for move in moves:
            new_state = (missionaries - move[0], cannibals - move[1], 0)
            if is_valid(new_state):
                action = f"Moved {move[0]} missionary(ies) and {move[1]} cannibal(s) from starting side to ending side.\n"
                successors.append((new_state, action))

    else:  # Boat on the ending side
        moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
        for move in moves:
            new_state = (missionaries + move[0], cannibals + move[1], 1)
            if is_valid(new_state):
                action = f"Moved {move[0]} missionary(ies) and {move[1]} cannibal(s) from ending side to starting side.\n"
                successors.append((new_state, action))

    return successors

# BFS algorithm to find solution path
def bfs(start_state, goal_state):

    queue = deque([(start_state, [])])
    visited = set()

    while queue:
        (state, path) = queue.popleft()
        if state in visited:
            continue
        visited.add(state)

        for successor, action in get_successors(state):
            if successor not in visited:
                new_path = path + [(successor, action)]
                if successor == goal_state:
                    return new_path
                queue.append((successor, new_path))

    return None

start_state = (3, 3, 1) # start state
goal_state = (0, 0, 0)  # goal state


solution = bfs(start_state, goal_state)

counter = 0

if solution:

    print("\nSolution found:\n")

    for step, action in solution:
        print(step)
        print(action)
        counter += 1
        
else:
    print("No solution found.")

print("Thus, total number of steps executed for the above problem are: ", counter, "\n")
print("Thank You !!!\n")
