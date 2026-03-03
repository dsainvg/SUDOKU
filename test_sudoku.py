import pytest
from hypothesis import given, strategies as st
from solver import solve_board
from validator import is_valid_sudoku
from dataset_loader import DatasetLoader
from generator import SudokuGenerator
import numpy as np

@given(st.lists(st.integers(min_value=0, max_value=4), min_size=16, max_size=16))
def test_random_4x4_boards_rejection(board_flat):
    board = [board_flat[i*4:(i+1)*4] for i in range(4)]
    if not is_valid_sudoku(board, 4):
        sols, _, _ = solve_board(4, board, max_solutions=1)
        assert len(sols) == 0

def test_uniqueness_check():
    loader = DatasetLoader(4)
    puzzle, solution = loader.get_random_pair()

    sols, _, _ = solve_board(4, puzzle.tolist(), max_solutions=2)
    assert len(sols) == 1
    assert sols[0] == solution.tolist()

def test_consistency_and_determinism():
    loader = DatasetLoader(9)
    puzzle, _ = loader.get_random_pair()

    sols1, guesses1, _ = solve_board(9, puzzle.tolist(), max_solutions=1, randomize=False)
    sols2, guesses2, _ = solve_board(9, puzzle.tolist(), max_solutions=1, randomize=False)

    assert sols1 == sols2
    assert guesses1 == guesses2

def test_integration_dataset_loader():
    for size in [4, 9, 16]:
        loader = DatasetLoader(size)
        assert len(loader.puzzles) > 0
        assert len(loader.solutions) > 0

        puzzle = loader.puzzles[0].tolist()
        solution = loader.solutions[0].tolist()

        assert is_valid_sudoku(solution, size)
        assert is_valid_sudoku(puzzle, size)

def test_difficulty_calibration():
    # Ensures guess count and removed clues are properly mapped
    gen = SudokuGenerator(9)

    assert gen._determine_difficulty(55, 60) == 'Expert'
    assert gen._determine_difficulty(48, 15) == 'Hard'
    assert gen._determine_difficulty(40, 5) == 'Medium'
