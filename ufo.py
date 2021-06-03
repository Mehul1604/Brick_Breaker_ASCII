import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
import global_var
import util
import brick
import numpy as np
import bomb
import time
import copy

# UFO class
class UFO(global_var.Object):
    def __init__(self , x , y , width , height):
        super().__init__(x,y , width , height)
        self.color = Back.BLACK + Fore.WHITE
        self.ufo_arr = []
        self.health = global_var.UFO_HEALTH
    
    def make(self):
        self.ufo_arr = []
        for r in global_var.UFO_ARR:
            self.ufo_arr.append(r)
    
    #follow the bar
    def move_to(self , x):
        if not ((x < global_var.WORLD_X) or ((x + self.width -1)  > (global_var.WORLD_X + global_var.WIDTH-1))):
            self.x_pos = x
    
    #decrease health
    def hurt(self , bricks):
        self.health -= 1
        global_var.SCORE += 3
        if self.health == 8:
            self.spawn_bricks_easy(bricks)
        elif self.health == 4:
            self.spawn_bricks_hard(bricks)
    
    # spawn bomb
    def drop_bomb(self , bomb_array):
        new_bomb = bomb.Bomb(self.x_pos + int(self.width/2) , self.y_pos + self.height -1 , 1 , 1)
        bomb_array.append(new_bomb)
    
    #spawn first layer of defensive bricks
    def spawn_bricks_easy(self , bricks):
        bricks[:] = util.make_bricks()
        X = global_var.BRICK_LEFT
        Y = self.y_pos + self.height + 1
        defensive_row = []
        for i in range(global_var.BRICK_ROW):
            strnth = 1
            brick_obj = brick.Brick(X , Y , global_var.BRICK_WIDTH , global_var.BRICK_HEIGHT , strnth)
            brick_obj.make()
            defensive_row.append(brick_obj)
            X += global_var.BRICK_WIDTH
        
        bricks.append(defensive_row)
    
    #spawn second layer of defensive bricks
    def spawn_bricks_hard(self , bricks):
        bricks[:] = util.make_bricks()
        X = global_var.BRICK_LEFT
        Y = self.y_pos + self.height + 1
        defensive_row = []
        for i in range(global_var.BRICK_ROW):
            if i%2 == 0:
                strnth = 1
            else:
                strnth = 2
            brick_obj = brick.Brick(X , Y , global_var.BRICK_WIDTH , global_var.BRICK_HEIGHT , strnth)
            brick_obj.make()
            defensive_row.append(brick_obj)
            X += global_var.BRICK_WIDTH
        
        bricks.append(defensive_row)


    # set on grid
    def set_on_canvas(self , game_board):
        for i in range(self.height):
            for j in range(self.width):
                game_board.grid[self.y_pos+i][self.x_pos+j] = self.color + self.ufo_arr[i][j]


        
    

        