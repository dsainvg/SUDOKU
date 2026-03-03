def get_box_dimensions(size):
    if size == 4:
        return 2, 2
    elif size == 9:
        return 3, 3
    elif size == 16:
        return 4, 4
    else:
        raise ValueError("Unsupported size")

def is_valid_sudoku(board, size=None):
    if size is None:
        size = len(board)
    if len(board) != size or any(len(row) != size for row in board):
        return False

    box_r, box_c = get_box_dimensions(size)

    # Check rows
    for r in range(size):
        seen = set()
        for c in range(size):
            val = board[r][c]
            if val != 0:
                if val < 1 or val > size or val in seen:
                    return False
                seen.add(val)

    # Check cols
    for c in range(size):
        seen = set()
        for r in range(size):
            val = board[r][c]
            if val != 0:
                if val < 1 or val > size or val in seen:
                    return False
                seen.add(val)

    # Check boxes
    for br in range(size // box_r):
        for bc in range(size // box_c):
            seen = set()
            for i in range(box_r):
                for j in range(box_c):
                    val = board[br * box_r + i][bc * box_c + j]
                    if val != 0:
                        if val < 1 or val > size or val in seen:
                            return False
                        seen.add(val)

    return True

def is_solved(board, size=None):
    if size is None:
        size = len(board)
    if not is_valid_sudoku(board, size):
        return False
    for r in range(size):
        for c in range(size):
            if board[r][c] == 0:
                return False
    return True
