from Board import *


class MoveChecker(Board):
    """This is a class derived from the Board class with extra functions to check the legal moves a piece has"""

    def __init__(self, master, n):
        Board.__init__(self, master, n)  # call to Board.__init__ to create board
        self.master = master
        self.n = n
        self.entry = ttk.Entry(self.controls_frame)  # add the entry field to specify which pieces to check
        self.entry.place(x=200, y=550)
        self.label = ttk.Label(self.controls_frame, text='Enter row and column number '
                                                         'in format xy, \'all\' or \'colour\'')  # add instruction label
        self.label.place(x=170, y=575)
        # add button to check current selection
        ttk.Button(self.controls_frame, text='Check', command=self.what_to_check).place(x=350, y=550)
        self.draw()

    def what_to_check(self):
        """Get user input from entry to choose what pieces to check"""
        value = self.entry.get()

        if len(value) not in [2, 3, 5]:  # allowed inputs are xy or all or black/white hence the allowed lengths
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
        if mode == 'xy':
            self.get_check_list(mode, x=x, y=y)
        else:
            self.get_check_list(mode)

    def get_check_list(self, mode, x=0, y=0):
        """Depending on the mode get list of squares containing the pieces to check"""
        to_check = []
        if mode == 'xy':
            try:
                self.positions[f'{x}{y}']
            except KeyError:
                pass
            to_check.append((x, y))
            # nice and simple just check the given point contains a piece and add it to the list

        elif mode == 'all':
            # iterate through all squares and any that have a piece are added to the list
            for i in range(self.n + 1):
                for j in range(self.n + 1):
                    try:
                        if self.positions[f'{i}{j}'] is not None:
                            to_check.append((i, j))
                    except KeyError:
                        # if self.positions['ij'] hasn't been created yet
                        # this will be raised (should not happen anymore)
                        pass

        elif mode == 'white':
            # iterate through squares and if it contains a white piece add it to the list
            for i in range(self.n + 1):
                for j in range(self.n + 1):
                    try:
                        if self.positions[f'{i}{j}'] is not None:
                            if self.positions[f'{i}{j}'].colour == 'white':
                                to_check.append((i, j))
                    except KeyError:  # shouldn't happen as should be initialised to None
                        pass

        elif mode == 'black':
            # see comments above for mode == 'white'
            for i in range(self.n + 1):
                for j in range(self.n + 1):
                    try:
                        if self.positions[f'{i}{j}'] is not None:
                            if self.positions[f'{i}{j}'].colour == 'black':
                                to_check.append((i, j))
                    except KeyError:
                        pass

        for p in to_check:
            # print values to check (for debugging purposes)
            print(self.positions[f'{p[0]}{p[1]}'])
            self.check(p)

        for p in to_check:
            # draw a circle over every piece to be checked
            r = 10  # radius
            self.canvas.create_oval(p[0] * self.cell_size - self.cell_size // 2 + r,
                                    p[1] * self.cell_size - self.cell_size // 2 + r,
                                    p[0] * self.cell_size - self.cell_size // 2 - r,
                                    p[1] * self.cell_size - self.cell_size // 2 - r, fill='yellow')

    def check(self, p):
        """p is a point (x, y) check the possible moves of the point at p"""
        piece = self.positions[f'{p[0]}{p[1]}']
        allowed = []
        x, y = p  # extract x and y values from point
        # if the piece is a pawn check its possible spots
        if piece.piece == 'pawn':
            if piece.colour == 'white':
                point = (x, y - 1)  # can always move 1 forward
                if self.can_move_to(point, 'white'):
                    allowed.append(point)
                if piece.y == 7:
                    point = (x, y - 2)  # can move 2 forward the first time they move
                    if self.can_move_to(point, 'white') and self.can_move_to((x, y - 1), 'white') and self.can_move_to(
                            (x, y - 1), 'black'):  # check that the point to move to and the point between are valid
                        allowed.append(point)
                point = (x - 1, y - 1)  # check diagonals, if there is a black piece then it is a valid spot
                try:
                    contents = self.positions[f'{x - 1}{y - 1}']
                except KeyError:  # should no longer happen
                    pass
                else:
                    if contents is not None:
                        if contents.colour == 'black':
                            allowed.append(point)
                point = (x + 1, y - 1)
                try:
                    contents = self.positions[f'{x + 1}{y - 1}']
                except KeyError:  # should no longer happen
                    pass
                else:
                    if contents is not None:
                        if contents.colour == 'black':
                            allowed.append(point)

            else:
                point = (x, y + 1)  # can always move 1 forward
                if self.can_move_to(point, 'black'):
                    allowed.append(point)
                if piece.y == 2:
                    point = (x, y + 2)  # can move 2 forward the first time the move
                    if self.can_move_to(point, 'black') and self.can_move_to((x, y + 1), 'black') and self.can_move_to(
                            (x, y + 1), 'white'):  # check that the point to move to and the point between are valid
                        allowed.append(point)
                point = (x - 1, y + 1)  # check diagonals, if there is a white piece then it is a valid spot
                try:
                    contents = self.positions[f'{x - 1}{y + 1}']
                except KeyError:  # should no longer happen
                    pass
                else:
                    if contents is not None:
                        if contents.colour == 'white':
                            allowed.append(point)
                point = (x + 1, y + 1)
                try:
                    contents = self.positions[f'{x + 1}{y + 1}']
                except KeyError:  # should no longer happen
                    pass
                else:
                    if contents is not None:
                        if contents.colour == 'white':
                            allowed.append(point)

        for p in allowed:
            # draw a red circle on all spots the piece(s) could move to
            r = 15  # radius
            self.canvas.create_oval(p[0] * self.cell_size - self.cell_size // 2 + r,
                                    p[1] * self.cell_size - self.cell_size // 2 + r,
                                    p[0] * self.cell_size - self.cell_size // 2 - r,
                                    p[1] * self.cell_size - self.cell_size // 2 - r, fill='red')

    def can_move_to(self, point, colour):
        """Check if a square is either empty or contains a piece of the opposite colour that can be taken"""
        try:
            contents = self.positions[f'{point[0]}{point[1]}']  # get contents of square
            if contents is None:  # there is nothing there
                return True
            if contents.colour == colour:  # if the piece there in the same colour then the spot isn't valid
                return False
            else:
                return True  # if the piece is the opposite colour then a move there is valid
        except KeyError:
            return True  # if self.positions[xy] hasn't been created yet then it is empty


def main():
    root = Tk()
    move_checker = MoveChecker(root, 8)  # create the game
    root.mainloop()


if __name__ == '__main__':
    main()
