import random
import copy
from solver import solve_board

class SudokuGenerator:
    def __init__(self, size=4):
        self.size = size
        self.box_r, self.box_c = 2, 2

    def generate_full_board(self):
        empty_board = [[0]*self.size for _ in range(self.size)]
        solutions, _, _ = solve_board(self.size, empty_board, max_solutions=1, randomize=True)
        if not solutions:
            raise RuntimeError("Failed to generate full board")
        return solutions[0]

    def _determine_difficulty(self, removed_count, guess_count):
        if guess_count > 1 or removed_count >= 10:
            return 'Hard'
        elif guess_count == 1 or removed_count >= 9:
            return 'Medium'
        return 'Easy'

    def remove_clues_target(self, board, max_clues_to_remove):
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)

        current_board = copy.deepcopy(board)
        removed_count = 0
        last_guess_count = 0

        for r, c in cells:
            if removed_count >= max_clues_to_remove:
                break

            val = current_board[r][c]
            current_board[r][c] = 0

            solutions, guess_count, timeout_exceeded = solve_board(self.size, current_board, max_solutions=2, randomize=False, timeout=0.1)

            if not timeout_exceeded and len(solutions) == 1:
                removed_count += 1
                last_guess_count = guess_count
            else:
                current_board[r][c] = val

        difficulty = self._determine_difficulty(removed_count, last_guess_count)
        return current_board, removed_count, difficulty
