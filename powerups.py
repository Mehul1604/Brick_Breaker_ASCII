import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
import global_var
import ball_file
import numpy as np
import time
import copy
import math
import random
import util


# Powerup parent class
class Powerup:
    def __init__(self , x , y , x_v , y_v):
        self.x_pos = x
        self.y_pos = y
        self.x_velo = x_v
        self.y_velo = y_v
        self.duration = global_var.POWERUP_DURATION
        self.type = ''
        self.color = Back.LIGHTRED_EX + Fore.BLUE
        self.symbol = 'X'
        self.expired = False
        self.isActive = False
        self.began = None
    
    def apply(self , bar , ball_array):
        pass
    
    def remove(self , bar , ball_array):
        pass
    
    # make the powerup fall by a unit
    # def move_down(self , bar , ball_array):
    #     new_y = self.y_pos + 1
    #     if new_y >= global_var.WORLD_Y + global_var.HEIGHT - 1:
    #         # touched bottom wall
    #         self.expired = True
    #     else:
    #         # caught by bar
    #         if self.x_pos >= bar.x_pos and self.x_pos <= bar.x_pos + bar.width - 1 and new_y >= bar.y_pos:
    #             self.isActive = True
    #             self.began = time.time()
    #             self.apply(bar , ball_array)
    #         else:
    #             self.y_pos = new_y

    def fall(self):
        self.y_velo += 1
    
    # check if powerup is expired
    def check_expired(self , bar , ball_array):
        if (time.time() - self.began) >= self.duration:
            self.expired = True
            self.isActive = False
            self.began = None
            self.remove(bar , ball_array)
    
    # set on grid
    def set_on_canvas(self , game_board):
        game_board.grid[self.y_pos][self.x_pos] = self.color + self.symbol
    
    def check_and_update(self , bar , ball_array):
        old_x = self.x_pos
        old_y = self.y_pos
        new_x = self.x_pos + self.x_velo
        new_y = self.y_pos + self.y_velo

        # create an estimated path from current position to new position
        estimation_path = util.create_estimation(old_x , old_y , new_x , new_y)
            
        
        cur_x = old_x
        cur_y = old_y
        cur_vx = self.x_velo
        cur_vy = self.y_velo
        updated_vx = cur_vx
        updated_vy = cur_vy
        int_points = []
        collisions = []

        # traversing point by point on the path
        for p in estimation_path:
            x_step = p[0]
            y_step = p[1]
            poss_x = cur_x
            poss_y = cur_y
            
            first_steps = 0
            second_steps = 0
            first_int = None
            second_int = None
            first_coll = False
            second_coll = False

            #first try
            
            if x_step:
                for i in range(abs(x_step)):
                    source_x = poss_x
                    if x_step > 0:
                        poss_x = poss_x + 1
                    else:
                        poss_x = poss_x - 1
                    
                    first_steps = first_steps + 1
                    
                    direction = ''
                    if x_step > 0:
                        direction = 'R'
                    else:
                        direction = 'L'
                    
                    
                    if direction == 'D':
                        #check collision with bar
                        first_coll = self.check_bar(bar , poss_x , poss_y , cur_vx , cur_vy)
                    
                    if first_coll:
                        first_int = (source_x , poss_y)
                        break
                    else:
                        # check collsion with walls
                        first_coll = self.check_walls(direction , poss_x , poss_y , cur_vx ,  cur_vy)
                        if first_coll:
                            first_int = (source_x , poss_y)
                            break

            
            if not first_coll:
                if y_step:
                    for i in range(abs(y_step)):
                        source_y = poss_y
                        if y_step > 0:
                            poss_y = poss_y + 1
                        else:
                            poss_y = poss_y - 1

                        first_steps = first_steps + 1
                        
                        direction = ''
                        if y_step < 0:
                            direction = 'U'
                        else:
                            direction = 'D'
                        
                        
                        if direction == 'D':
                            #check collision with bar
                            first_coll = self.check_bar(bar , poss_x , poss_y , cur_vx , cur_vy)
                        
                        if first_coll:
                            first_int = (poss_x , source_y)
                            break
                        else:
                            # check collision with walls
                            first_coll = self.check_walls(direction , poss_x , poss_y , cur_vx ,  cur_vy)
                            if first_coll:
                                first_int = (poss_x , source_y)
                                break
                            

            poss_x = cur_x
            poss_y = cur_y

            if x_step != 0 and y_step != 0:
                #second try
                if y_step:
                    for i in range(abs(y_step)):
                        source_y = poss_y
                        if y_step > 0:
                            poss_y = poss_y + 1
                        else:
                            poss_y = poss_y - 1

                        second_steps = second_steps + 1
            
                        direction = ''
                        if y_step < 0:
                            direction = 'U'
                        else:
                            direction = 'D'
                        
                        
                        if direction == 'D':
                            # check collision with bar
                            second_coll = self.check_bar(bar , poss_x , poss_y , cur_vx , cur_vy)
                        
                        if second_coll:
                            second_int = (poss_x , source_y)
                            break
                        else:
                            #check collision with walls
                            second_coll = self.check_walls(direction , poss_x , poss_y , cur_vx ,  cur_vy)
                            if second_coll:
                                second_int = (poss_x , source_y)
                                break
                        
                
                if not second_coll:
                    if x_step:
                        for i in range(abs(x_step)):
                            source_x = poss_x
                            if x_step > 0:
                                poss_x = poss_x + 1
                            else:
                                poss_x = poss_x - 1
                            
                            second_steps = second_steps + 1

                            direction = ''
                            if x_step > 0:
                                direction = 'R'
                            else:
                                direction = 'L'
                            
                            if direction == 'D':
                                #check collision with bar
                                second_coll = self.check_bar(bar , poss_x , poss_y , cur_vx , cur_vy)
                            
                            if second_coll:
                                second_int = (source_x , poss_y)
                                break
                            else:
                                #check collision with walls
                                second_coll = self.check_walls(direction , poss_x , poss_y , cur_vx ,  cur_vy)
                                if second_coll:
                                    second_int = (source_x , poss_y)
                                    break
                            

            if first_coll or second_coll:
                # collision occured
                if first_coll and second_coll:
                    if first_steps < second_steps:
                        # take the first try collision
                        int_points.append(first_int)
                        collisions.append(first_coll)

                    elif second_steps < first_steps:
                        #take the second try collision
                        int_points.append(second_int)
                        collisions.append(second_coll)
                    
                    else:
                        # double collision
                        if first_int[0] == second_int[0] and first_int[1] == second_int[1]:
                            int_points.append(first_int)
                        else:
                            int_points.append(first_int)
                            int_points.append(second_int)
                        
                        collisions.append(first_coll)
                        collisions.append(second_coll)                 
                    break
                
                elif first_coll:
                    # first try collision
                    int_points.append(first_int)
                    collisions.append(first_coll)
                    break
                else:
                    # second try collision
                    int_points.append(second_int)
                    collisions.append(second_coll)
                    break

            # if no collision
            cur_x = cur_x + x_step
            cur_y = cur_y + y_step
            

        if len(collisions):
            # there were collisions
            if len(collisions) == 1:
                col = collisions[0]
                                        
                int_p = int_points[0]
                updated_vx = updated_vx + col[1]
                updated_vy = updated_vy + col[2]
                self.x_pos = int_p[0]
                self.y_pos = int_p[1]
                if col[0] == 'BAR':
                    self.isActive = True
                    self.began = time.time()
                    self.apply(bar , ball_array)
                
                if col[0] == 'D_WALL':
                    self.expired = True

                
                self.x_velo = updated_vx
                self.y_velo = updated_vy          
            
            else:
                col1 = collisions[0]
                col2 = collisions[1]
                
                if len(int_points) == 1:
                    int_p = int_points[0]
                else:
                    int_p1 = int_points[0]
                    int_p2 = int_points[1]
                    int_p = (int_p2[0] , int_p1[1])
                
                updated_vx = updated_vx + (col1[1] + col2[1])
                updated_vy = updated_vy + (col1[2] + col2[2])
                self.x_pos = int_p[0]
                self.y_pos = int_p[1]
                if col1[0] == 'BAR' or col2[0] == 'BAR':
                    self.isActive = True
                    self.began = time.time()
                    self.apply(bar , ball_array)
                
                if col1[0] == "D_WALL" or col2[0] == "D_WALL":
                    self.expired = True
                    
                self.x_velo = updated_vx
                self.y_velo = updated_vy
        else:
            # No collisions
            self.x_pos = new_x
            self.y_pos = new_y
    
    # function to check wall collision
    def check_walls(self , direction ,  poss_x , poss_y , vx , vy):
        coll_wall = direction
        coll = False
        dx = 0
        dy = 0
        if coll_wall == 'R':
            # right wall
            wall = (global_var.WORLD_Y , global_var.WORLD_Y + global_var.HEIGHT -1)
            if poss_x == global_var.WORLD_X + global_var.WIDTH - 1:
                if poss_y >= wall[0] and poss_y <= wall[1]:
                    coll = True
                    dx = -2*vx
                    dy = 0
                    return ('R_WALL' , dx , dy)

        elif coll_wall == 'U':
            # upper wall
            wall = (global_var.WORLD_X , global_var.WORLD_X + global_var.WIDTH -1)
            if poss_y == global_var.WORLD_Y:
                if poss_x >= wall[0] and poss_x <= wall[1]:
                    coll = True
                    dx = 0
                    dy = -2*vy
                    return ('U_WALL' , dx , dy)
        
        elif coll_wall == 'L':
            # left wall
            wall = (global_var.WORLD_Y , global_var.WORLD_Y + global_var.HEIGHT -1)
            if poss_x == global_var.WORLD_X:
                if poss_y >= wall[0] and poss_y <= wall[1]:
                    coll = True
                    dx = -2*vx
                    dy = 0
                    return ('L_WALL' , dx , dy)
        
        elif coll_wall == 'D':
            # lower wall
            wall = (global_var.WORLD_X , global_var.WORLD_X + global_var.WIDTH -1)
            if poss_y == global_var.WORLD_Y + global_var.HEIGHT -1:
                if poss_x >= wall[0] and poss_x <= wall[1]:
                    # self.dead = True # ball dies
                    coll = True
                    dx = 0
                    dy = -2*vy
                    return ('D_WALL' , dx , dy)
        
        if not coll:
            return coll
        
        

    # function to check collision with bar
    def check_bar(self , bar , poss_x , poss_y , vx , vy):
        # defining bar area for physics
        edge_length = int(bar.width / 3)
        centre_length = bar.width - 2*edge_length
        left_edge = (bar.x_pos , bar.x_pos + edge_length - 1)
        centre = (bar.x_pos + edge_length , bar.x_pos + edge_length + centre_length - 1)
        right_edge = (bar.x_pos + edge_length + centre_length , bar.x_pos + bar.width - 1)
        dx = 0
        dy = 0
        coll = False
        if poss_y == bar.y_pos:
            if poss_x >= left_edge[0] and poss_x <= right_edge[1]:
                coll = True
                dy = -2*vy
                if poss_x >= left_edge[0] and poss_x <= left_edge[1]:
                    dx = (poss_x - left_edge[1] - 1)
                elif poss_x >= centre[0] and poss_x <= centre[1]:
                    dx = 0
                else:
                    dx = (poss_x - right_edge[0] + 1)
        
        
        if not coll:
            return coll
        
        return ('BAR' , dx , dy)
    
    
        
    

