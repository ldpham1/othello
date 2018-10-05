class InvalidInputError(Exception):
    """Raised whenever the user input is invalid"""
    pass

class GameOverError(Exception):
    """
    Raised whenever an attempt is made to make a move after
    the game has already ended
    """
    pass

class GameState:
    def __init__(self):
        self.num_of_rows = 0        #The total number of rows on the board
        self.num_of_columns = 0     #The total number of columns on the board
        self.turn = None            #Current player's turn
        self.winner_criteria = None #A string representing how the game is won
        self.board = None           #A list of nested lists containing the rows and columns of the board

        self.row = None               #The row the player wants to move to
        self.column = None             #The column the player wants to move to
        
        self.num_of_black_discs = 0 #Number of black discs currently on the board
        self.num_of_white_discs = 0 #Number of white discs currently on the board
        self.winner = None          #The winner of the game
        
    def get_num_of_rows(self):
        """Returns the user input for the number of rows on the game board"""
        self.num_of_rows = int(input())
        if self.num_of_rows not in range(4, 17) or self.num_of_rows % 2 != 0:
            raise InvalidInputError()
        return self.num_of_rows
        
    def get_num_of_columns(self):
        """Returns the user input for the number of columns on the game board"""
        self.num_of_columns = int(input())
        if self.num_of_columns not in range(4, 17) or self.num_of_rows % 2 != 0:
            raise InvalidInputError()
        return self.num_of_rows
    
    def determine_first_turn(self):
        """Returns the user input for which player gets to make the first move"""
        self.turn = input().upper()
        if self.turn != "B" and self.turn != "W":
            raise InvalidInputError()
        return self.turn

    def determine_winner_criteria(self):
        """Returns the user input for how the game will be won"""
        self.winner_criteria = input()
        if self.winner_criteria != ">" and self.winner_criteria != "<":
            raise InvalidInputError()
        return self.winner_criteria
    
    def get_and_create_starting_board(self) -> [[str]]:
        """
        Gets the user input for the starting board and returns a
        list of nested lists representing the board
        """
        rows = []
        for r in range(self.num_of_rows):
            row = input().split()
            rows.append(row)
        self.board = rows
        return self.board
    
    def count_discs_in_cell(self):
        """Returns the number of black and white discs currently on the board"""
        black_discs = 0
        white_discs = 0
        
        for nested_list in self.board:
            for element in nested_list:
                if element == "B":
                    black_discs += 1
                elif element == "W":
                    white_discs += 1
                    
        self.num_of_black_discs = black_discs
        self.num_of_white_discs = white_discs
        return self.num_of_black_discs, self.num_of_white_discs

    def list_of_valid_moves(self) -> [[int, int]]:
        """Creates a list of the valid moves the player can make"""
        valid_moves = []
        for row in range(self.num_of_rows):
            for column in range(self.num_of_columns):
                if self._is_valid_move(row, column) == True:
                    valid_moves.append([row, column])
        return valid_moves
    
    def make_a_move(self) -> str:
        """Executes the player's move"""
        try:
            while True:
                self._require_game_not_over()
                
                row_num, column_num = self._ask_for_move()
                
                if self._is_valid_move(row_num, column_num):
                    return "VALID"
                else:
                    print("INVALID")

        except ValueError:
            raise InvalidInputError()
        
    def new_turn(self):
        """Given whose turn it currently is, this function returns the opposite player"""
        if self.turn == "B":
            self.turn = "W"
            return self.turn
        
        elif self.turn == "W":
            self.turn = "B"
            return self.turn
        
    def new_board(self, row_num: int, column_num: int) -> [[str]]:
        """Returns a new board after the player has made a valid move"""
        copied_board = self._copy_board()
        cell, opponent_cell = self._define_cell_and_opponent_cell(row_num, column_num)
        if row_num != None and column_num != None:
            for i in self._cells_to_flip(row_num, column_num, cell, opponent_cell):
                copied_board[i[0]][i[1]] = cell
                
                copied_board[row_num][column_num] = self.turn
        else:
            return self.board
        
        self.board = copied_board
        
        return self.board
    
    def declare_winner(self) -> str:
        """Returns the winner of the game, or None if there is no winner"""
        if self.winner_criteria == ">":
            if self.num_of_black_discs > self.num_of_white_discs:
                self.winner = "B"
            elif self.num_of_white_discs > self.num_of_black_discs:
                self.winner = "W"
            else:
                self.winner = "NONE"
        if self.winner_criteria == "<":
            if self.num_of_black_discs < self.num_of_white_discs:
                self.winner = "B"
            elif self.num_of_white_discs < self.num_of_black_discs:
                self.winner = "W"
            else:
                self.winner = "NONE"

    def _ask_for_move(self) -> [int, int]:
        """Asks the player where they would like to place their disc"""
        action = input()
        row, column = action.split()
        row_num = int(row) - 1
        column_num = int(column) - 1
        self.row, self.column = row_num, column_num
        return self.row, self.column
    
    def _is_valid_move(self, row: int, column: int) -> bool:
        """Checks if the player's move is valid and returns False if it is not"""
        cell, opponent_cell = self._define_cell_and_opponent_cell(row, column)
        if len(self._cells_to_flip(row, column, cell, opponent_cell)) == 0:
            return False
        elif self._is_on_board(row, column) == False and cell != ".":
            return False
        return True
    
    def _copy_board(self) -> [[str]]:
        """Copies the game board"""
        board_copy = []
        for nested_list in self.board:
            board_copy.append(nested_list)
        return board_copy              

    def _is_on_board(self, row: int, column: int) -> bool:
        """Checks if the cell is on a valid place on the board"""
        if row in range(0, self.num_of_rows) and column in range(0, self.num_of_columns):
            return True
        else:
            return False

    def _define_cell_and_opponent_cell(self, row: int, column: int) -> [str, str]:
        """ Defines the variables 'cell' and 'opponent_cell' """
        if row != None and column != None:
            cell = self.board[row][column]
        else:
            cell = None
        opponent_cell = None
        
        if self._is_on_board(row, column) and cell == ".":
            cell = self.turn
            if cell == "B":
                opponent_cell = "W"
            elif cell == "W":
                opponent_cell = "B"
                
        return cell, opponent_cell
        
    def _cells_to_flip(self, row: int, column: int, cell: str, opponent_cell: str) -> [[str, str]]:
        """Returns a list of the cells that need to be flipped as a result of the player's move"""
        cells_to_flip = []
        check_all_directions = [[-1,0], [1,0], [0,-1], [0,1], [-1,1], [1,1], [-1,-1], [1,-1]]
        start_x, start_y = row, column
        
        for increment_x, increment_y in check_all_directions:
            middle_discs = 0
            x, y = row, column
            if self._is_on_board(x + increment_x, y + increment_y):
                if (self.board[x + increment_x][y + increment_y] == opponent_cell):
                    middle_discs += 1
                    x += increment_x
                    y += increment_y
                    
                    while self._is_on_board(x, y) and self.board[x][y] == opponent_cell:
                        middle_discs += 1
                        
                        x += increment_x
                        y += increment_y
                    if self._is_on_board(x, y) and self.board[x][y] == cell:
                        for num in range(1, middle_discs + 1):
                            cells_to_flip.append([start_x + num*increment_x, start_y + num*increment_y])
                        
        return cells_to_flip
    
    def _require_game_not_over(self):
        """
        Raises GameOverError if an attempt to make a move
        is made after the game has already ended
        """
        if self.winner != None:
            raise GameOverError()

