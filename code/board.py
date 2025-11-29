from data.puzzles import get_puzzle


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
    
    # Remove values already in the row
    for x in range(9):
        if grid[row][x] != 0:
            possible.discard(grid[row][x])
    
    # Remove values already in the column
    for x in range(9):
        if grid[x][col] != 0:
            possible.discard(grid[x][col])
    
    # Remove values already in the 3x3 box
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] != 0:
                possible.discard(grid[start_row + i][start_col + j])
    
    # Remove values already on the main diagonal
    if row == col:
        for x in range(9):
            if grid[x][x] != 0:
                possible.discard(grid[x][x])
    
    # Remove values already on the anti-diagonal
    if row + col == 8:
        for x in range(9):
            if grid[x][8 - x] != 0:
                possible.discard(grid[x][8 - x])
    
    return possible

def forward_check(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                possible = get_possible_values(grid, i, j)
                if not possible:
                    return False
    return True

def solve_forward(grid):
    empty = find_empty(grid)
    if not empty:
        return True  
    row, col = empty

    for num in range(1, 10):
        if can_place(grid, row, col, num):
            grid[row][col] = num
            
            if forward_check(grid):
                if solve_forward(grid):
                    return True
            
            grid[row][col] = 0
    return False

def solve_backtrack(grid):
    empty = find_empty(grid)
    if not empty:
        return True  
    row, col = empty

    for num in range(1, 10):
        if can_place(grid, row, col, num):
            grid[row][col] = num
            if solve_backtrack(grid):
                return True
            grid[row][col] = 0
    return False

if __name__ == "__main__":

    sudoku1 = get_puzzle()
    sudoku2 = sudoku1.copy()
    print("Original Sudoku:")
    print_grid(sudoku1)

    if solve_forward(sudoku1):
        print("\nSolved Sudoku: (Forward Checking)")
        print_grid(sudoku1)
    else:
        print("No solution")

    if solve_backtrack(sudoku2):
        print("\nSolved Sudoku (Backtracking):")
        print_grid(sudoku2)
    else:
        print("No solution")