# GrowBar Powerup class
class GrowBar(Powerup):
    def __init__(self,x,y , x_v , y_v):
        super().__init__(x,y , x_v , y_v)
        self.type = global_var.GROW_BAR
        self.symbol = global_var.GROW_BAR_SYM
        self.color = global_var.GROW_BAR_COL
    

    # apply
    def apply(self , bar , ball_array):
        bar.grow_bar()
    
    # remove
    def remove(self , bar , ball_array):
        bar.shrink_bar()

#ShrinkBar Powerup class
class ShrinkBar(Powerup):
    def __init__(self,x,y , x_v , y_v):
        super().__init__(x,y , x_v , y_v)
        self.type = global_var.SHRINK_BAR
        self.symbol = global_var.SHRINK_BAR_SYM
        self.color = global_var.SHRINK_BAR_COL
    
    
    #apply
    def apply(self , bar , ball_array):
        bar.shrink_bar()
    
    #remove
    def remove(self , bar , ball_array):
        bar.grow_bar()

#StickyBar Powerup class
class StickyBar(Powerup):
    def __init__(self , x , y , x_v , y_v):
        super().__init__(x,y , x_v , y_v)
        self.type = global_var.STICKY_BAR
        self.symbol = global_var.STICKY_BAR_SYM
        self.color = global_var.STICKY_BAR_COL

    
    #apply
    def apply(self , bar , ball_array):
        bar.isSticky = bar.isSticky + 1
        if bar.isSticky == 1:
            bar.color = Back.BLUE
    
    #remove
    def remove(self , bar , ball_array):
        bar.isSticky = bar.isSticky - 1
        if bar.isSticky == 0:
            bar.color = Back.WHITE


