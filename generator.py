import random
import copy
from solver import solve_board

class SudokuGenerator:
    def __init__(self, size):
        self.size = size

    def generate_full_board(self):
        empty_board = [[0]*self.size for _ in range(self.size)]
        solutions, _, _ = solve_board(self.size, empty_board, max_solutions=1, randomize=True)
        if not solutions:
            raise RuntimeError("Failed to generate full board")
        return solutions[0]

    def _determine_difficulty(self, removed_count, guess_count):
        # Determine difficulty based on combination of removed clues and backtracking guess depth
        if self.size == 4:
            if guess_count > 1 or removed_count >= 10:
                return 'Hard'
            elif guess_count == 1 or removed_count >= 9:
                return 'Medium'
            return 'Easy'

        elif self.size == 9:
            # typical 9x9 targets: Easy (40 clues ~ 41 removed), Medium (33 clues ~ 48 removed), Hard (28 clues ~ 53 removed), Expert (<28 clues ~ >53 removed)
            if guess_count >= 50 or removed_count >= 55:
                return 'Expert'
            elif guess_count >= 10 or removed_count >= 48:
                return 'Hard'
            elif guess_count >= 2 or removed_count >= 40:
                return 'Medium'
            return 'Easy'

        elif self.size == 16:
            if guess_count >= 200 or removed_count >= 150:
                return 'Expert'
            elif guess_count >= 50 or removed_count >= 135:
                return 'Hard'
            elif guess_count >= 10 or removed_count >= 120:
                return 'Medium'
            return 'Easy'
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

            timeout = 0.05 if self.size == 16 else 0.5
            solutions, guess_count, timeout_exceeded = solve_board(self.size, current_board, max_solutions=2, randomize=False, timeout=timeout)

            if not timeout_exceeded and len(solutions) == 1:
                removed_count += 1
                last_guess_count = guess_count
            else:
                current_board[r][c] = val

        difficulty = self._determine_difficulty(removed_count, last_guess_count)
        return current_board, removed_count, difficulty
