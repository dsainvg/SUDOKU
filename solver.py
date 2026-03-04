import random
import time

def get_box_index(r, c, box_r, box_c):
    return (r // box_r) * box_c + (c // box_c)

class SudokuSolver:
    def __init__(self, size, board, max_solutions=2, timeout=None):
        self.size = size
        self.board = [list(row) for row in board]
        self.max_solutions = max_solutions
        self.timeout = timeout
        self.start_time = None
        self.solutions = []
        self.guess_count = 0
        self.timeout_exceeded = False

        self.box_r, self.box_c = 2, 2

        self.row_mask = [0] * size
        self.col_mask = [0] * size
        self.box_mask = [0] * size
        self.empty_cells = []
        self.cells = []

        self.invalid_initial_state = False

        for r in range(size):
            for c in range(size):
                v = self.board[r][c]
                self.cells.append(v)
                if v != 0:
                    bit = 1 << v
                    b = get_box_index(r, c, self.box_r, self.box_c)
                    if (self.row_mask[r] & bit) or (self.col_mask[c] & bit) or (self.box_mask[b] & bit):
                        self.invalid_initial_state = True
                    self.row_mask[r] |= bit
                    self.col_mask[c] |= bit
                    self.box_mask[b] |= bit
                else:
                    self.empty_cells.append(r * size + c)

        self.full_mask = (1 << (size + 1)) - 2

    def solve(self, randomize=False):
        if self.invalid_initial_state:
            return [], 0, False

        self.guess_count = 0
        self.solutions = []
        self.start_time = time.time()
        self.timeout_exceeded = False
        self._backtrack(0, randomize)
        return self.solutions, self.guess_count, self.timeout_exceeded

    def _backtrack(self, depth, randomize):
        if self.timeout is not None and (time.time() - self.start_time > self.timeout):
            self.timeout_exceeded = True
            return

        if len(self.solutions) >= self.max_solutions:
            return

        if depth == len(self.empty_cells):
            sol_board = []
            for r in range(self.size):
                sol_board.append(list(self.cells[r * self.size : (r + 1) * self.size]))
            self.solutions.append(sol_board)
            return

        min_options = self.size + 1
        best_cell_idx = -1
        best_options = 0
        best_r, best_c, best_b = -1, -1, -1

        for i in range(depth, len(self.empty_cells)):
            idx = self.empty_cells[i]
            r = idx // self.size
            c = idx % self.size
            b = get_box_index(r, c, self.box_r, self.box_c)

            used = self.row_mask[r] | self.col_mask[c] | self.box_mask[b]
            options = self.full_mask & ~used

            count = options.bit_count()
            if count == 0:
                return # Dead end

            if count < min_options:
                min_options = count
                best_cell_idx = i
                best_options = options
                best_r, best_c, best_b = r, c, b
                if count == 1:
                    break

        self.empty_cells[depth], self.empty_cells[best_cell_idx] = self.empty_cells[best_cell_idx], self.empty_cells[depth]

        guesses_made = 1 if min_options > 1 else 0

        opts = []
        for v in range(1, self.size + 1):
            if best_options & (1 << v):
                opts.append(v)

        if randomize:
            random.shuffle(opts)

        for v in opts:
            bit = 1 << v
            self.row_mask[best_r] |= bit
            self.col_mask[best_c] |= bit
            self.box_mask[best_b] |= bit
            self.cells[best_r * self.size + best_c] = v
            self.guess_count += guesses_made

            self._backtrack(depth + 1, randomize)

            if self.timeout_exceeded or len(self.solutions) >= self.max_solutions:
                break

            self.row_mask[best_r] &= ~bit
            self.col_mask[best_c] &= ~bit
            self.box_mask[best_b] &= ~bit
            self.cells[best_r * self.size + best_c] = 0

        self.empty_cells[depth], self.empty_cells[best_cell_idx] = self.empty_cells[best_cell_idx], self.empty_cells[depth]

def solve_board(size, board, max_solutions=2, randomize=False, timeout=None):
    solver = SudokuSolver(size, board, max_solutions, timeout=timeout)
    return solver.solve(randomize=randomize)
