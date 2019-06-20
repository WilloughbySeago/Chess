from Board import *


class MoveChecker(Board):
    def __init__(self, master, n):
        Board.__init__(self, master, n)
        self.master = master
        self.n = n
        self.entry = ttk.Entry(self.controls_frame)
        self.entry.place(x=200, y=550)
        self.label = ttk.Label(self.controls_frame, text='Enter row and column number '
                                                         'in format xy, \'all\' or \'colour\'')
        self.label.place(x=170, y=575)
        ttk.Button(self.controls_frame, text='Check', command=self.what_to_check).place(x=350, y=550)

    def what_to_check(self):
        value = self.entry.get()

        if len(value) not in [2, 3, 5]:
            messagebox.showerror(title='Check error', message='Invalid format, enter either:'
                                                              '\n-Coordinates in format \'xy\''
                                                              '\n-The word \'all\''
                                                              '\n-\'black\' or \'white\'')
            return

        # initialise as None
        mode = None
        x, y, = None, None

        # if xy entered get x and y
        if len(value) == 2:
            mode = 'xy'
            try:
                x = int(value[0])
            except ValueError:
                messagebox.showerror(title='Invalid Input', message='To enter coordinates enter xy as integers.'
                                                                    '\nthe x you entered wasn\'t a integer')
                return
            try:
                y = int(value[1])
            except ValueError:
                messagebox.showerror(title='Invalid Input', message='To enter coordinates enter xy as integers.'
                                                                    '\nthe y you entered wasn\'t a integer')
                return
            try:
                self.positions[f'{x}{y}']
            except KeyError:
                messagebox.showerror(title='Not a piece', message='There is no piece in that square\n'
                                                                  'Note that (1, 1) is the top left corner')
                return

        # if keyword entered set mode to key word
        if value.lower() == 'all':
            mode = 'all'

        if value.lower() == 'white':
            mode = 'white'

        if value.lower() == 'black':
            mode = 'black'

        if mode is None:
            messagebox.showerror(title='Invalid input', message='Invalid format, enter either:'
                                                                '\n-Coordinates in format \'xy\''
                                                                '\n-The word \'all\''
                                                                '\n-\'black\' or \'white\'')
            return
        if x is not None:
            self.get_check_list(mode, x=x, y=y)
        else:
            self.get_check_list(mode)

    def get_check_list(self, mode, x=0, y=0):
        to_check = []
        if mode == 'xy':
            to_check.append((x, y))

        elif mode == 'all':
            for i in range(self.n + 1):
                for j in range(self.n + 1):
                    try:
                        if self.positions[f'{i}{j}'] is not None:
                            to_check.append((i, j))
                    except KeyError:
                        pass

        elif mode == 'white':
            for i in range(self.n + 1):
                for j in range(self.n + 1):
                    try:
                        if self.positions[f'{i}{j}'] is not None:
                            if self.positions[f'{i}{j}'].colour == 'white':
                                to_check.append((i, j))
                    except KeyError:
                        pass

        elif mode == 'black':
            for i in range(self.n + 1):
                for j in range(self.n + 1):
                    try:
                        if self.positions[f'{i}{j}'] is not None:
                            if self.positions[f'{i}{j}'].colour == 'black':
                                to_check.append((i, j))
                    except KeyError:
                        pass

        for p in to_check:
            print(self.positions[f'{p[0]}{p[1]}'])
            self.check(p)

        for p in to_check:
            self.canvas.create_oval(p[0] * self.cell_size - self.cell_size // 2 + 10,
                                    p[1] * self.cell_size - self.cell_size // 2 + 10,
                                    p[0] * self.cell_size - self.cell_size // 2 - 10,
                                    p[1] * self.cell_size - self.cell_size // 2 - 10, fill='yellow')

    def check(self, p):
        piece = self.positions[f'{p[0]}{p[1]}']
        allowed = []

        # if the piece is a pawn check its possible spots
        if piece.piece == 'pawn':
            if piece.colour == 'white':
                point = (p[0], p[1] - 1)  # can always move 1 forward
                if self.is_empty(point, 'white'):
                    allowed.append(point)
                if piece.y == 7:
                    point = (p[0], p[1] - 2)  # can move 2 forward the first time they move
                    if self.is_empty(point, 'white'):
                        allowed.append(point)

            else:
                point = (p[0], p[1] + 1)  # can always move 1 forward
                if self.is_empty(point, 'black'):
                    allowed.append(point)
                if piece.y == 2:
                    point = (p[0], p[1] + 2)  # can move 2 forward the first time the move
                    if self.is_empty(point, 'black'):
                        allowed.append(point)

        for p in allowed:
            self.canvas.create_oval(p[0] * self.cell_size - self.cell_size // 2 + 10,
                                    p[1] * self.cell_size - self.cell_size // 2 + 10,
                                    p[0] * self.cell_size - self.cell_size // 2 - 10,
                                    p[1] * self.cell_size - self.cell_size // 2 - 10, fill='red')

    def is_empty(self, point, colour):
        try:
            contents = self.positions[f'{point[0]}{point[1]}']  # get contents of square
            if contents is None:  # in there is nothing there
                return True
            if contents.colour == colour:  # if the piece there in the same colour
                return False
            else:
                return True  # if the piece is the opposite colour then a move there is valid
        except KeyError:
            return True  # if self.positions[xy] hasn't been created yet then it is empty


def main():
    root = Tk()
    move_checker = MoveChecker(root, 8)
    root.mainloop()


if __name__ == '__main__':
    main()
