from os import system
from time import sleep
import random
import input
import brick
import canvas
import sys
import bar
import ball_file
import powerups
import global_var
import math

    
def clear():
    _ = system('clear')

# make the brick layout
def make_bricks():
    filename = ''
    if global_var.LEVEL == 1:
        filename = './levels/level1.txt'
    if global_var.LEVEL == 2:
        filename = './levels/level2.txt'
    if global_var.LEVEL == 3:
        filename = './levels/level3.txt'
    if global_var.LEVEL == 4:
        filename = './levels/level4.txt'

    BRICK_LAYOUT = []

    f = open(filename)
    b_rows = f.readlines()

    for b_r in b_rows:
        row = []
        for ch in b_r:
            if ch != '\n':
                row.append(int(ch))

        BRICK_LAYOUT.append(row)

    brick_arr = []
    cur_x = global_var.BRICK_LEFT
    cur_y = global_var.BRICK_UP
    for row in BRICK_LAYOUT:
        b_row = []
        cur_x = global_var.BRICK_LEFT
        for num in row:
            if num > 0:
                st = 1
                if num == 1:
                    st = 1
                elif num == 2:
                    st = 2
                elif num == 3:
                    st = 3
                elif num == 4:
                    st = -1 # unbreakable
                elif num == 5:
                    st = -2 # exploding
                elif num == 6:
                    st = 1
                
                brick_obj = brick.Brick(cur_x , cur_y , global_var.BRICK_WIDTH , global_var.BRICK_HEIGHT , st)
                if num == 6:
                    brick_obj.isRandom = True
                brick_obj.make()
                b_row.append(brick_obj)
            
            cur_x = cur_x + global_var.BRICK_WIDTH
        
        brick_arr.append(b_row)
        cur_y = cur_y + global_var.BRICK_HEIGHT

    return brick_arr

# function to create an estimation line for ball trajectory
def create_estimation(old_x , old_y , new_x , new_y):
    dx = new_x - old_x
    dy = new_y - old_y
    
    x_dir = 0
    y_dir = 0
    if dx < 0:
        x_dir = -1
    elif dx > 0:
        x_dir = 1
    else:
        x_dir = 0
    
    if dy < 0:
        y_dir = -1
    elif dy > 0:
        y_dir = 1
    else:
        y_dir = 0
    
    dx = abs(dx)
    dy = abs(dy)
    
    if dx >= dy:
        if dy:
            x_step = math.ceil(dx/dy)
            y_step = 1
        else:
            x_step = 1
            y_step = 0
    else:
        if dx:
            y_step = math.ceil(dy/dx)
            x_step = 1
        else:
            y_step = 1
            x_step = 0
    
    
    estimation_path = []
    while dx or dy:
        pair = [0,0]
        if dx:
            if (dx - x_step) < 0:
                pair[0] = dx
                dx = 0
            else:
                pair[0] = x_step
                dx = dx - x_step
        
        if dy:
            if (dy - y_step) < 0:
                pair[1] = dy
                dy = 0
            else:
                pair[1] = y_step
                dy = dy - y_step
        
        pair[0] = pair[0]*x_dir
        pair[1] = pair[1]*y_dir
        estimation_path.append(pair)
    
    return estimation_path

#make bricks fall
def fall_bricks(cur_bricks , bar):
    for b_row in cur_bricks:
        for b in b_row:
            b.y_pos = b.y_pos + 1
            b.upper_wall = ((b.x_pos , b.y_pos) , (b.x_pos + b.width-1 , b.y_pos))
            b.lower_wall = ((b.x_pos , b.y_pos+b.height-1), (b.x_pos+b.width-1 , b.y_pos+b.height-1))
            b.left_wall = ((b.x_pos , b.y_pos) , (b.x_pos , b.y_pos+b.height-1))
            b.right_wall = ((b.x_pos+b.width-1 , b.y_pos) , (b.x_pos+b.width-1 , b.y_pos+b.height-1))
            if b.exist:
                if b.y_pos + b.height  >= bar.y_pos:
                    global_var.BRICKS_FELL = True
                    break