#FastBall Powerup class
class FastBall(Powerup):
    def __init__(self , x , y , x_v , y_v):
        super().__init__(x,y , x_v , y_v)
        self.type = global_var.FAST_BALL
        self.symbol = global_var.FAST_BALL_SYM
        self.color = global_var.FAST_BALL_COL

    
    #apply
    def apply(self , bar , ball_array):
        for ball in ball_array:
            ball.inc_speed()
    
    #remove
    def remove(self , bar , ball_array):
        for ball in ball_array:
            ball.dec_speed()

#ThruBall Powerup class
class ThruBall(Powerup):
    def __init__(self , x , y , x_v , y_v):
        super().__init__(x,y , x_v , y_v)
        self.type = global_var.THRU_BALL
        self.symbol = global_var.THRU_BALL_SYM
        self.color = global_var.THRU_BALL_COL

    
    #apply
    def apply(self , bar , ball_array):
        for ball in ball_array:
            ball.isThruBall = ball.isThruBall + 1
            if ball.isThruBall == 1:
                ball.color = Back.BLACK + Fore.YELLOW
    
    #remove
    def remove(self , bar , ball_array):
        for ball in ball_array:
            ball.isThruBall = ball.isThruBall - 1
            if ball.isThruBall == 0:
                ball.color = Back.BLACK + Fore.WHITE


