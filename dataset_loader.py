import numpy as np
import random
import os

class DatasetLoader:
    def __init__(self, size, filepath=None):
        self.size = size
        if filepath is None:
            filepath = f"outputs/dataset_{size}x{size}.npz"

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset file {filepath} not found.")

        data = np.load(filepath)
        self.puzzles = data['puzzles']
        self.solutions = data['solutions']
        self.metadata = data['difficulty_metadata']

    def get_by_difficulty(self, difficulty):
        indices = np.where(self.metadata == difficulty)[0]
        if len(indices) == 0:
            return [], []
        return self.puzzles[indices], self.solutions[indices]

    def get_random_pair(self, difficulty=None):
        if difficulty is not None:
            indices = np.where(self.metadata == difficulty)[0]
            if len(indices) == 0:
                raise ValueError(f"No puzzles found for difficulty {difficulty}")
            idx = random.choice(indices)
        else:
            idx = random.randint(0, len(self.puzzles) - 1)

        return self.puzzles[idx], self.solutions[idx]

    @staticmethod
    def print_board(board, size):
        if size == 4:
            box_r, box_c = 2, 2
        elif size == 9:
            box_r, box_c = 3, 3
        elif size == 16:
            box_r, box_c = 4, 4
        else:
            raise ValueError("Unsupported size")

        def fmt(v):
            if v == 0:
                return "."
            if v > 9:
                return chr(ord('A') + v - 10)
            return str(v)

        for r in range(size):
            if r > 0 and r % box_r == 0:
                print("-" * (size * 2 + (size // box_c) - 1))
            row_str = []
            for c in range(size):
                if c > 0 and c % box_c == 0:
                    row_str.append("|")
                row_str.append(fmt(board[r][c]))
            print(" ".join(row_str))

if __name__ == "__main__":
    # Test just loading the module
    print("DatasetLoader loaded.")
