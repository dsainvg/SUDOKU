# Sudoku 4×4: Rules, Generation, and Solutions

**Overview:** Sudoku is a logic puzzle where numbers must be placed so that each row, column, and subgrid contains all allowed symbols exactly once.  A **4×4 Sudoku** is a smaller variant using a 4×4 grid with digits 1–4.  The 4×4 grid is subdivided into four 2×2 blocks【11†L96-L99】.  The goal is to fill the grid so that **each row, each column, and each 2×2 block contains the digits 1–4 exactly once**【2†L114-L118】【8†L53-L58】.  In other words, no number may repeat in any row, column or block【2†L114-L118】.  A well-posed Sudoku puzzle has exactly one valid solution【2†L120-L124】.  

【12†embed_image】 *Figure: Completed 4×4 Sudoku grid example. Each row, column, and 2×2 block contains the digits 1–4 exactly once【2†L114-L118】【8†L53-L58】. This illustrates the core Sudoku rule that no number repeats in any row, column or block.*  

## Generating 4×4 Sudoku Programmatically

A common method to generate a 4×4 Sudoku puzzle is to first create a full valid solution grid and then remove entries while maintaining a unique solution.  In fact, there are only **288 valid completed 4×4 Sudoku grids**, a number that can be found by exhaustive backtracking【13†L245-L247】.  One typical algorithm proceeds as follows【15†L197-L204】【15†L205-L209】:

- **Step 1 – Generate full solution:** Start with an empty 4×4 grid and fill it completely using a backtracking solver.  Randomize the order of candidate digits to ensure a different solution each run.  This backtracking ensures every placement follows the Sudoku rules【15†L197-L204】.  
- **Step 2 – Remove clues iteratively:** Once a full grid is made, remove one cell’s value at a time (creating a blank).  After each removal, use a Sudoku solver to check the puzzle’s solvability.  If the puzzle still has exactly one solution, keep the removal; if multiple solutions arise, put the digit back【15†L205-L209】.  
- **Step 3 – Repeat for difficulty:** Continue removing values (and checking) until the puzzle has the desired number of clues.  More removals (fewer clues) generally mean a harder puzzle.  For example, repeating removals and uniqueness checks yields a more difficult puzzle【15†L209-L212】.  By controlling how many clues remain, one can tune the difficulty of the generated puzzle.

This method is essentially a randomized backtracking fill followed by controlled clue deletion【15†L197-L204】【15†L205-L209】.  Below is a conceptual pseudocode outline for generation:

```plaintext
# Pseudocode for 4×4 Sudoku generator
GenerateFullGrid():
    grid = empty 4×4 array
    solve_with_backtracking(grid, randomize=True)  # fills grid fully

RemoveClues(grid):
    For each cell in random order:
        Save the value and set cell to blank
        If solver(grid) finds more than one solution:
            restore the saved value
    Return puzzle grid

# The result is a 4×4 Sudoku puzzle with a unique solution.
```

*References:* This approach is described in algorithmic form (for 9×9) by using backtracking to fill a grid and then removing clues while checking uniqueness【15†L197-L204】【15†L205-L209】.  

## Solving a 4×4 Sudoku

To solve a 4×4 Sudoku (or to verify a generated puzzle has a unique solution), one typically uses a simple **backtracking algorithm**【8†L84-L89】.  The solver searches for empty cells and tries digits 1–4 recursively:

1. **Find an empty cell.** If none remain, the puzzle is solved.  
2. **Try each digit 1–4.** For a candidate digit, check that it does not already appear in the same row, column, or 2×2 block (the Sudoku constraints).  
3. **Recurse:** If the placement is valid, place the digit and recursively attempt to solve the rest of the grid.  
4. **Backtrack on conflict:** If the recursion fails (no valid completion), reset the cell to empty and try the next digit.  
5. **Repeat:** Continue until the grid is filled or all possibilities are exhausted.  

This procedure is described in detail in backtracking Sudoku solvers【8†L84-L89】.  A sample Python-like implementation might look like this:

