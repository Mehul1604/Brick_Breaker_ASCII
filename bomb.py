import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
import global_var
import numpy as np
import time
import copy

#bomb class
class Bomb(global_var.Object):
    def __init__(self , x , y , width , height):
        super().__init__(x,y , width , height)
        self.color = Back.RED + Fore.WHITE
        self.symbol = 'O'
        self.expired = False
    
    #drop down
    def move_down(self , bar):
        new_y = self.y_pos + 1
        if new_y >= global_var.WORLD_Y + global_var.HEIGHT -1:
            # touched lower wall
            self.expired = True
        else:
            #caught by bar
            if self.x_pos >= bar.x_pos and self.x_pos <= bar.x_pos + bar.width - 1 and new_y >= bar.y_pos:
                self.expired = True
                bar.bombHit = 1
            else:
                self.y_pos = new_y
    
    # set on grid
    def set_on_canvas(self , game_board):
        game_board.grid[self.y_pos][self.x_pos] = self.color + self.symbol


def move_bombs(bomb_array , bar):
    for bomb in bomb_array:
        if not bomb.expired:
            bomb.move_down(bar)

def check_update_bombs(bomb_array):
    filtered_arr = []
    for bomb in bomb_array:
        if not bomb.expired:
            filtered_arr.append(True)
        else:
            filtered_arr.append(False)
    
    bomb_array_filtered = np.array(bomb_array)
    bomb_array_filtered = bomb_array_filtered[filtered_arr]
    bomb_array_filtered = list(bomb_array_filtered)
    bomb_array[:] = bomb_array_filtered
        
    

        