"""
Name: Lillian Pham
ID: 68168196
"""

import game_logic

def run_game():
    """Main function that runs the whole game"""
    print("FULL")
    try:
        g = game_logic.GameState()
        
        rows = g.get_num_of_rows()
        columns = g.get_num_of_columns()   
        first_turn = g.determine_first_turn()
        winner_criteria = g.determine_winner_criteria()
        
        board = g.get_and_create_starting_board()
        while g.winner == None:
            run_turns(g)
        
        print("WINNER:", g.winner)
        
    except game_logic.InvalidInputError:
        print("Invalid input.")
    except game_logic.GameOverError:
        print("You attempted to make a move after the game already ended.")

def print_board(g: game_logic.GameState):
    """Prints the current game board"""
    for nested_list in g.board:
        print(" ".join(nested_list))

def run_turns(g: game_logic.GameState):
    """Runs the player's turn and ends if there are no more valid moves"""
    valid_moves = g.list_of_valid_moves()
    if len(valid_moves) == 0:
        g.count_discs_in_cell()
        print("B:", g.num_of_black_discs, " W:", g.num_of_white_discs)
        g.new_board(g.row, g.column)
        g.new_turn()
        valid_moves = g.list_of_valid_moves()
        if len(valid_moves) == 0:
            g.new_board(g.row, g.column)
            print_board(g)
            g.declare_winner()
            return
    else:
        g.count_discs_in_cell()
        print("B:", g.num_of_black_discs, " W:", g.num_of_white_discs)
        
    print_board(g)
    print("TURN:", g.turn)
    g.make_a_move()
    print("VALID")
    g.new_board(g.row, g.column)
    g.new_turn()
    
if __name__ == "__main__":
    run_game()
