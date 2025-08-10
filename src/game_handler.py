from .board import Board
from .player import AI_Player, Player

class Game_Handler:
    def __init__(self, players, board):
        self.players = players
        self.current_player = self.players[0]
        self.board = board

    # def __init__(self, num_players, player_chars, width, height, num_to_win, empty_char, h_divider, v_divider):
    #     self.board = Board(width, height, num_to_win, empty_char, h_divider, v_divider)
    #     self.players = self.create_players(num_players, player_chars)
    #     self.current_player = self.players[0]
    #
    # def create_players(self, num_players, player_chars):
    #     players = []
    #     for i in range(1, num_players+1):
    #         input_value = input(f"Player {i}, enter your name: ")
    #         players.append(Player(input_value, player_chars[i-1]))
    #     players.append(AI_Player("AI", "🔵", ["🔴", "🔵"]))
    #     return players

    def set_next_player(self):
        self.current_player = self.players[(self.players.index(self.current_player) + 1) % len(self.players)]


    def game_loop(self):
        is_over = False
        is_draw = False
        move_valid = False
        column_value = 0

        while not is_over :
            self.set_next_player()
            self.board.print_board()
            
            # Check if valid moves remain
            if (len(self.board.get_valid_moves()) != 0):

                # Get input for a move until input is valid
                while not move_valid:
                    column_value = self.current_player.take_turn(self.board)
                    move_valid = self.board.validate_move(column_value)

                    if not move_valid:
                        print("Invalid column number")
                move_valid = False 

                # Add piece to the board
                self.board.add_piece(self.current_player.icon, column_value)
                is_over = self.board.check_player_win(self.current_player.icon)
            else: 
                is_draw = True

        self.board.print_board()

        if not is_draw:
            print(f"{self.current_player.name}, you have WON!")
        else:
            print("DRAW!")

