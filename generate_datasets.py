import argparse
import numpy as np
import os
import time
from generator import SudokuGenerator
from validator import is_valid_sudoku

def generate_dataset(size, target_count):
    total_needed = target_count

    generator = SudokuGenerator(size)

    puzzles = []
    solutions = []
    meta = []

    print(f"Generating {total_needed} puzzles for size {size}x{size}", flush=True)

    generated = 0
    t_start = time.time()

    while generated < total_needed:
        t0 = time.time()

        # We must generate a FULLY UNIQUE solution board for every single puzzle
        # as requested, rather than reusing them to prioritize correctness and uniqueness over speed.
        try:
            full_board = generator.generate_full_board()
        except Exception as e:
            print("Failed base board", flush=True)
            continue

        if size == 4: max_removals = 12
        elif size == 9: max_removals = 50
        else: max_removals = 120

        puzzle, removed, difficulty = generator.remove_clues_target(full_board, max_removals)

        if is_valid_sudoku(puzzle, size):
            puzzles.append(puzzle)
            solutions.append(full_board)
            meta.append(difficulty)
            generated += 1

            if generated % 100 == 0:
                print(f"Size {size}x{size} | {generated}/{total_needed} | Last gen: {time.time()-t0:.2f}s | Total elapsed: {time.time()-t_start:.2f}s", flush=True)

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
