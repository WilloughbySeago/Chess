from tkinter import *
from tkinter import ttk, messagebox
from Piece import *


class Board:
    def __init__(self, master, n):
        self.master = master
        self.n = n
        self.run_for_normal_chess()
        self.master.geometry('1250x600+10+10')
        self.master.title('Board')
        self.master.update_idletasks()
        self.max_size = min(self.master.winfo_width(), self.master.winfo_height())
        self.master.update_idletasks()
        self.cell_size = self.max_size // self.n
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

        self.master.bind('<Return>', lambda e: self.redraw())

    def create_canvas(self):
        self.canvas = Canvas(self.canvas_frame, width=self.max_size, height=self.max_size)
        self.canvas.pack()
        for i in range(self.n):
            for j in range(self.n):
                if (i + j) % 2 == 1:
                    self.canvas.create_rectangle(i * self.cell_size, j * self.cell_size,
                                                 (i + 1) * self.cell_size, (j + 1) * self.cell_size,
                                                 fill='black')

    def place_piece(self, piece, x, y):
        board_x = (x - 1) * self.cell_size + self.cell_size // 2
        board_y = (y - 1) * self.cell_size + self.cell_size // 2
        if (x + y) % 2 == 1:
            pad = 27
            self.canvas.create_rectangle(board_x - pad, board_y - pad, board_x + pad, board_y + pad, fill='white')
        self.canvas.create_text(board_x, board_y, text=piece.char, font='Arial 40', tag='piece')

    def start_setup(self):
        for i in range(self.n):
            self.cells.append([])
            for j in range(self.n):
                self.cells[i].append(None)
                try:
                    self.cells[i][j] = self.start_dict[f'{i}{j}']
                except KeyError:
                    self.cells[i][j] = None

    def create_start(self):
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

    def draw(self):
        self.canvas.destroy()
        self.create_canvas()

        for key in self.positions.keys():
            p = self.positions[key]
            if p is not None:
                self.place_piece(p, p.x, p.y)

    def redraw(self):
        self.canvas.destroy()
        self.create_canvas()

        for i in range(self.n):
            for j in range(self.n):
                entry = self.entries[i][j]
                value = entry.get()
                if value == '':
                    self.positions[f'{i + 1}{j + 1}'] = None
                    continue
                if len(value) < 7:
                    messagebox.showerror(title='Invalid Entry',
                                         message=f'Invalid Entry:\n({i + 1},{j + 1})\nEnter \'colour type\'')
                    print('value')
                    continue
                if value[:5].lower() in ['black', 'white']:
                    colour = value[:5]
                else:
                    messagebox.showerror(title='Invalid Colour',
                                         message=f'Invalid Entry:\n({i + 1},{j + 1})\nEnter \'black\' or \'white\'')
                    print('value')
                    continue
                if value[6:].lower() in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
                    piece = value[6:]
                else:
                    messagebox.showerror(title='Invalid Type',
                                         message=f'Invalid Entry:\n({i + 1},{j + 1})\nEnter \'type\' eg \'rook\'')
                    print('value')
                    continue
                self.positions[f'{i + 1}{j + 1}'] = Piece(colour, piece, i + 1, j + 1)

        for key in self.positions.keys():
            p = self.positions[key]
            if p is not None:
                self.place_piece(p, p.x, p.y)

    def clear(self):
        for i in range(self.n):
            for j in range(self.n):
                entry = self.entries[i][j]
                entry.delete(0, END)
        self.redraw()

    def controls(self):
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
                except KeyError:
                    entry.delete(0, END)

        ttk.Button(self.controls_frame, text='Submit', command=self.redraw).place(x=568, y=550)  # relx=-200, rely=550)
        ttk.Button(self.controls_frame, text='Clear', command=self.clear).place(x=0, y=550)


def main():
    root = Tk()
    b = Board(root, 8)
    b.start_setup()
    b.draw()
    root.mainloop()


if __name__ == '__main__':
    main()
