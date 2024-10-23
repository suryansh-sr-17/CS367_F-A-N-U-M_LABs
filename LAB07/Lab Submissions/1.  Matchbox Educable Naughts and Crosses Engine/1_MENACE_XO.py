import random

class MENACE:
    def __init__(self):
        self.matchboxes = {}  # Maps game states to lists of move beads
        self.history = []  # Tracks moves made during a game
    
    def get_symmetrical_state(self, state):
        # For now, treat the state as-is (add symmetry handling later if needed)
        return tuple(state)
    
    def choose_move(self, state):
        state = self.get_symmetrical_state(state)
        if state not in self.matchboxes:
            self.matchboxes[state] = self.initialize_moves(state)
        
        move = random.choices(list(self.matchboxes[state].keys()), 
                              weights=self.matchboxes[state].values())[0]
        self.history.append((state, move))
        return move
    
    def initialize_moves(self, state):
        # Create an initial move set for the given state
        return {i: 1 for i in range(9) if state[i] == ' '}
    
    def update_learning(self, result):
        # Adjust bead counts based on the game result
        reward = 3 if result == 'win' else (1 if result == 'draw' else -1)
        for state, move in self.history:
            if move in self.matchboxes[state]:
                self.matchboxes[state][move] = max(
                    1, self.matchboxes[state][move] + reward
                )
        self.history.clear()
    
    def play_game(self, opponent_type='human'):
        state = [' '] * 9
        turn = 'X'  # MENACE always starts as 'X'
        
        while True:
            self.display_board(state)
            if turn == 'X':
                print("MENACE's turn:")
                move = self.choose_move(state)
                state[move] = 'X'
            else:
                if opponent_type == 'human':
                    move = self.user_move(state)
                else:
                    move = self.random_opponent(state)
                state[move] = 'O'
            
            if self.check_winner(state):
                self.display_board(state)
                print(f"{turn} wins!")
                self.update_learning('win' if turn == 'X' else 'lose')
                break
            elif ' ' not in state:
                self.display_board(state)
                print("It's a draw!")
                self.update_learning('draw')
                break
            
            turn = 'O' if turn == 'X' else 'X'
    
    def user_move(self, state):
        # Ask the user for a valid move
        while True:
            try:
                move = int(input("Your turn (0-8): "))
                if 0 <= move < 9 and state[move] == ' ':
                    return move
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a number between 0 and 8.")
    
    def random_opponent(self, state):
        # Randomly select a valid move
        return random.choice([i for i, cell in enumerate(state) if cell == ' '])
    
    def display_board(self, state):
        # Display the Tic-tac-toe board
        board = [state[i] if state[i] != ' ' else str(i) for i in range(9)]
        print("\n")
        print(f"{board[0]} | {board[1]} | {board[2]}")
        print("---------")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print("---------")
        print(f"{board[6]} | {board[7]} | {board[8]}")
        print("\n")
    
    def check_winner(self, state):
        # Check if there's a winning line on the board
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in lines:
            if state[a] == state[b] == state[c] and state[a] != ' ':
                return True
        return False
    
    def evaluate_game(self, state):
        # Determine the game's outcome for MENACE
        if self.check_winner(state):
            return 'win' if state.count('X') > state.count('O') else 'lose'
        return 'draw'

# Main function to train or play with MENACE
def main():
    menace = MENACE()
    print("Welcome to Tic-tac-toe! You are playing as 'O'.")
    
    while True:
        choice = input("Do you want to train MENACE with a random opponent or play against it? (train/play): ").lower()
        if choice == 'train':
            for _ in range(100):
                menace.play_game(opponent_type='random')
            print("Training completed with 100 games.")
        elif choice == 'play':
            menace.play_game(opponent_type='human')
        else:
            print("Invalid choice. Please select 'train' or 'play'.")
            continue
        
        play_again = input("Do you want to continue? (y/n): ").lower()
        if play_again != 'y':
            break

# Run the main function
if __name__ == "__main__":
    main()