#change rainbow brick color
def update_rainbow_bricks(cur_bricks):
    for b_row in cur_bricks:
        for b in b_row:
            if b.exist:
                if b.isRandom:
                    prev_strength = b.strength
                    if prev_strength == 1 or prev_strength == 2:
                        b.set_strength(prev_strength+1)
                    elif prev_strength == 3:
                        b.set_strength(1)


#create new powerup with 40% chance
def spawn_new_powerup(powerup_array ,x , y , x_v , y_v):
    chance = random.randint(0,100)
        # 40% chance to spawn a powerup
    if chance <= 80:
        new_type = random.choice(global_var.POWERUP_TYPES)
        if new_type == global_var.GROW_BAR:
            new_powerup = powerups.GrowBar(x , y , x_v , y_v)
        elif new_type == global_var.SHRINK_BAR:
            new_powerup = powerups.ShrinkBar(x , y , x_v , y_v)
        elif new_type == global_var.STICKY_BAR:
            new_powerup = powerups.StickyBar(x , y , x_v , y_v)
        elif new_type == global_var.FAST_BALL:
            new_powerup = powerups.FastBall(x , y , x_v , y_v)
        elif new_type == global_var.THRU_BALL:
            new_powerup = powerups.ThruBall(x , y , x_v , y_v)
        elif new_type == global_var.MULTI_BALL:
            new_powerup = powerups.MultiBall(x , y , x_v , y_v)
        elif new_type == global_var.SHOOT_BAR:
            new_powerup = powerups.ShootBar(x , y , x_v , y_v)

        powerup_array.append(new_powerup)
        


# load up game
def start_up():
    print('Game is loading..\n')
    sleep(2)
    clear()
    
# function to set all objects and characters on the 2D grid
def set_canvas(game_board , brick_grid , bar , ball_array , powerup_array , bullet_array , bomb_array):
    game_board.make_canvas()
    for br_row in brick_grid:
        for br in br_row:
            if br.exist:
              br.set_on_canvas(game_board)
    
    bar.set_on_canvas(game_board)
    for ball in ball_array:
        ball.set_on_canvas(game_board)

    for powerup in powerup_array:
        if not powerup.isActive:
            powerup.set_on_canvas(game_board)

    for bullet in bullet_array:
        if not bullet.expired:
            bullet.set_on_canvas(game_board)
    
    for bomb in bomb_array:
        if not bomb.expired:
            bomb.set_on_canvas(game_board)


# Function when a life is lost
def life_lost(ball_array ,powerup_array , bullet_array , bomb_array):
    # making new bar and ball
    fresh_bar_player = bar.Bar()
    starting_ball_x = random.randint(fresh_bar_player.x_pos , fresh_bar_player.x_pos + fresh_bar_player.width)
    starting_stuck = starting_ball_x - fresh_bar_player.x_pos
    fresh_ball_obj = ball_file.Ball(starting_ball_x , fresh_bar_player.y_pos-1 , starting_stuck)
    fresh_bar_player.make()
    fresh_ball_obj.make()
    powerup_array[:] = []
    bullet_array[:] = []
    bomb_array[:] = []
    ball_array[:] = [fresh_ball_obj]
    return fresh_bar_player

def level_cleared(ball_array ,powerup_array , bullet_array , bomb_array):
    # making new bar and ball
    fresh_bar_player = bar.Bar()
    starting_ball_x = random.randint(fresh_bar_player.x_pos , fresh_bar_player.x_pos + fresh_bar_player.width)
    starting_stuck = starting_ball_x - fresh_bar_player.x_pos
    fresh_ball_obj = ball_file.Ball(starting_ball_x , fresh_bar_player.y_pos-1 , starting_stuck)
    fresh_bar_player.make()
    fresh_ball_obj.make()
    powerup_array[:] = []
    bullet_array[:] = []
    bomb_array[:] = []
    ball_array[:] = [fresh_ball_obj]
    next_brick_grid = make_bricks()
    return (fresh_bar_player , next_brick_grid)

