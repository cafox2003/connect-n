import os

class Board:
    def __init__(self, width, height, num_to_win, empty_char, h_divider, v_divider):
        self.width = width
        self.height = height
        self.num_to_win = num_to_win
        self.empty_char = empty_char
        self.h_divider = h_divider
        self.v_divider = v_divider
        self.board = []
        self.reset_board()

    def reset_board(self):
        self.board = [[self.empty_char for _ in range(self.width)] for _ in range(self.height)]

    def __eq__(self, other):
        if not isinstance(other, Board):
            return NotImplemented
        return (
            self.width == other.width and
            self.height == other.height and
            self.num_to_win == other.num_to_win and
            self.empty_char == other.empty_char and
            self.board == other.board
        )

    def __hash__(self):
        return hash((
            self.width,
            self.height,
            self.num_to_win,
            self.empty_char,
            tuple(tuple(row) for row in self.board)
        ))

    def print_board(self):
        if os.name == 'nt':
            os.system('cls')
        else:                
            os.system('clear')
        
        # Print header to show columns
        print(f"{self.v_divider}", end="")
        for i in range(self.width):
            print(f"{i}{self.v_divider}", end="")
        
        # print a divider
        print()
        for i in range(self.width * 2 + 1):
            print(f"{self.h_divider}", end="")
        print()

        reversed_rows = self.board[::-1]
        for row in reversed_rows:
            print(f"{self.v_divider}", end="")
            for char in row:
                print(f"{char}{self.v_divider}", end="")
            print()

    def add_piece(self, game_char, column):
        if (self.validate_move(column)):
            for i in range(self.height):
                position_char = self.board[i][column]

                if position_char == self.empty_char:
                    self.board[i][column] = game_char
                    break
        else:
            print(f"Invalid column: {column}")
    
    def validate_move(self, column):
        # Check width
        if column >= self.width:
            return False
        # Check height
        elif self.board[self.height - 1][column] != self.empty_char:
            return False
        else:
            return True

    def get_valid_moves(self):
        valid_moves = []
        for i in range(self.width):
            if self.validate_move(i):
                valid_moves.append(i)

        return valid_moves

    def check_win(self, game_chars):
        for char in game_chars:
            if self.check_player_win(char):
                return char

    def check_player_win(self, game_char):
        horizontal = self.check_player_win_horizontal(game_char)
        vertical = self.check_player_win_vertical(game_char)
        diag_l = self.check_player_win_diagonal_left(game_char)
        diag_r = self.check_player_win_diagonal_right(game_char)

        return (horizontal or vertical or diag_l or diag_r)

    def check_player_win_horizontal(self, game_char):
        checked_spaces = []

        for row_index in range(self.height):
            for column_index in range(self.width - self.num_to_win + 1):
                for potential_line_index in range(self.num_to_win):
                    checked_spaces.append(self.board[row_index][column_index + potential_line_index])

                if self.check_list_win(game_char, checked_spaces):
                    return True
                else:
                    checked_spaces = []
        return False

    def check_player_win_vertical(self, game_char):
        checked_spaces = []
        for column_index in range(self.width):
            for row_index in range(self.height - self.num_to_win + 1):
                for potential_line_index in range(self.num_to_win):
                    checked_spaces.append(self.board[row_index + potential_line_index][column_index])

                if self.check_list_win(game_char, checked_spaces):
                    return True
                else:
                    checked_spaces = []
        return False

    def check_player_win_diagonal_left(self, game_char):
        checked_spaces = []

        for column_index in range(self.width - self.num_to_win + 1):
            for row_index in range(self.height - self.num_to_win + 1):
                potential_row_index = row_index
                potential_column_index = column_index
                for _ in range(self.num_to_win):
                    checked_spaces.append(self.board[potential_row_index][potential_column_index])
                    potential_row_index += 1
                    potential_column_index += 1

                if self.check_list_win(game_char, checked_spaces):
                    return True
                else:
                    checked_spaces = []

        return False

    def check_player_win_diagonal_right(self, game_char):
        checked_spaces = []

        for column_index in range(self.num_to_win - 1, self.width):
            for row_index in range(self.height - self.num_to_win + 1):
                potential_row_index = row_index
                potential_column_index = column_index
                for _ in range(self.num_to_win):
                    checked_spaces.append(self.board[potential_row_index][potential_column_index])
                    potential_row_index += 1
                    potential_column_index -= 1

                if self.check_list_win(game_char, checked_spaces):
                    return True
                else:
                    checked_spaces = []
        return False

    def check_list_win(self, game_char, spaces_list):
        return all(x == game_char for x in spaces_list)

