import random


def generate_sudoku():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    fill_grid(grid)
    return grid


def fill_grid(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(grid, i, j, num):
                        grid[i][j] = num
                        if fill_grid(grid):
                            return True
                        grid[i][j] = 0
                return False
    return True


def is_valid(grid, row, col, num):
    return (is_valid_row(grid, row, num) and
            is_valid_col(grid, col, num) and
            is_valid_box(grid, row - row % 3, col - col % 3, num))


def is_valid_row(grid, row, num):
    return num not in grid[row]


def is_valid_col(grid, col, num):
    return num not in [grid[i][col] for i in range(9)]


def is_valid_box(grid, start_row, start_col, num):
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True


def print_sudoku(grid):
    horizontal_line = "+-------+-------+-------+"
    print(horizontal_line)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print(horizontal_line)
        row_str = "| "
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += str(grid[i][j]) + " "
        row_str += "|"
        print(row_str)
    print(horizontal_line)


if __name__ == "__main__":
    sudoku = generate_sudoku()
    print("Generated Sudoku:")
    print_sudoku(sudoku)
