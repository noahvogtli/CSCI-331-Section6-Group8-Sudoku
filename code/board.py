from data.puzzles import get_puzzle
import time

backtrack_count = 0
forward_check_count = 0
backtrack_steps = 0
forward_steps = 0

def print_grid(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                print(".", end=" ")
            else:
                print(grid[i][j], end=" ")
            if (j + 1) % 3 == 0 and j < 8:
                print("|", end=" ")
        print()
        if (i + 1) % 3 == 0 and i < 8:
            print("-" * 21)

def can_place(grid, row, col, num):

    for x in range(9):
        if grid[row][x] == num:
            return False

    for x in range(9):
        if grid[x][col] == num:
            return False

    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    
    if row == col:
        for x in range(9):
            if grid[x][x] == num:
                return False
    
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
    
    for x in range(9):
        if grid[row][x] != 0:
            possible.discard(grid[row][x])
    
    for x in range(9):
        if grid[x][col] != 0:
            possible.discard(grid[x][col])
    
  
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] != 0:
                possible.discard(grid[start_row + i][start_col + j])
    
    if row == col:
        for x in range(9):
            if grid[x][x] != 0:
                possible.discard(grid[x][x])
    

    if row + col == 8:
        for x in range(9):
            if grid[x][8 - x] != 0:
                possible.discard(grid[x][8 - x])
    
    return possible

def forward_check(grid):
    global forward_check_count
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                possible = get_possible_values(grid, i, j)
                forward_check_count += 1
                if not possible:
                    return False
    return True

def _solve_forward(grid):
    global forward_steps
    empty = find_empty(grid)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if can_place(grid, row, col, num):
            forward_steps += 1         
            grid[row][col] = num

            if forward_check(grid):
                if _solve_forward(grid):
                    return True

            grid[row][col] = 0
    return False

def solve_forward(grid):
    start = time.perf_counter()
    result = _solve_forward(grid)
    end = time.perf_counter()
    if result:
        print(f"Forward Checking solved in {end - start:.6f} seconds")
    return result


def _solve_backtrack(grid):
    global backtrack_count, backtrack_steps
    empty = find_empty(grid)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if can_place(grid, row, col, num):
            backtrack_steps += 1      
            backtrack_count += 1      
            grid[row][col] = num
            if _solve_backtrack(grid):
                return True
            grid[row][col] = 0
    return False

def solve_backtrack(grid):
    start = time.perf_counter()
    result = _solve_backtrack(grid)
    end = time.perf_counter()
    if result:
        print(f"Backtracking solved in {end - start:.6f} seconds")
    return result

if __name__ == "__main__":

    sudoku1 = get_puzzle()
    sudoku2 = [row.copy() for row in sudoku1]
    print("Original Sudoku:")
    print_grid(sudoku1)

    # reset counters for forward run
    forward_check_count = 0
    forward_steps = 0
    if solve_forward(sudoku1):
        print("\nSolved Sudoku: (Forward Checking)")
        print_grid(sudoku1)
        print(f"Forward checks performed: {forward_check_count}")
        print(f"Forward trial assignments performed: {forward_steps}")
    else:
        print("No solution")

    # reset counters for backtrack run
    backtrack_count = 0
    backtrack_steps = 0
    if solve_backtrack(sudoku2):
        print("\nSolved Sudoku (Backtracking):")
        print_grid(sudoku2)
        print(f"Backtrack steps performed: {backtrack_count}")
    else:
        print("No solution")