```python
def solve_sudoku(grid):
    # Find first empty cell (denoted by 0)
    for r in range(4):
        for c in range(4):
            if grid[r][c] == 0:
                # Try digits 1 through 4
                for num in range(1, 5):
                    if is_valid(grid, r, c, num):
                        grid[r][c] = num
                        if solve_sudoku(grid):
                            return True
                        # Backtrack
                        grid[r][c] = 0
                # If no valid number found, trigger backtracking
                return False
    # No empty cells left: solved
    return True

def is_valid(grid, r, c, num):
    # Check row and column
    if num in grid[r]: return False
    if any(grid[i][c] == num for i in range(4)): return False
    # Check 2x2 block
    br, bc = (r//2)*2, (c//2)*2
    for i in range(br, br+2):
        for j in range(bc, bc+2):
            if grid[i][j] == num:
                return False
    return True
```

This simple backtracking solver will fill in the grid if a solution exists【8†L84-L89】. It enforces the rule that no digit repeats in any row, column, or block.

## Example 4×4 Sudoku Puzzles

Below are example puzzles at increasing difficulty, each with a complete solution.  (Blank cells are shown as underscores.)  The *difficulty* is roughly controlled by the number of given clues and how many must be deduced:

- **Easy (8 clues):**  
  ```
  _ 2 _ 4
  3 4 1 2
  2 _ 4 1
  4 1 2 _
  ```  
  **Solution:**  
  ```
  1 2 3 4
  3 4 1 2
  2 3 4 1
  4 1 2 3
  ```  
  *Note:* This easy puzzle has one or two blanks in each row.  For example, Row 1 has digits [2, 4] present, so the blanks must be 1 and 3.  Simple elimination in each row or column quickly solves it.  

- **Medium (7 clues):**  
  ```
  _ 2 _ 4
  3 _ 1 2
  2 _ 4 1
  4 1 2 _
  ```  
  **Solution:**  
  ```
  1 2 3 4
  3 4 1 2
  2 3 4 1
  4 1 2 3
  ```  
  *Note:* With 7 clues, some rows have two blanks.  The solver must look at both the row and column (or block) constraints together. For example, if Row 2 is missing  and , one can use the fact that Column 2 already contains 2 and 1 to deduce the missing value.

- **Hard (6 clues):**  
  ```
  _ 2 _ 4
  _ _ 1 2
  2 _ _ 1
  4 1 2 _
  ```  
  **Solution:**  
  ```
  1 2 3 4
  3 4 1 2
  2 3 4 1
  4 1 2 3
  ```  
  *Note:* This puzzle has only 6 clues.  Solving it may require noting how a missing cell’s possible digits are constrained by two different units (e.g. by its row and by its column or block simultaneously).  It still has a unique solution if solved correctly.

Each of these puzzles follows the 4×4 Sudoku rules and has exactly one solution.  In practice, solving can be done by scanning for rows/columns/blocks with only one missing number or by recursive backtracking as shown above.  Fewer clues generally increases difficulty because more inference (or deeper recursion) is needed.

**Summary:** A 4×4 Sudoku uses the same rules as standard Sudoku but on a smaller 4×4 grid with 2×2 blocks【2†L114-L118】【8†L53-L58】.  To generate puzzles, one can fill a grid by backtracking and then remove clues while ensuring a unique solution【15†L197-L204】【15†L205-L209】.  To solve them, a backtracking solver (try digits 1–4 in empty cells recursively) is typically used【8†L84-L89】. The examples above illustrate valid puzzles and solutions at different difficulty levels, all obeying the rule that each row, column, and block contains 1–4 exactly once.  

**Sources:** Authoritative Sudoku guides and algorithmic tutorials were used for definitions, rules, and generation/solving methods【2†L114-L118】【8†L53-L58】【15†L197-L204】【15†L205-L209】. The count of 288 total solutions comes from an exhaustive enumeration【13†L245-L247】.