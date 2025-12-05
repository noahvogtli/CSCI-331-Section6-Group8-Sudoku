from data.puzzles import get_puzzle
import time

backtrack_steps = 0
forward_steps = 0


def print_grid(grid):
    for i in range(9):
        for j in range(9):
            val = grid[i][j]
            print(val if val != 0 else ".", end=" ")
            if (j + 1) % 3 == 0 and j < 8:
                print("|", end=" ")
        print()
        if (i + 1) % 3 == 0 and i < 8:
            print("-" * 21)


def can_place(grid, row, col, num):
    # Row
    for x in range(9):
        if grid[row][x] == num:
            return False

    # Column
    for x in range(9):
        if grid[x][col] == num:
            return False

    # Box
    br = 3 * (row // 3)
    bc = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[br + i][bc + j] == num:
                return False

    # Main diagonal
    if row == col:
        for x in range(9):
            if grid[x][x] == num:
                return False

    # Other diagonal
    if row + col == 8:
        for x in range(9):
            if grid[x][8 - x] == num:
                return False

    return True


def find_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def get_possible_values(grid, row, col):
    if grid[row][col] != 0:
        return set()

    possible = set(range(1, 10))

    # Row
    for x in range(9):
        if grid[row][x] in possible:
            possible.remove(grid[row][x])

    # Column
    for x in range(9):
        if grid[x][col] in possible:
            possible.remove(grid[x][col])

    # Box
    br = 3 * (row // 3)
    bc = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            val = grid[br + i][bc + j]
            if val in possible:
                possible.remove(val)

    # Main diagonal
    if row == col:
        for x in range(9):
            val = grid[x][x]
            if val in possible:
                possible.remove(val)

    # Other diagonal
    if row + col == 8:
        for x in range(9):
            val = grid[x][8 - x]
            if val in possible:
                possible.remove(val)

    return possible


def select_cell(grid):
    best_cell = None
    best_size = 10

    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                domain = get_possible_values(grid, i, j)
                domain_size = len(domain)

                if domain_size < best_size:
                    best_size = domain_size
                    best_cell = (i, j)

                if best_size == 1:
                    return best_cell

    return best_cell


def solve_forward(grid):
    global forward_steps

    cell = select_cell(grid)
    if cell is None:
        return True

    row, col = cell
    domain = get_possible_values(grid, row, col)

    for num in domain:
        forward_steps += 1
        grid[row][col] = num

        if forward_check(grid):
            if solve_forward(grid):
                return True

        grid[row][col] = 0

    return False

def forward_check(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                if len(get_possible_values(grid, i, j)) == 0:
                    return False
    return True


def solve_backtrack(grid):
    global backtrack_steps

    empty = find_empty(grid)
    if not empty:
        return True

    row, col = empty

    for num in range(1, 10):
        if can_place(grid, row, col, num):
            backtrack_steps += 1
            grid[row][col] = num

            if solve_backtrack(grid):
                return True

            grid[row][col] = 0

    return False


if __name__ == "__main__":
    sudoku1 = get_puzzle()
    sudoku2 = [row.copy() for row in sudoku1]

    print("Original Sudoku:")
    print_grid(sudoku1)

    forward_steps = 0
    start = time.perf_counter()
    fsolved = solve_forward(sudoku1)
    end = time.perf_counter()

    if fsolved:
        print("\nSolved with Forward Checking:")
        print_grid(sudoku1)
        print(f"Forward Checking Time: {end - start:.6f} seconds")
        print(f"Forward Checking Backtracking Steps: {forward_steps}")

    backtrack_steps = 0
    start = time.perf_counter()
    bsolved = solve_backtrack(sudoku2)
    end = time.perf_counter()

    if bsolved:
        print("\nSolved with Backtracking:")
        print_grid(sudoku2)
        print(f"Backtracking Time: {end - start:.6f} seconds")
        print(f"Backtracking Steps: {backtrack_steps}")

    diff = forward_steps - backtrack_steps
    if diff > 0:
        print(f"Forward Checking performed {diff} more steps than Backtracking.")
    elif diff < 0:
        print(f"Backtracking performed {-diff} more steps than Forward Checking.")
    else:
        print("Both methods performed the same number of steps.")
