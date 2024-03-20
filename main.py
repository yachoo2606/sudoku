import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import random
from sudokuConsoleVersion import generate_sudoku


class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title, message, image_path):
        super().__init__(parent)
        self.title(title)

        self.image_path = image_path
        self.frames = self.load_frames()

        self.image_label = ttk.Label(self)
        self.image_label.pack(pady=10)

        self.label = ttk.Label(self, text=message)
        self.label.pack(pady=10)

        self.button = ttk.Button(self, text="OK", command=self.destroy)
        self.button.pack(pady=10)

        self.animate()

    def load_frames(self):
        gif = Image.open(self.image_path)
        frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]
        self.geometry(f"{gif.width}x{gif.height + 100}")  # Adjust window size to fit the image
        return frames

    def animate(self, frame_index=0):
        if frame_index < len(self.frames):
            self.image_label.config(image=self.frames[frame_index])
            self.after(100, self.animate, frame_index + 1)
        else:
            self.after(100, self.animate, 0)


def return_path(name):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, "assets", name)
    else:
        return "assets/" + name


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
                if random.random() < 0.2:
                    initial_value = self.sudoku[i][j]
                    cell = tk.Label(self.master, text=str(initial_value), font=('Arial', 18, 'bold'),
                                    relief='ridge')
                else:
                    cell = tk.Entry(self.master, font=('Arial', 18, 'bold'), justify='center')

                padx = 10 if j == 2 or j == 5 else 0
                pady = 10 if i == 2 or i == 5 else 0
                cell.grid(row=i, column=j, sticky="nsew", padx=(0, padx), pady=(0, pady))
                row.append(cell)
            self.cells.append(row)
        for i in range(9):
            self.master.grid_rowconfigure(i, weight=1)

        for j in range(9):
            self.master.grid_columnconfigure(j, weight=1)

        solve_button = tk.Button(self.master, text="Solve", command=self.solve)
        solve_button.grid(row=9, columnspan=4, sticky="ew")
        clear_button = tk.Button(self.master, text="Clear", command=self.clear)
        clear_button.grid(row=9, column=5, columnspan=4, sticky="ew")

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
        print(os.getcwd())
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
            win_dialog = CustomDialog(self.master, "Congratulations!", "YOU WIN!", return_path("clapping_hands.gif"))
            self.master.wait_window(win_dialog)
            self.master.quit()
        else:
            error_dialog = CustomDialog(self.master, "Error", "ERRORS!!!!", return_path("sad.gif"))
            self.master.wait_window(error_dialog)


def main():
    root = tk.Tk()
    sudoku = generate_sudoku()
    SudokuGUI(root, sudoku)
    root.mainloop()


if __name__ == "__main__":
    main()
