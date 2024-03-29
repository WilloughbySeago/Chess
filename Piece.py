class Piece:
    def __init__(self, colour, piece, x=None, y=None):
        self.colour = colour
        self.piece = piece
        self.x = x
        self.y = y
        self.char_dict = {
            'king': {'white': u'\u2654', 'black': u'\u265A'},
            'queen': {'white': u'\u2655', 'black': u'\u265B'},
            'rook': {'white': u'\u2656', 'black': u'\u265C'},
            'bishop': {'white': u'\u2657', 'black': u'\u265D'},
            'knight': {'white': u'\u2658', 'black': u'\u265E'},
            'pawn': {'white': u'\u2659', 'black': u'\u265F'},
        }
        self.char = self.char_dict[piece][colour]

    def __repr__(self):
        if self.colour == 'white':
            return f'<Chess piece: {self.colour} {self.piece} {self.char_dict[self.piece]["black"]}>'
        else:
            return f'<Chess piece: {self.colour} {self.piece} {self.char_dict[self.piece]["white"]}>'