#MultiBall Powerup class
class MultiBall(Powerup):
    def __init__(self , x , y , x_v , y_v):
        super().__init__(x,y , x_v , y_v)
        self.type = global_var.MULTI_BALL
        self.symbol = global_var.MULTI_BALL_SYM
        self.color = global_var.MULTI_BALL_COL
    
    #apply
    def apply(self , bar , ball_array):
        duplicate_arr = []
        for ball in ball_array:
            new_ball_obj = copy.deepcopy(ball)
            new_ball_obj.y_velo = new_ball_obj.y_velo*-1
            new_ball_obj.x_velo = new_ball_obj.x_velo
            new_ball_obj.make()
            duplicate_arr.append(new_ball_obj)
        
        for dup_ball in duplicate_arr:
            ball_array.append(dup_ball)

#shoot poweup
class ShootBar(Powerup):
    def __init__(self ,x , y , x_v , y_v):
        super().__init__(x , y , x_v , y_v)
        self.type = global_var.SHOOT_BAR
        self.symbol = global_var.SHOOT_BAR_SYM
        self.color = global_var.SHOOT_BAR_COL
    
    def apply(self , bar , ball_arr):
        bar.isShoot += 1
    
    def remove(self , bar , ball_arr):
        bar.isShoot -= 1

    def get_time_remaining(self , cur_time):
        return math.ceil(self.began + self.duration - cur_time)
        
    







def move_powerups(powerup_array , bar , ball_array):
    for powerup in powerup_array:
        if (not powerup.isActive) and (not powerup.expired):
            powerup.check_and_update(bar , ball_array)
        
        elif powerup.isActive:
            powerup.check_expired(bar , ball_array)

#decrease y velocity of powerups
def gravity_powerups(powerup_array):
    for powerup in powerup_array:
        if (not powerup.isActive) and (not powerup.expired):
            powerup.fall()
        
def check_update_powerups(powerup_array):
    filtered_arr = []
    for powerup in powerup_array:
        if not powerup.expired:
            filtered_arr.append(True)
        else:
            filtered_arr.append(False)
    
    powerup_array_filtered = np.array(powerup_array)
    powerup_array_filtered = powerup_array_filtered[filtered_arr]
    powerup_array_filtered = list(powerup_array_filtered)
    powerup_array[:] = powerup_array_filtered
    # print("\033[%d;%dH length of new powerup array is %d" % (14 , 150 , len(powerup_array)) , end='' , flush=True)
        
def check_shoot_time(powerup_array):
    shoot_time = 0
    cur_time = time.time()
    for powerup in powerup_array:
        if not powerup.expired:
            if powerup.isActive:
                if powerup.type == global_var.SHOOT_BAR:
                    shoot_time = max(powerup.get_time_remaining(cur_time),shoot_time)
    
    return shoot_time