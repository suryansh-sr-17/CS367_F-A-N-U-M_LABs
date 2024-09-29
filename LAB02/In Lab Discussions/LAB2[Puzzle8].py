from collections import deque
import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

def get_successors(node):
    successors = []
    index = node.state.index(0)
    
    
    moves = {
        "up": -3,    
        "down": 3,  
        "left": -1,  
        "right": 1   
    }

    for move, move_val in moves.items():
        im = index + move_val
        if im >= 0 and im < 9:
            if move == "left" and index % 3 == 0:
                continue
            if move == "right" and (index + 1) % 3 == 0:
                continue
            
            new_state = list(node.state)
            new_state[index], new_state[im] = new_state[im], new_state[index]
            successor = Node(new_state, node)
            successors.append(successor)
    
    return successors

def bfs(start_state, goal_state):
    start_node = Node(start_state)
    goal_node = Node(goal_state)
    queue = deque([start_node])
    visited = set()
    nodes_explored = 0

    while queue:
        node = queue.popleft()
        if tuple(node.state) in visited:
            continue
        
        visited.add(tuple(node.state))
        nodes_explored += 1

        if node.state == list(goal_node.state):
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            print('Total nodes explored:', nodes_explored)
            return path[::-1]

        for successor in get_successors(node):
            queue.append(successor)

    print('Total nodes explored:', nodes_explored)
    return None

def print_matrix(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

start_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8] 

solution = bfs(start_state, goal_state)
if solution:
    print("Solution found:")
    for step in solution:
        print_matrix(step)
else:
    print("No solution found.")
