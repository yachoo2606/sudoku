import tkinter as tk
from tkinter import messagebox
import random
from sudokuConsoleVersion import generate_sudoku


class SudokuGUI:
    def __init__(self, master, sudoku):
        self.master = master
        self.sudoku = sudoku
        self.initUI()

    def initUI(self):
        self.master.title("Sudoku")
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                if random.random() < 0.2:  # Adjust the probability here to control the number of initial values
                    initial_value = self.sudoku[i][j]
                    cell = tk.Label(self.master, text=str(initial_value), font=('Arial', 18, 'bold'),
                                    relief='ridge')
                else:
                    cell = tk.Entry(self.master, font=('Arial', 18, 'bold'), justify='center')

                # Determine if the cell is on the right or bottom edge of a 3x3 block
                padx = 10 if j == 2 or j == 5 else 0  # Add extra padding after the 3rd and 6th column
                pady = 10 if i == 2 or i == 5 else 0  # Add extra padding after the 3rd and 6th row
                cell.grid(row=i, column=j, sticky="nsew", padx=(0, padx), pady=(0, pady))
                row.append(cell)
            self.cells.append(row)
        for i in range(9):
            self.master.grid_rowconfigure(i, weight=1)

        for j in range(9):
            self.master.grid_columnconfigure(j, weight=1)

        solve_button = tk.Button(self.master, text="Solve", command=self.solve)
        solve_button.grid(row=9, columnspan=4, sticky="ew")
        solve_button = tk.Button(self.master, text="Clear", command=self.clear)
        solve_button.grid(row=9, column=5, columnspan=4, sticky="ew")

        self.master.bind('<Configure>', self.on_resize)

    def clear(self):
        for i in range(9):
            for j in range(9):
                if isinstance(self.cells[i][j], tk.Entry):
                    self.cells[i][j].delete(0, tk.END)

    def on_resize(self, event):
        font_size = max(8, min(event.width, event.height) // 25)
        for row in self.cells:
            for cell in row:
                if isinstance(cell, tk.Label) or isinstance(cell, tk.Entry):
                    cell.config(font=('Arial', font_size, 'bold'))

    def solve(self):
        # Get the user input from the GUI
        user_input = []
        for i in range(9):
            row_input = []
            for j in range(9):
                if isinstance(self.cells[i][j], tk.Entry):
                    value = self.cells[i][j].get()
                elif isinstance(self.cells[i][j], tk.Label):
                    value = self.cells[i][j].cget("text")
                row_input.append(value)
            user_input.append(row_input)

        # Check if entries correspond to the values in the Sudoku matrix
        errors = False
        for i in range(9):
            for j in range(9):
                if user_input[i][j] != str(self.sudoku[i][j]):
                    errors = True
                    break

        # Display appropriate messagebox
        if not errors:
            messagebox.showinfo("Congratulations!", "YOU WIN!")
            self.master.quit()
        else:
            messagebox.showerror("Error", "ERRORS!!!!")

    def solve_sudoku(self, grid):
        empty_cell = self.find_empty_cell(grid)
        if not empty_cell:
            return True

        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid(grid, row, col, num):
                grid[row][col] = num
                if self.solve_sudoku(grid):
                    return True
                grid[row][col] = 0
        return False

    def find_empty_cell(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, grid, row, col, num):
        return (self.is_valid_row(grid, row, num) and
                self.is_valid_col(grid, col, num) and
                self.is_valid_box(grid, row - row % 3, col - col % 3, num))

    def is_valid_row(self, grid, row, num):
        return num not in grid[row]

    def is_valid_col(self, grid, col, num):
        return num not in [grid[i][col] for i in range(9)]

    def is_valid_box(self, grid, start_row, start_col, num):
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        return True


def main():
    root = tk.Tk()
    sudoku = generate_sudoku()  # generate initial Sudoku puzzle
    SudokuGUI(root, sudoku)
    root.mainloop()


if __name__ == "__main__":
    main()
