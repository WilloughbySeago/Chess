from tkinter import *
from tkinter import ttk
import numpy as np

class Board:
    def __init__(self, n):
        self.n = n

    def create_board(self):
        for i in range(self.n):
            for j in range(self.n):