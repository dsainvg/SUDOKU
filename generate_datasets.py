import argparse
import numpy as np
import os
import time
from generator import SudokuGenerator
from validator import is_valid_sudoku

def generate_dataset(size, target_count):
    # Determine counts based on rules: 500 for 4x4, 5000 for others
    total_needed = 500 if size == 4 else 5000
    if target_count is not None:
        total_needed = target_count

    generator = SudokuGenerator(size)

    # We will generate puzzles and bin them by their dynamically computed difficulty
    puzzles = []
    solutions = []
    meta = []

    print(f"Generating {total_needed} puzzles for size {size}x{size}")

    generated = 0
    while generated < total_needed:
        t0 = time.time()
        full_board = generator.generate_full_board()

        # Max removals target to push for harder puzzles
        if size == 4: max_removals = 12
        elif size == 9: max_removals = 60
        else: max_removals = 160

        puzzle, removed, difficulty = generator.remove_clues_target(full_board, max_removals)

        # Explicit validation before appending, per requirements
        if is_valid_sudoku(puzzle, size):
            puzzles.append(puzzle)
            solutions.append(full_board)
            meta.append(difficulty)
            generated += 1

            if generated % 10 == 0:
                print(f"Size {size}x{size} | {generated}/{total_needed} | Diff: {difficulty} | Last gen: {time.time()-t0:.2f}s")
        else:
            print("Warning: Invalid puzzle generated. Skipping.")

    os.makedirs('outputs', exist_ok=True)
    filename = f'outputs/dataset_{size}x{size}.npz'
    np.savez_compressed(
        filename,
        puzzles=np.array(puzzles, dtype=np.uint8),
        solutions=np.array(solutions, dtype=np.uint8),
        difficulty_metadata=np.array(meta),
        board_size=size
    )
    print(f"Saved {filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, required=True, choices=[4, 9, 16])
    parser.add_argument('--count', type=int, default=None)
    args = parser.parse_args()

    generate_dataset(args.size, args.count)
