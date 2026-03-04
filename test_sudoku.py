import pytest
from solver import solve_board
from validator import is_valid_sudoku
from dataset_loader import DatasetLoader
import numpy as np

def test_uniqueness_check():
    loader = DatasetLoader(4)
    puzzle, solution = loader.get_random_pair()

    sols, _, _ = solve_board(4, puzzle.tolist(), max_solutions=2)
    assert len(sols) == 1
    assert sols[0] == solution.tolist()

def test_integration_dataset_loader():
    loader = DatasetLoader(4)
    assert len(loader.puzzles) == 1280
    assert len(loader.solutions) == 1280

    puzzle = loader.puzzles[0].tolist()
    solution = loader.solutions[0].tolist()

    assert is_valid_sudoku(solution, 4)
    assert is_valid_sudoku(puzzle, 4)
