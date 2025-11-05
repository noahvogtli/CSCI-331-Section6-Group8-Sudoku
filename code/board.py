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
    return True

def find_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def solve(grid):
    empty = find_empty(grid)
    if not empty:
        return True  
    row, col = empty

    for num in range(1, 10):
        if can_place(grid, row, col, num):
            grid[row][col] = num
            if solve(grid):
                return True
            grid[row][col] = 0
    return False

if __name__ == "__main__":
    sudoku = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]

    print("Original Sudoku:")
    print_grid(sudoku)

    if solve(sudoku):
        print("\nSolved Sudoku:")
        print_grid(sudoku)
    else:
        print("No solution")
