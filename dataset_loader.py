import numpy as np
import random
import os

class DatasetLoader:
    def __init__(self, size=4, filepath=None):
        self.size = size
        if filepath is None:
            filepath = f"outputs/dataset_{size}x{size}.npz"

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset file {filepath} not found.")

        data = np.load(filepath)
        self.puzzles = data['puzzles']
        self.solutions = data['solutions']
        self.metadata = data['difficulty_metadata']

    def get_random_pair(self, difficulty=None):
        if difficulty is not None:
            indices = np.where(self.metadata == difficulty)[0]
            if len(indices) == 0:
                raise ValueError(f"No puzzles found for difficulty {difficulty}")
            idx = random.choice(indices)
        else:
            idx = random.randint(0, len(self.puzzles) - 1)

        return self.puzzles[idx], self.solutions[idx]