# Function to show game instructions
def show_instructions():
    print("\033[%d;%dH"%(1 , 150) , end='')
    print("\033[%d;%dH BRICKS:"%(2 , 150) , end='')
    sample_brick1 = brick.Brick(0,0,5,2,1)
    sample_brick1.make()
    sample_brick2 = brick.Brick(0,0,5,2,2)
    sample_brick2.make()
    sample_brick3 = brick.Brick(0,0,5,2,3)
    sample_brick3.make()
    sample_unbreakable = brick.Brick(0,0,5,2,-1)
    sample_unbreakable.make()
    sample_exploding = brick.Brick(0,0,5,2,-2)
    sample_exploding.make()
    sample_brick_arr = [sample_brick1 , sample_brick2 , sample_brick3 , sample_unbreakable , sample_exploding]

    r_num = 2
    
    for br in sample_brick_arr:
        r_num += 1
        for i in range(br.height):
            r_num += 1
            print("\033[%d;%dH" % (r_num , 150) , end='')
            for j in range(br.width):
                print(br.color + br.brick_arr[i][j] , end='')
            
        r_num += 1
        if br.unbreakable:
            print("\033[%d;%dH Unbreakable" % (r_num , 150) , end='')
        elif br.isExploding:
            print("\033[%d;%dH Exploding" % (r_num , 150) , end='')
        else:
            print("\033[%d;%dH Strength: %d" % (r_num , 150 , br.strength) , end='')
    
    
    r_num += 3
    print("\033[%d;%dH POWERUPS:" % (r_num , 150) , end='')
    sample_grow_bar = powerups.GrowBar(0,0 , 0 , 0)
    sample_shrink_bar = powerups.ShrinkBar(0,0 , 0 , 0)
    sample_sticky_bar = powerups.StickyBar(0,0 , 0 , 0)
    sample_fast_ball = powerups.FastBall(0,0 , 0 , 0)
    sample_thru_bar = powerups.ThruBall(0,0 , 0 , 0)
    sample_multi_bar = powerups.MultiBall(0,0 , 0 , 0)
    sample_shoot_bar = powerups.ShootBar(0,0 , 0 , 0)
    sample_powerup_arr = [sample_grow_bar , sample_shrink_bar , sample_sticky_bar , sample_fast_ball , sample_thru_bar , sample_multi_bar , sample_shoot_bar]

    for pwrp in sample_powerup_arr:
        r_num += 2
        print("\033[%d;%dH" % (r_num , 150) , end='')
        print(pwrp.color + pwrp.symbol , end='')

        if pwrp.type == global_var.GROW_BAR:
            print(" Grow Bar" , end='')
        elif pwrp.type == global_var.SHRINK_BAR:
            print(" Shrink Bar" , end='')
        elif pwrp.type == global_var.STICKY_BAR:
            print(" Sticky Bar" , end='')
        elif pwrp.type == global_var.FAST_BALL:
            print(" Fast Ball" , end='')
        elif pwrp.type == global_var.THRU_BALL:
            print(" Thru Ball" , end='')
        elif pwrp.type == global_var.MULTI_BALL:
            print(" Multi Ball" , end='')
        elif pwrp.type == global_var.SHOOT_BAR:
            print(" Shoot Bar" , end='')
    
    r_num += 2
    print("\033[%d;%dHControls" % (r_num , 150) , end='')
    r_num += 1
    print("\033[%d;%dHA - Move Left | D - Move Right | R - Release Ball | Q - Quit" % (r_num , 144) , end='')
    r_num += 1
    print("\033[%d;%dHX - Skip Level" % (r_num , 144) , end='')




