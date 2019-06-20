from Board import *


class MoveChecker(Board):
    def __init__(self, master, n):
        Board.__init__(self, master, n)
        self.master = master
        self.n = n
        self.entry = ttk.Entry(self.controls_frame)
        self.entry.place(x=260, y=550)
        self.label = ttk.Label(self.controls_frame, text='Enter row and column number '
                                                         'in format xy, \'all\' or \'colour\'')
        self.label.place(x=170, y=575)
        ttk.Button(self.controls_frame, text='Check', command=self.what_to_check)

    def what_to_check(self):
        value = self.entry.get()
        if len(value) not in [4, 3, 5]:
            messagebox.showerror(title='Check error', message='Invalid format, enter either:'
                                                              '\n-Coordinates in format \'xy\''
                                                              '\n-The word \'all\''
                                                              '\n-\'black\' or \'white\'')
            return
        mode = None

        # if xy entered get x and y
        if len(value) == 2:
            mode = 'single'
            try:
                x = int(value[1])
            except ValueError:
                messagebox.showerror(title='Invalid Input', message='To enter coordinates enter xy as integers.'
                                                                    '\n the x you entered wasn\'t a integer')
                return
            try:
                y = int(value[2])
            except ValueError:
                messagebox.showerror(title='Invalid Input', message='To enter coordinates enter xy as integers.'
                                                                    '\n the y you entered wasn\'t a integer')
            if self.positions[f'{x}{y}'] is None:
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










def main():
    root = Tk()
    move_checker = MoveChecker(root, 8)
    root.mainloop()


if __name__ == '__main__':
    main()
