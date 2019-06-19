from tkinter import *
from tkinter import ttk
import numpy as np
from Piece import *


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
        for i in range(self.n):
            for j in range(self.n):
                if (i + j) % 2 == 1:
                    self.canvas.create_rectangle(i * self.cell_size, j * self.cell_size,
                                                 (i + 1) * self.cell_size, (j + 1) * self.cell_size,
                                                 fill='black')

    def create_board(self):
        cells = []
        for i in range(self.n):
            cells.append([])
            for j in range(self.n):
                if (i + j) % 2 == 1:
                    cells[i].append('black')
                else:
                    cells[i].append('white')
        return cells

    def place_piece(self, piece, x, y):
        board_x = (x - 1) * self.cell_size + self.cell_size // 2
        board_y = (y - 1) * self.cell_size + self.cell_size // 2
        if (x + y) % 2 == 1:
            pad = 27
            self.canvas.create_rectangle(board_x - pad, board_y - pad, board_x + pad, board_y + pad, fill='white')
        self.canvas.create_text(board_x, board_y, text=piece.char, font='Arial 40', tag='piece')

    def start_setup(self):
        pieces = []
        # pawns
        for i in range(self.n):
            pieces.append(Piece('white', 'pawn', i + 1, 7))
            pieces.append(Piece('black', 'pawn', i + 1, 2))

        # rooks
        pieces.append(Piece('white', 'rook', 1, 8))
        pieces.append(Piece('white', 'rook', 8, 8))
        pieces.append(Piece('black', 'rook', 1, 1))
        pieces.append(Piece('black', 'rook', 8, 1))

        # knights
        pieces.append(Piece('white', 'knight', 2, 8))
        pieces.append(Piece('white', 'knight', 7, 8))
        pieces.append(Piece('black', 'knight', 2, 1))
        pieces.append(Piece('black', 'knight', 7, 1))

        # bishops
        pieces.append(Piece('white', 'bishop', 3, 8))
        pieces.append(Piece('white', 'bishop', 6, 8))
        pieces.append(Piece('black', 'bishop', 3, 1))
        pieces.append(Piece('black', 'bishop', 6, 1))

        # queens
        pieces.append(Piece('white', 'queen', 4, 8))
        pieces.append(Piece('black', 'queen', 4, 1))

        # kings
        pieces.append(Piece('white', 'king', 5, 8))
        pieces.append(Piece('black', 'king', 5, 1))

        for p in pieces:
            self.place_piece(p, p.x, p.y)


def main():
    root = Tk()
    b = Board(root, 8)
    b.start_setup()
    root.mainloop()


if __name__ == '__main__':
    main()
