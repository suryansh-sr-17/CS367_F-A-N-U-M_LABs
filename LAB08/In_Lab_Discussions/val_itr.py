import numpy as np 
from enum import Enum


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class State:
    def __init__(self,start=(2,1),goal_positive=(3,0),goal_negative=(3,1),non_terminal_reward = -0.04):
        self.grid = np.array((4,3))
        self.start = start
        self.goal_negative = goal_negative
        self.goal_positive = goal_positive
        self.curr_position = start
        self.non_terminal_reward = non_terminal_reward

    # Checks
    def _in_bounds(self,point=None):
        if not point:
            point = self.curr_position
        x,y = point
        return 0<=x<4 and 0<=y<3

    def is_at_goal(self,point=None): # 0 for not , -1 ,1
        if not point:
            point = self.curr_position

        if point == self.goal_negative:
            return True,-1
        if point == self.goal_positive:
            return True,1
        return False,self.non_terminal_reward

    #  Action functions

    def _move(self,direction:Direction,point=None): # returns state info after a potential movement: is-goal, reward, position
        if not point:
            point = self.curr_position

        x,y = point 
        if direction == Direction.DOWN:
            dx,dy = (1,0)
        elif direction == Direction.UP:
            dx,dy = (-1,0)
        elif direction == Direction.RIGHT:
            dx,dy = (0,1)
        elif direction == Direction.LEFT:
            dx,dy = (0,-1)

        x_new,y_new = x+dx,y+dy

        if not self._in_bounds((x_new,y_new)):
            x_new,y_new = (x,y)
        
        return  x_new,y_new 

         
    # def step(self,direction:Direction): # probabilistic movement: actually moves
    #     val = direction.value
    #     directions = [
    #         direction,
    #         Direction((val+1)%4+1), # +90
    #         Direction((val-1)%4+1)  #-90
    #     ]
    #     probabilities = [0.8,0.1,0.1]
    #     chosen_direction = np.random.choice(directions,p=probabilities)
       
    #     self.curr_position = self._move(chosen_direction)[2]

def value_iteration(reward,discount = 0.95,theta = 1e-4):

    V = np.zeros((4,3))
    directions = list(Direction)

    V[3,0] =1
    V[3,1] = -1
    while True:
        V_new = np.copy(V)
        delta = 0

        for i in range(4):
            for j in range(3):
                state = (i,j)
                s = State(start=(i,j),non_terminal_reward=reward)

                is_goal,reward= s.is_at_goal()

                if is_goal:
                    V_new[i,j] = reward
                    continue

                action_values = []
                for action in directions:
                    value = 0

                    for p,a in zip(
                        [0.8,0.1,0.1],
                        [
                            action,
                            directions[(action.value-1)%4],
                            directions[(action.value+1)%4]
                        ]
                        ):
                        next_state = s._move(a,state)
                        _,next_reward = s.is_at_goal(next_state)
                        value+= p*(next_reward+discount*V[next_state])
                    action_values.append(value)

                V_new[i,j] = max(action_values)
                delta = max(delta,abs(V_new[i,j] - V[i,j])) 

        V= V_new
        if delta<theta:
            break
    return V



def main():
    rewards = [-2,0.1,0.02,1]

    for r_s in rewards:
        print(f"\nValue function for r(s) = {r_s}:\n{value_iteration(r_s)}\n")

if __name__ == "__main__":
    main()
