import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
import global_var
import util
import math
import numpy as np


# Ball Object Class
class Ball(global_var.Object):
    def __init__(self , x , y , starting_stuck):
        super().__init__(x , y , 1 , 1)
        self.ball_arr = []
        self.color = Back.BLACK + Fore.WHITE
        self.x_velo = 1
        self.y_velo = -1
        self.bar_stuck = starting_stuck #position where ball is stuck to bar
        self.isThruBall = 0 # if ball is a thru ball
        self.dead = False # if ball is dead

    # make the ball characters   
    def make(self):
        self.ball_arr = []
        self.ball_arr.append("O")
    
    # setting it on the grid
    def set_on_canvas(self,game_board):
        game_board.grid[self.y_pos][self.x_pos] = self.color + self.ball_arr[0]
    
    # increase speed in fast ball powerup
    def inc_speed(self):
        direction = 0
        if self.y_velo > 0:
            direction = 1
        elif self.y_velo < 0:
            direction = -1
        
        y_mag = abs(self.y_velo)
        y_mag = math.ceil(y_mag*1.5)
        self.y_velo = direction*y_mag
    
    # decrease speed back to normal
    def dec_speed(self):
        direction = 0
        if self.y_velo > 0:
            direction = 1
        elif self.y_velo < 0:
            direction = -1
        
        y_mag = abs(self.y_velo)
        y_mag = math.floor(y_mag/1.5)
        self.y_velo = direction*y_mag

    
    def check_and_update(self , bar , bricks , powerup_array , ufo_obj):
        old_x = self.x_pos
        old_y = self.y_pos
        new_x = self.x_pos + self.x_velo
        new_y = self.y_pos + self.y_velo
        if self.bar_stuck != None:
            stuck_pos = bar.x_pos + self.bar_stuck
            if stuck_pos > bar.x_pos + bar.width - 1:
                stuck_pos = bar.x_pos + bar.width - 1
            
            self.x_pos = stuck_pos
            self.y_pos = old_y
            self.bar_stuck = stuck_pos - bar.x_pos
            return

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
        debug_cnt = 1
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
                    
                    # check collision with bricks
                    first_coll = self.check_bricks(direction , bricks , poss_x , poss_y , cur_vx , cur_vy)
                    if first_coll:
                        # if ball is thru ball then cancel collsion and destroy brick
                        if self.isThruBall > 0:
                            brick_obliterated = first_coll[3]
                            if not brick_obliterated.isExploding:
                                brick_obliterated.dissapear()
                            else:
                                brick_obliterated.explode(bricks)
                            first_coll = False
                    
                    if first_coll:
                        first_int = (source_x , poss_y)
                        break
                    
                    else:
                        if global_var.LEVEL == 4:
                            #check with ufo
                            first_coll = self.check_ufo(direction , ufo_obj , poss_x , poss_y , cur_vx , cur_vy)
                        
                        if first_coll:
                            first_int = (source_x , poss_y)
                            break
                        else:
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
                        
                        #check collision with bricks
                        first_coll = self.check_bricks(direction , bricks , poss_x , poss_y , cur_vx , cur_vy)
                        if first_coll:
                            # if ball is thru ball then cancel collsion and destroy brick
                            if self.isThruBall > 0:
                                brick_obliterated = first_coll[3]
                                if not brick_obliterated.isExploding:
                                    brick_obliterated.dissapear()
                                else:
                                    brick_obliterated.explode(bricks)
                                first_coll = False
                        
                        if first_coll:
                            first_int = (poss_x , source_y)
                            break
                        else:
                            if global_var.LEVEL == 4:
                                first_coll = self.check_ufo(direction , ufo_obj , poss_x , poss_y , cur_vx , cur_vy)
                            
                            if first_coll:
                                first_int = (poss_x , source_y)
                                break
                            else:
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
                        
                        #check collision with bricks
                        second_coll = self.check_bricks(direction , bricks , poss_x , poss_y , cur_vx , cur_vy)
                        if second_coll:
                            #if ball is thru ball then cancel collision and destroy brick
                            if self.isThruBall > 0:
                                brick_obliterated = second_coll[3]
                                if not brick_obliterated.isExploding:
                                    brick_obliterated.dissapear()
                                else:
                                    brick_obliterated.explode(bricks)
                                second_coll = False
                            
                        if second_coll:
                            second_int = (poss_x , source_y)
                            break
                        else:
                            if global_var.LEVEL == 4:
                                second_coll = self.check_ufo(direction , ufo_obj , poss_x , poss_y , cur_vx , cur_vy)
                            
                            if second_coll:
                                second_int = (poss_x , source_y)
                                break
                            else:
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
                            
                            #check collision with bricks
                            second_coll = self.check_bricks(direction , bricks , poss_x , poss_y , cur_vx , cur_vy)
                            if second_coll:
                                #if ball is thru ball then cancel collision and destroy brick
                                if self.isThruBall > 0:
                                    brick_obliterated = second_coll[3]
                                    if not brick_obliterated.isExploding:
                                        brick_obliterated.dissapear()
                                    else:
                                        brick_obliterated.explode(bricks)
                                    second_coll = False

                            if second_coll:
                                second_int = (source_x , poss_y)
                                break
                            else:
                                if global_var.LEVEL == 4:
                                    second_coll = self.check_ufo(direction , ufo_obj , poss_x , poss_y , cur_vx , cur_vy)
                                
                                if second_coll:
                                    second_int = (source_x , poss_y)
                                    break
                                else:
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
                    debug_cnt += 3                    
                    break
                
                elif first_coll:
                    # first try collision
                    int_points.append(first_int)
                    collisions.append(first_coll)
                    debug_cnt += 3
                    break
                else:
                    # second try collision
                    int_points.append(second_int)
                    collisions.append(second_coll)
                    debug_cnt += 3
                    break

            # if no collision

            cur_x = cur_x + x_step
            cur_y = cur_y + y_step
            

        if len(collisions):
            # there were collisions
            if len(collisions) == 1:
                col = collisions[0]
                if col[0] == 'BRICK':
                    # destroy/damage brick
                    brick_collided = col[3]
                    brick_collided.decrease_strength(bricks)
                    if not brick_collided.exist:
                        if global_var.LEVEL != 4:
                            util.spawn_new_powerup(powerup_array , brick_collided.x_pos , brick_collided.y_pos , self.x_velo , self.y_velo)
                
                #decrease UFO health
                if col[0] == 'UFO':
                    ufo_obj.hurt(bricks)
                        
                
                int_p = int_points[0]
                updated_vx = updated_vx + col[1]
                updated_vy = updated_vy + col[2]
                self.x_pos = int_p[0]
                self.y_pos = int_p[1]
                if col[0] == 'BAR':
                    # make bricks fall
                    if global_var.isFalling:
                        util.fall_bricks(bricks , bar)
                    # check if bar is sticky
                    if bar.isSticky > 0:
                        self.bar_stuck = self.x_pos - bar.x_pos
                
                if col[0] == 'D_WALL':
                    self.dead = True
                
                self.x_velo = updated_vx
                self.y_velo = updated_vy          
            
            else:
                col1 = collisions[0]
                col2 = collisions[1]
                if col1[0] == 'BRICK':
                    #destroy/damage bricks
                    brick_collided1 = col1[3]
                    brick_collided1.decrease_strength(bricks)
                    if not brick_collided1.exist:
                        #spawn new powerup
                        if global_var.LEVEL != 4:
                            util.spawn_new_powerup(powerup_array , brick_collided1.x_pos , brick_collided1.y_pos , self.x_velo , self.y_velo)
                if col2[0] == 'BRICK':
                    #destroy/damage bricks
                    brick_collided2 = col2[3]
                    if brick_collided2 != brick_collided1:
                        brick_collided2.decrease_strength(bricks)
                        if not brick_collided2.exist:
                            if global_var.LEVEL != 4:
                                util.spawn_new_powerup(powerup_array , brick_collided2.x_pos , brick_collided2.y_pos , self.x_velo , self.y_velo)
                
                if col1[0] == 'UFO' or col2[0] == 'UFO':
                    ufo_obj.hurt(bricks)
                
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
                    if global_var.isFalling:
                        util.fall_bricks(bricks , bar)
                    # check if bar is sticky
                    if bar.isSticky > 0:
                        self.bar_stuck = self.x_pos - bar.x_pos
                
                if col1[0] == 'D_WALL' or col2[0] == 'D_WALL':
                    self.dead = True
                
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
    
    # function to check collision with a brick
    def check_bricks(self , direction ,  bricks , poss_x , poss_y , vx , vy):
        # which brick wall
        if direction == 'R':
            coll_wall = 'L'
            
        if direction == 'L':
            coll_wall = 'R'

        if direction == 'U':
            coll_wall = 'D'

        if direction == 'D':
            coll_wall = 'U'

        coll = False
        dx = 0
        dy = 0
        brick_collided = None
        # traversing through bricks
        for brick_row in bricks:
            for brick in brick_row:
                if not brick.exist:
                    continue
                if coll_wall == 'R':
                    wall = brick.right_wall
                    if poss_x >= wall[0][0] and poss_x <= wall[1][0] and poss_y >= wall[0][1] and poss_y <= wall[1][1]:
                        coll = True
                        dx = -2*vx
                        dy = 0
                        brick_collided = brick
                        break
                
                elif coll_wall == 'U':
                    wall = brick.upper_wall
                    if poss_x >= wall[0][0] and poss_x <= wall[1][0] and poss_y >= wall[0][1] and poss_y <= wall[1][1]:
                        coll = True
                        dx = 0
                        dy = -2*vy
                        brick_collided = brick
                        break
                
                elif coll_wall == 'L':
                    wall = brick.left_wall
                    if poss_x >= wall[0][0] and poss_x <= wall[1][0] and poss_y >= wall[0][1] and poss_y <= wall[1][1]:
                        coll = True
                        dx = -2*vx
                        dy = 0
                        brick_collided = brick
                        break
                
                elif coll_wall == 'D':
                    wall = brick.lower_wall
                    if poss_x >= wall[0][0] and poss_x <= wall[1][0] and poss_y >= wall[0][1] and poss_y <= wall[1][1]:
                        coll = True
                        dx = 0
                        dy = -2*vy
                        brick_collided = brick
                        break
        
        if not coll:
            return coll
        
        return ('BRICK' , dx , dy , brick_collided)

    #function to check ufo collision
    def check_ufo(self , direction ,  ufo_obj , poss_x , poss_y , vx , vy):
        # which ufo wall
        if direction == 'R':
            coll_wall = 'L'
            
        if direction == 'L':
            coll_wall = 'R'

        if direction == 'U':
            coll_wall = 'D'

        if direction == 'D':
            coll_wall = 'U'

        coll = False
        dx = 0
        dy = 0
    
        if coll_wall == 'R':
            wall = ((ufo_obj.x_pos + ufo_obj.width - 1 , ufo_obj.y_pos) , (ufo_obj.x_pos + ufo_obj.width - 1 , ufo_obj.y_pos+ufo_obj.height-1)) #right wall
            if poss_x >= wall[0][0] and poss_x <= wall[1][0] and poss_y >= wall[0][1] and poss_y <= wall[1][1]:
                coll = True
                dx = -2*vx
                dy = 0
        
        elif coll_wall == 'U':
            wall = ((ufo_obj.x_pos , ufo_obj.y_pos) , (ufo_obj.x_pos + ufo_obj.width -1  , ufo_obj.y_pos)) #upper wall
            if poss_x >= wall[0][0] and poss_x <= wall[1][0] and poss_y >= wall[0][1] and poss_y <= wall[1][1]:
                coll = True
                dx = 0
                dy = -2*vy
        
        elif coll_wall == 'L':
            wall = ((ufo_obj.x_pos , ufo_obj.y_pos) , (ufo_obj.x_pos , ufo_obj.y_pos+ufo_obj.height-1)) #left wall
            if poss_x >= wall[0][0] and poss_x <= wall[1][0] and poss_y >= wall[0][1] and poss_y <= wall[1][1]:
                coll = True
                dx = -2*vx
                dy = 0
        
        elif coll_wall == 'D':
            wall = ((ufo_obj.x_pos , ufo_obj.y_pos + ufo_obj.height -1) , (ufo_obj.x_pos + ufo_obj.width - 1 , ufo_obj.y_pos+ufo_obj.height-1)) #lower wall
            if poss_x >= wall[0][0] and poss_x <= wall[1][0] and poss_y >= wall[0][1] and poss_y <= wall[1][1]:
                coll = True
                dx = 0
                dy = -2*vy
        
        if not coll:
            return coll
        
        return ('UFO' , dx , dy)


# function to move all balls
def move_balls(ball_array , bar , bricks , powerup_array , ufo_obj):
    for ball in ball_array:
        if not ball.dead:
            ball.check_and_update(bar , bricks , powerup_array , ufo_obj)

# function to remove dead balls
def check_filter_balls(ball_array):
    filtered_arr = []
    for ball in ball_array:
        if not ball.dead:
            filtered_arr.append(True)
        else:
            filtered_arr.append(False)
    
    ball_array_filtered = np.array(ball_array)
    ball_array_filtered = ball_array_filtered[filtered_arr]
    ball_array_filtered = list(ball_array_filtered)
    ball_array[:] = ball_array_filtered
    return len(ball_array)



