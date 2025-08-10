import copy
import heapq
import itertools
import random

class Player:
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
        self.is_turn = False

    def take_turn(self, board):
        while True:
            user_input = input(f"\n{self.name} ({self.icon}), enter a column: ")
            try:
                return int(user_input)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

class AI_Player(Player):
    def __init__(self, name, icon, opponent_icons, max_search_depth=10, animate=False):
        self.opponent_icons = [char for char in opponent_icons if char != icon]
        self.counter = itertools.count()
        self.max_search_depth = max_search_depth
        self.animate = animate
        super().__init__(name, icon)

    def take_turn(self, board):
        visited = set()
        value = self.get_best_move([(self.get_heuristic(board), 0, board, 0)], visited=visited, depth=0)

        return value

    def get_best_move(self, board_states, visited, depth=0):
        if not board_states:
            return random.randint(0,6)

        priority, count, board, original_move = heapq.heappop(board_states)

        if depth > self.max_search_depth:
            return original_move

        if board in visited:
            # input("depth exceeded")
            return self.get_best_move(board_states, visited, depth=depth)
        visited.add(board)

        original_board = copy.deepcopy(board)


        # print(original_board)
        # print(original_board.width)

        # original_board.print_board()

        for i in range(original_board.width):
            temp_board = copy.deepcopy(original_board)

            # Skip invalid moves
            if (not temp_board.validate_move(i)):
                continue
            temp_board.add_piece(self.icon, i)

            if temp_board.check_player_win(self.icon):
                return original_move if not depth == 0 else i


            original_move = i if depth == 0 else original_move

            priority = self.get_heuristic(temp_board)
            
            if temp_board not in visited:
                heapq.heappush(board_states, (priority, next(self.counter), temp_board, original_move))

        return self.get_best_move(board_states, visited=visited, depth=depth+1)

    # Generates a heuristic on how well they're estimated to have played
    def get_heuristic(self, board):
        original_board = copy.deepcopy(board)
        start_num_to_win = board.num_to_win

        score = 0

        penalty = 0
        for char in self.opponent_icons:
            for col in range(board.width):
                temp_board = copy.deepcopy(board)
                if not temp_board.validate_move(col):
                    continue
                temp_board.add_piece(char, col)
                if temp_board.check_player_win(char):
                    penalty += 100_000  # Accumulate penalty for every opponent's winning move

        if penalty > 0:
            return -penalty
        # for char in self.opponent_icons:
        #     for col in range(board.width):
        #         temp_board = copy.deepcopy(board)
        #         if not temp_board.validate_move(col):
        #             continue
        #         temp_board.add_piece(char, col)
        #         if temp_board.check_player_win(char):
        #             return -1_000_000  # Huge penalty for leaving opponent win open
        #
        for i in range(2, start_num_to_win + 1):
            # print(f"\tNow playing: Connect-{i}""")
            original_board.num_to_win = i
            for char in self.opponent_icons:
                    # score -= i * self.get_ways_won(original_board, char)
                    score -=  self.get_score(original_board, i, char) * (10000 if i == start_num_to_win - 1 else 1)
            #         print(f"\tPoints subtratced: {self.get_score(original_board, i, char)}")
            # print(f"Points added: {self.get_score(original_board, i, self.icon)}")
            score += self.get_score(original_board, i, self.icon)


        if (self.animate):
            # print(f"Score: {score}")
            board.print_board()
        return score

    def get_score(self, board, i, char):
        return (self.get_ways_won(board, char) + 1) ** (i ** 2)
    
    # Returns 1 for each way that they have won
    def get_ways_won(self, board, char):
        horizontal = board.check_player_win_horizontal(char)
        vertical = board.check_player_win_vertical(char)
        diag_l = board.check_player_win_diagonal_left(char)
        diag_r = board.check_player_win_diagonal_right(char)

        return int(horizontal) + int(vertical) + int(diag_l) + int(diag_r)


