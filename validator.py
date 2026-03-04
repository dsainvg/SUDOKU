def is_valid_sudoku(board, size=4):
    if len(board) != size or any(len(row) != size for row in board):
        return False

    box_r, box_c = 2, 2

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
