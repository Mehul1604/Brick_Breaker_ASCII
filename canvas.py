import numpy as np
import random
import colorama
from colorama import Fore , Back , Style
import brick
import bar
import ball_file
colorama.init(autoreset=True)

#class for the canvas for the 2d grid
class Canvas:
    def __init__(self , rows , cols , orig_x , orig_y):
        self.rows = rows
        self.cols = cols
        self.grid = []  # 2d grid to hold all characters
        self.orig_x = orig_x
        self.orig_y = orig_y
    
    # make the background
    def make_canvas(self):
        self.grid = []
        for r in range(self.rows + self.orig_y):
            row = []
            if r < self.orig_y:
                for c in range(self.cols + self.orig_x):
                    row.append(Back.RESET + " ")
            else:
                for c in range(self.cols + self.orig_x):
                    if c < self.orig_x:
                        row.append(Back.RESET + " ")
                    else:
                        if r == self.orig_y or r == self.orig_y + self.rows -1 or  c == self.orig_x + self.cols -1 or c == self.orig_x:
                            row.append(Back.WHITE + Fore.WHITE + " ")
                        else:
                            row.append(Back.BLACK + Fore.BLACK + " ")
            
            self.grid.append(row)
            
    # print everything
    def draw_canvas(self):
        canvas_str = ""
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                canvas_str += self.grid[r][c]
            
            canvas_str += '\n'    

        print('\033[H' + canvas_str)
    

    