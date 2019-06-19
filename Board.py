from tkinter import *
from tkinter import ttk
import numpy as np


class Board:
    def __init__(self, master, n):
        self.master = master
        self.n = n
        self.master.geometry('600x600+10+10')
        self.master.update_idletasks()
        self.max_size = min(self.master.winfo_width(), self.master.winfo_height())
        self.master.update_idletasks()
        self.canvas = None
        self.cells = self.create_board()
        self.cell_size = self.max_size // self.n
        self.create_canvas()

    def create_canvas(self):
        self.canvas = Canvas(self.master, width=self.max_size, height=self.max_size)
        self.canvas.pack()
        self.canvas.configure(background='black')
        for i in range(self.n):
            for j in range(self.n):
                self.canvas.create_rectangle(i * self.cell_size, j * self.cell_size,
                                             (i + 1) * self.cell_size, (j + 1) * self.cell_size,
                                             fill=self.cells[i][j])

    def create_board(self):
        cells = []
        for i in range(self.n):
            cells.append([])
            for j in range(self.n):
                if (i + j) % 2 == 0:
                    cells[i].append('black')
                else:
                    cells[i].append('white')
        return cells


def main():
    root = Tk()
    b = Board(root, 8)
    root.mainloop()


if __name__ == '__main__':
    main()
