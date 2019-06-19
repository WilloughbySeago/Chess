from tkinter import *
from tkinter import ttk


class Piece:
    def __init__(self, colour, piece):
        self.colour = colour
        self.piece = piece
        self.char_dict = {
            'king': {'white': u'\u2654', 'black': u'\u265A'},
            'queen': {'white': u'\u2655', 'black': u'\u265B'},
            'rook': {'white': u'\u2656', 'black': u'\u265C'},
            'bishop': {'white': u'\u2657', 'black': u'\u265D'},
            'knight': {'white': u'\u2658', 'black': u'\u265E'},
            'pawn': {'white': u'\u2659', 'black': u'\u265F'},
        }
        self.char = self.char_dict[piece][colour]


p = Piece('white', 'king')
print(p.char_dict)
