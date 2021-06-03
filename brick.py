import colorama
from colorama import Fore, Back, Style
import random
import powerups
import global_var
colorama.init(autoreset=True)

# Brick object class
class Brick(global_var.Object):
    def __init__(self , x , y , width , height , strength):
        super().__init__(x,y , width , height)
        self.brick_arr = []
        # defining collision walls
        self.upper_wall = ((x , y) , (x + width-1 , y))
        self.lower_wall = ((x , y+height-1), (x+width-1 , y+height-1))
        self.left_wall = ((x , y) , (x , y+height-1))
        self.right_wall = ((x+width-1 , y) , (x+width-1 , y+height-1))
        self.strength = strength # strength of brick
        self.color = None
        self.unbreakable = False # is brick unbreakable
        self.isExploding = False #is brick exploding
        self.isRandom = False
        self.exist = True
        if strength == -1:
            self.unbreakable = True
        if strength == -2:
            self.isExploding = True
        
        if not self.unbreakable:
            if not self.isExploding:
                if strength == 1:
                    self.color = Back.BLUE + Fore.WHITE
                elif strength == 2:
                    self.color = Back.GREEN + Fore.WHITE
                elif strength == 3:
                    self.color = Back.YELLOW + Fore.WHITE
            else:
                self.color = Back.WHITE + Fore.BLACK
        else:
            self.color = Back.RED + Fore.WHITE

    # making the characters of brick
    def make(self):
        self.brick_arr = []
        self.exist = True
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if j==0 or j==4:
                    row.append("|")
                else:
                    row.append("-")
            self.brick_arr.append(row)
    
    # damage the brick
    def decrease_strength(self ,  bricks):
        if self.isRandom:
            self.isRandom = False
            return
        
        if self.unbreakable:
            return
        
        if self.isExploding:
            self.explode(bricks)
            return
        
        
        
        self.strength = self.strength - 1
        if self.strength == 0:
            self.dissapear()
        else:
            if self.strength == 1:
                global_var.SCORE += 1
                self.color = Back.BLUE + Fore.WHITE
            elif self.strength == 2:
                global_var.SCORE += 1
                self.color = Back.GREEN + Fore.WHITE

    # destroying the brick 
    def dissapear(self):
        if self.isRandom:
            self.isRandom = False
        
        global_var.SCORE += 3
        
        
        self.exist = False

    # explode brick
    def explode(self ,bricks):
        self.dissapear()
        x_range = (self.x_pos - self.width , self.x_pos + self.width)
        y_range = (self.y_pos - self.height , self.y_pos + self.height)

        # damaging 3*3 area
        for b_row in bricks:
            for b in b_row:
                if b.exist:
                    if b.x_pos >= x_range[0] and b.x_pos <= x_range[1] and b.y_pos >= y_range[0] and b.y_pos <= y_range[1]:
                        if not b.isExploding:
                            b.dissapear()
                        else:
                            b.explode(bricks)
                
    #setting on grid
    def set_on_canvas(self , game_board):
        for i in range(self.height):
            for j in range(self.width):
                game_board.grid[self.y_pos+i][self.x_pos+j] = self.color +  self.brick_arr[i][j]

    #for rainbow bricks
    def set_strength(self , new_strength):
        self.unbreakable = False # is brick unbreakable
        self.isExploding = False #is brick exploding

        self.strength = new_strength
        if self.strength == -1:
            self.unbreakable = True
        if self.strength == -2:
            self.isExploding = True
        
        if not self.unbreakable:
            if not self.isExploding:
                if self.strength == 1:
                    self.color = Back.BLUE + Fore.WHITE
                elif self.strength == 2:
                    self.color = Back.GREEN + Fore.WHITE
                elif self.strength == 3:
                    self.color = Back.YELLOW + Fore.WHITE
            else:
                self.color = Back.WHITE + Fore.BLACK
        else:
            self.color = Back.RED + Fore.WHITE
        

# get number of destroyed bricks
def get_bricks_destroyed(bricks):
    cnt = 0
    for b_row in bricks:
        for b in b_row:
            if not b.exist:
                cnt += 1
    
    return cnt

#get number of breakable bricks left
def get_bricks_left(bricks):
    cnt = 0
    for b_row in bricks:
        for b in b_row:
            if b.exist and (not b.unbreakable):
                cnt += 1
    
    return cnt


