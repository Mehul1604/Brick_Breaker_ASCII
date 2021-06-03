import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
import global_var

# Bar object class
class Bar(global_var.Object):
    def __init__(self):
        super().__init__(global_var.WORLD_X + int(global_var.WIDTH/2) - 5 , global_var.WORLD_Y + global_var.HEIGHT -3 , 10 , 1)
        self.bar_arr = []
        self.color = Back.WHITE
        self.isSticky = 0 # if sticky bar powerup is active
        self.isShoot = 0 #if it has shooting powerup
        self.shootTime = 0
        self.bombHit = 0 #if it was hit by a bomb
        

    #making on local array
    def make(self):
        self.bar_arr = []
        for i in range(self.width):
            self.bar_arr.append((" "))
    
    #setting it on grid
    def set_on_canvas(self,game_board):
        if self.isShoot < 1:
            for i in range(self.width):
                game_board.grid[self.y_pos][self.x_pos+i] = self.color +  self.bar_arr[i]
        else:
            half = int(self.width/2)
            left_half = half-1
            for i in range(self.width):
                if i == half or i == left_half:
                    game_board.grid[self.y_pos-1][self.x_pos+i] = self.color +  self.bar_arr[i]
                else:
                    game_board.grid[self.y_pos-1][self.x_pos+i] = Back.BLACK + self.bar_arr[i]
            
            for i in range(self.width):
                    game_board.grid[self.y_pos][self.x_pos+i] = self.color +  self.bar_arr[i]
    
    
    # bar movement with boundaries
    def move(self , delx):
        if (not (delx < 0 and (self.x_pos + delx) < global_var.WORLD_X)) and (not (delx > 0 and (self.x_pos + self.width -1 + delx) > global_var.WORLD_X + global_var.WIDTH-1)):
            self.x_pos = self.x_pos + delx
    
    # increase bar width 
    def grow_bar(self):
        self.width = self.width + 2
        self.make()

    # decrease bar width
    def shrink_bar(self):
        if self.width >= 6:
            self.width = self.width - 2
            self.make()
    
        