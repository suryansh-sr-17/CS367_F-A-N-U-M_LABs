import numpy as np
import scipy.stats as stats
from scipy.stats import poisson
import matplotlib.pyplot as plt

MOVEMENT_COST = -2
RENT_COST = 10
PARKING_COST = -4

MAX_FREE_PARKING = 10
EXPECT_REQUESTS = [3,4]
EXPECT_RETURNS = [3,2]
MAX_BIKES = 20
MAX_MOVE = 5
DISCOUNT_RATE= 0.9

class State:

    def __init__(self,bikes_1,bikes_2):
        self.bikes_1 = bikes_1
        self.bikes_2 = bikes_2

    def move_locations(self,action):
        action = max(-MAX_MOVE,min(action,MAX_MOVE))
        bikes_1 = min(MAX_BIKES,max(0,self.bikes_1-action) )
        bikes_2= min(MAX_BIKES,max(0,self.bikes_2+action))
        if action>0:
            move_reward = 0 if action==1 else MOVEMENT_COST*(abs(action)-1)
        else:
            move_reward = MOVEMENT_COST*abs(action)

        return bikes_1,bikes_2,move_reward


    def pmf(self,n,l):
        return stats.poisson.pmf(n,l)

def parking_cost(bikes):
    return PARKING_COST if bikes>MAX_FREE_PARKING else 0


def expected_reward(b1,b2,action,value):
    state = State(b1,b2)
    bikes_1,bikes_2,move_reward = state.move_locations(action)
    total_expected_reward = move_reward + parking_cost(bikes_1) + parking_cost(bikes_2)

    
    for req1 in range(0,MAX_BIKES+1):
        for req2 in range(0,MAX_BIKES+1):
            for ret1 in range(MAX_BIKES-bikes_1+1):
                for ret2 in range(MAX_BIKES-bikes_2+1):
                    prob = poisson.pmf(req1,EXPECT_REQUESTS[0])*poisson.pmf(req2,EXPECT_REQUESTS[1])*poisson.pmf(ret1,EXPECT_RETURNS[0])*poisson.pmf(ret2,EXPECT_RETURNS[1])

                    
                    actual_requests1 = min(bikes_1,req1)
                    actual_requests2 = min(bikes_2,req2)

                    new_bikes_1 = min(MAX_BIKES,bikes_1-actual_requests1+ret1)
                    new_bikes_2 = min(MAX_BIKES,bikes_2-actual_requests2+ret2)

                    reward = RENT_COST*(actual_requests1+actual_requests2)
                    total_expected_reward+= prob*(
                        reward+DISCOUNT_RATE*value[new_bikes_1,new_bikes_2]
                        + parking_cost(new_bikes_1)
                        + parking_cost(new_bikes_2)
                        )

    return total_expected_reward


def plot(value,policy):
    plt.figure(figsize=(12,6))

    plt.subplot(1,2,1)
    plt.contour(policy,levels = np.arange(-MAX_MOVE,MAX_MOVE+1),cmap='coolwarm')
    plt.colorbar(label='Overnight Bike Movement')
    plt.title('Policy Transfer Matrix')
    plt.xlabel('Location 2')
    plt.ylabel('Location 1')

    plt.subplot(1,2,2)
    plt.imshow(value,cmap='viridis',origin='lower')
    plt.colorbar(label='Value')
    plt.title('Value Function')
    plt.xlabel('Location 2')
    plt.ylabel('Location 1')

    plt.tight_layout
    plt.show()

def policy_iteration(theta = 1e-4):

    value = np.zeros((MAX_BIKES+1,MAX_BIKES+1))
    policy = np.zeros((MAX_BIKES+1,MAX_BIKES+1),dtype=int)

    delta = 1
        
    # POLICY Evaluation
    while delta>theta:
        delta = 0
        for i in range(MAX_BIKES+1):
            for j in range(MAX_BIKES+1):
                v = value[i,j]
                action = policy[i,j]
                value[i,j] = expected_reward(i,j,action,value)
                delta = max(delta,abs(v-value[i,j]))

            
    # POlicy Improvement
    while True:
        policy_stable = True

        for i in range(MAX_BIKES+1):
            for j in range(MAX_BIKES+1):
                action = policy[i,j]
                best_action = max(range(-MAX_MOVE,MAX_MOVE+1),key=lambda x: State.expected_reward(i,j,x,value))
                policy[i,j] = best_action

                if action!= best_action:
                    policy_stable=False
        if policy_stable:
            break
    
    return value,policy

if __name__ == "__main__":
    value,policy = policy_iteration()
    print("Optimal Value Function: ")
    print(value)
    print("Optimal Policy: ")
    print(policy)
    plot(value,policy)
