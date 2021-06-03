import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
import global_var
import ball_file
import numpy as np
import time
import copy

#Bullet class
class Bullet(global_var.Object):
    def __init__(self , x , y , width , height):
        super().__init__(x,y , width , height)
        self.color = Back.WHITE + Fore.WHITE
        self.symbol = ' '
        self.expired = False
    
    def move_up(self , bricks , powerup_array):
        new_y = self.y_pos - 1
        if new_y <= global_var.WORLD_Y:
            # touched upper wall
            self.expired = True
        else:
            # hit brick
            brick_collided = None
            for brick_row in bricks:
                for brick in brick_row:
                    if not brick.exist:
                        continue
                    wall = brick.lower_wall
                    if self.x_pos >= wall[0][0] and self.x_pos <= wall[1][0] and self.y_pos >= wall[0][1] and self.y_pos <= wall[1][1]:
                        self.expired = True
                        brick_collided = brick
                        break
                    
            
            if brick_collided:
                brick_collided.decrease_strength(bricks)
            else:
                self.y_pos = new_y
    
    # set on grid
    def set_on_canvas(self , game_board):
        game_board.grid[self.y_pos][self.x_pos] = self.color + self.symbol


def move_bullets(bullet_array , bricks , powerup_array):
    for bullet in bullet_array:
        if not bullet.expired:
            bullet.move_up(bricks , powerup_array)

def check_update_bullets(bullet_array):
    filtered_arr = []
    for bullet in bullet_array:
        if not bullet.expired:
            filtered_arr.append(True)
        else:
            filtered_arr.append(False)
    
    bullet_array_filtered = np.array(bullet_array)
    bullet_array_filtered = bullet_array_filtered[filtered_arr]
    bullet_array_filtered = list(bullet_array_filtered)
    bullet_array[:] = bullet_array_filtered
        
    

        