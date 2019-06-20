from tkinter import *
from tkinter import ttk, messagebox
from Piece import *


class Board:
    """This is a class for a chess board"""
    def __init__(self, master, n: int):
        self.master = master
        self.n = n
        self.master.geometry('1250x600+10+10')
        self.master.title('Board')
        self.master.update_idletasks()  # needed for next line to work
        self.max_size = min(self.master.winfo_width(), self.master.winfo_height())  # set board size
        self.cell_size = self.max_size // self.n  # calculate the size of one square
        self.cells = []
        self.entries = None
        self.start_dict = None
        self.canvas = None
        self.pieces = None
        self.canvas_frame = ttk.Frame(self.master)
        self.controls_frame = ttk.Frame(self.master, width=650, height=600)
        self.canvas_frame.pack(side=LEFT)
        self.controls_frame.pack(side=LEFT)
        self.create_start()
        self.create_canvas()
        self.create_start()
        self.positions = self.start_dict.copy()
        self.controls()
        self.draw()

        self.master.bind('<Return>', lambda e: self.redraw())  # hit enter to submit

        self.style = ttk.Style()
        self.colour = '#444444'
        self.style.configure('TFrame', background=self.colour)
        self.style.configure('TButton', background=self.colour)
        self.style.configure('TEntry', background=self.colour)
        self.master.configure(background=self.colour)

    def create_canvas(self):
        """Create the canvas and draw the black squares"""
        self.canvas = Canvas(self.canvas_frame, width=self.max_size, height=self.max_size)
        self.canvas.pack()
        for i in range(self.n):
            for j in range(self.n):
                if (i + j) % 2 == 1:  # every other square is black
                    self.canvas.create_rectangle(i * self.cell_size, j * self.cell_size,
                                                 (i + 1) * self.cell_size, (j + 1) * self.cell_size,
                                                 fill='black')

    def place_piece(self, piece, x, y):
        """Draw given piece at given coords"""
        board_x = (x - 1) * self.cell_size + self.cell_size // 2
        board_y = (y - 1) * self.cell_size + self.cell_size // 2
        if (x + y) % 2 == 1:  # if the square is black draw a white box for the piece to go in
            pad = 27
            self.canvas.create_rectangle(board_x - pad, board_y - pad, board_x + pad, board_y + pad, fill='white')
        self.canvas.create_text(board_x, board_y, text=piece.char, font='Arial 40', tag='piece')

    def start_setup(self):
        """Create an array of all the squares and also the dict of the start positions"""
        for i in range(self.n):
            self.cells.append([])
            for j in range(self.n):
                self.cells[i].append(None)
                try:
                    self.cells[i][j] = self.start_dict[f'{i}{j}']
                except KeyError:
                    self.cells[i][j] = None
                    self.start_dict[f'{i}{j}'] = None

    def create_start(self):
        """Create the dictionary of start positions leaving all other squares as None"""
        self.start_dict = {}

        # pawns
        for i in range(self.n):
            self.start_dict[f'{i + 1}{2}'] = Piece('black', 'pawn', i + 1, 2)
            self.start_dict[f'{i + 1}{7}'] = Piece('white', 'pawn', i + 1, 7)
        # other pieces
        self.start_dict[f'{1}{8}'] = Piece('white', 'rook', 1, 8)
        self.start_dict[f'{8}{8}'] = Piece('white', 'rook', 8, 8)
        self.start_dict[f'{1}{1}'] = Piece('black', 'rook', 1, 1)
        self.start_dict[f'{8}{1}'] = Piece('black', 'rook', 8, 1)
        self.start_dict[f'{2}{8}'] = Piece('white', 'knight', 2, 8)
        self.start_dict[f'{7}{8}'] = Piece('white', 'knight', 7, 8)
        self.start_dict[f'{2}{1}'] = Piece('black', 'knight', 2, 1)
        self.start_dict[f'{7}{1}'] = Piece('black', 'knight', 7, 1)
        self.start_dict[f'{3}{8}'] = Piece('white', 'bishop', 3, 8)
        self.start_dict[f'{6}{8}'] = Piece('white', 'bishop', 6, 8)
        self.start_dict[f'{3}{1}'] = Piece('black', 'bishop', 3, 1)
        self.start_dict[f'{6}{1}'] = Piece('black', 'bishop', 6, 1)
        self.start_dict[f'{4}{8}'] = Piece('white', 'queen', 4, 8)
        self.start_dict[f'{4}{1}'] = Piece('black', 'queen', 4, 1)
        self.start_dict[f'{5}{8}'] = Piece('white', 'king', 5, 8)
        self.start_dict[f'{5}{1}'] = Piece('black', 'king', 5, 1)

        # create all other positions as None
        for i in range(self.n):
            for j in range(self.n):
                try:
                    self.start_dict[f'{i+1}{j+1}']  # if it doesn't exist it will throw a key error
                except KeyError:
                    self.start_dict[f'{i+1}{j+1}'] = None  # if the key error is thrown set it to None

    def draw(self):
        """draw the board and pieces"""
        self.canvas.destroy()  # kill the canvas and then draw it again
        self.create_canvas()

        # draw all the pieces again
        for key in self.positions.keys():
            p = self.positions[key]
            if p is not None:
                self.place_piece(p, p.x, p.y)

    def redraw(self):
        """draw the board and add new pieces from the entries"""
        self.canvas.destroy()
        self.create_canvas()

        for i in range(self.n):
            for j in range(self.n):
                entry = self.entries[i][j]
                value = entry.get()
                # a blank entry is no piece
                if value == '':
                    self.positions[f'{i + 1}{j + 1}'] = None
                    continue
                # min value length is 7 as the format is color piece and black/white is 5 letters
                # + space + first letter of piece gives 7 characters at least
                if len(value) < 7:
                    messagebox.showerror(title='Invalid Entry',
                                         message=f'Invalid Entry:\n({i + 1},{j + 1})\nEnter \'colour type\'')
                    # print('value')
                    continue
                # check that the first 5 letters are either black or white
                if value[:5].lower() in ['black', 'white']:
                    colour = value[:5]
                else:
                    messagebox.showerror(title='Invalid Colour',
                                         message=f'Invalid Entry:\n({i + 1},{j + 1})\nEnter \'black\' or \'white\'')
                    # print('value')
                    continue
                # check that from 6 on it is a valid piece
                if value[6:].lower() in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
                    piece = value[6:]
                else:
                    messagebox.showerror(title='Invalid Type',
                                         message=f'Invalid Entry:\n({i + 1},{j + 1})\nEnter \'type\' eg \'rook\'')
                    # print('value')
                    continue
                # update dict of piece positions
                self.positions[f'{i + 1}{j + 1}'] = Piece(colour, piece, i + 1, j + 1)

        # draw pieces
        for key in self.positions.keys():
            p = self.positions[key]
            if p is not None:
                self.place_piece(p, p.x, p.y)

    def clear(self):
        """clear all entry fields and the board"""
        for i in range(self.n):
            for j in range(self.n):
                entry = self.entries[i][j]
                entry.delete(0, END)
        self.redraw()

    def controls(self):
        """Set up entry fields/buttons etc."""
        self.entries = []
        for i in range(self.n):
            self.entries.append([])
            for j in range(self.n):
                self.entries[i].append(Entry(self.controls_frame, width=12))

        for i in range(self.n):
            for j in range(self.n):
                entry = self.entries[i][j]
                entry.place(relx=i / self.n, rely=j / self.n)  # .grid(row=i + 1, column=j + 1, pady=35)
                try:
                    piece = self.positions[f'{i + 1}{j + 1}']
                    entry.insert(0, f'{piece.colour} {piece.piece}')
                except KeyError:  # if the position hasn't been added to the dict (should no longer happen)
                    entry.delete(0, END)
                except AttributeError:  # if piece is None then piece.colour raises this error
                    pass

        # add submit and clear buttons to the controls
        ttk.Button(self.controls_frame, text='Submit', command=self.redraw).place(x=568, y=550)
        ttk.Button(self.controls_frame, text='Clear', command=self.clear).place(x=0, y=550)


def main():
    root = Tk()
    b = Board(root, 8)  # create the board
    root.mainloop()


if __name__ == '__main__':
    main()
