from src.board import Board
import unittest

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.width = 7
        self.height = 6
        self.num_to_win = 4
        self.board = Board(self.width, self.height, self.num_to_win, "_")

    def test_validate_move(self):
        for i in range(self.width):
            self.assertTrue(self.board.validate_move(i))

        for i in range(self.width + 1,self.width + 3):
            self.assertFalse(self.board.validate_move(i))

    def test_add_piece(self):
        for i in range(self.width):
            self.board.add_piece("c", 0)
            self.board.add_piece("c", i)

        expected_board = [["_" for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            expected_board[i][0] = "c"

        for i in range(self.width - 1):
            expected_board[0][i + 1] = "c"

        self.assertEqual(self.board.board, expected_board)

    def test_check_player_win(self):
        for i in range(self.num_to_win):
            self.board.add_piece("c", i)

        self.assertTrue(self.board.check_player_win("c"))

    def test_check_player_win_horizontal(self):
        for i in range(self.height):
            for j in range(self.width - self.num_to_win + 1):
                for k in range(self.num_to_win):
                    self.board.board[i][j + k] = "c"
                self.assertTrue(self.board.check_player_win_horizontal("c"))
                self.reset_board()

    def test_check_player_win_vertical(self):
        for i in range(self.width):
            for j in range(self.height - self.num_to_win + 1):
                for k in range(self.num_to_win):
                    self.board.board[j + k][i] = "c"
                self.assertTrue(self.board.check_player_win_vertical("c"))
                self.reset_board()

    def test_check_player_win_diagonal_left(self):
        for i in range(self.width - self.num_to_win + 1):
            for j in range(self.height - self.num_to_win + 1):
                potential_row_index = i
                potential_column_index = j
                for _ in range(self.num_to_win):
                    self.board.board[potential_column_index][potential_row_index] = "c"
                    potential_row_index += 1
                    potential_column_index += 1
                self.assertTrue(self.board.check_player_win_diagonal_left("c"))
                self.reset_board()

    def test_check_player_win_diagonal_right(self):
        for i in range(self.num_to_win - 1, self.width):
            for j in range(self.height - self.num_to_win + 1):
                potential_row_index = i
                potential_column_index = j
                for _ in range(self.num_to_win):
                    self.board.board[potential_column_index][potential_row_index] = "c"
                    potential_column_index += 1
                    potential_row_index -= 1
                self.assertTrue(self.board.check_player_win_diagonal_right("c"))
                self.reset_board()

    def reset_board(self):
        self.board = Board(self.width, self.height, self.num_to_win, "_")
