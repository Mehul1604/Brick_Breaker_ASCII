from os import system
import time
from time import sleep
import random
import colorama
from colorama import Fore , Back , Style
import input
import brick
import canvas
import sys
import bar
import ball_file
import powerups
import bullet
import bomb
import ufo
import global_var
import util
colorama.init(autoreset=True)

# making cursor dissapear and turning off echo mode
system("stty -echo")
sys.stdout.write("\033[?25l")
sys.stdout.flush()
global_var.LEVEL = 1
while 1:
    # starting/restarting game and re initializing objects
    util.start_up()
    getch = input.Get()
    bar_player = bar.Bar()
    starting_ball_x = random.randint(bar_player.x_pos , bar_player.x_pos + bar_player.width)
    starting_stuck = starting_ball_x - bar_player.x_pos
    ball_obj = ball_file.Ball(starting_ball_x , bar_player.y_pos -1 , starting_stuck)
    ball_array = [ball_obj]
    bar_player.make()
    ball_obj.make()

    global_var.LEVEL = 1
    won = 0
    
    #initializing bricks , bombs , bullets
    brick_grid = util.make_bricks()
    powerup_array = []
    bullet_array = []
    bomb_array = []
    global_var.falling_time = 0
    global_var.isFalling = False

    global_var.BRICKS_FELL = False
   

    # making the game world and defining boundaries (Canavas class)
    game_world = canvas.Canvas(global_var.HEIGHT , global_var.WIDTH , global_var.WORLD_X , global_var.WORLD_Y)
    game_world.make_canvas()
    global_var.LIVES = 8
    global_var.SCORE = 0


    # starting game time
    global_var.prev_time = time.time()
    global_var.isPlaying = False
    global_var.played_time = 0
    util.show_instructions()

    ufo_obj = None
    while 1:

        # TAKING INPUT
        ch = input.input_to(getch)
        if ch:
            if ch == 'q' or ch == 'Q' or ord(ch) == 3 or ord(ch) == 4 or ord(ch) == 26:
                break
        
            
        # STATE UPDATE
        if ch == 'a' or ch == 'A':
            bar_player.move(-2)
        if ch == 'd' or ch =='D':
            bar_player.move(2)
        if ch == 'r' or ch == 'R':
            if not global_var.isPlaying:
                global_var.isPlaying = True
                global_var.prev_time = time.time()
            for ball in ball_array:
                ball.bar_stuck = None
        
        #skip level
        if ch == 'x' or ch == 'X':
            global_var.LEVEL += 1
            if global_var.LEVEL > 4:
                won = 1
                break
            
            if global_var.LEVEL == 4:
                ufo_obj = ufo.UFO(bar_player.x_pos - int(global_var.UFO_WIDTH/2) + int(bar_player.width/2) , global_var.UFO_Y , global_var.UFO_WIDTH , global_var.UFO_HEIGHT)
                ufo_obj.make()
            
            #reset and increase level
            ret = util.level_cleared(ball_array , powerup_array , bullet_array , bomb_array)
            bar_player = ret[0]
            brick_grid = ret[1]
            global_var.isPlaying = False
            global_var.isFalling = False
            global_var.falling_time = 0
            reposition = "\033[{};{}H".format(global_var.WORLD_Y + global_var.HEIGHT +5 , 0)
            level_str = "\n\t\t\t\t\t\t\t\t\t\t\t  " + Back.WHITE + Fore.BLACK + Style.BRIGHT +  "LEVEL CLEARED!"
            print(reposition + level_str , end='')
            sleep(2)
            reset_str = "\n\t\t\t\t\t\t\t\t\t\t\t  " + Back.RESET + Fore.RESET  +  "              "
            print(reposition + reset_str , end='')
            continue
        
        # update balls
        ball_file.move_balls(ball_array , bar_player , brick_grid , powerup_array , ufo_obj)
        util.update_rainbow_bricks(brick_grid)
        rem_balls = ball_file.check_filter_balls(ball_array)
        if rem_balls == 0 or bar_player.bombHit:
            global_var.LIVES = global_var.LIVES - 1
            if global_var.LIVES == 0:
                break
            else:
                # life lost
                bar_player = util.life_lost(ball_array , powerup_array , bullet_array , bomb_array)
                global_var.isPlaying = False
                continue
        
        if global_var.BRICKS_FELL:
            global_var.LIVES = 0
            break

        # update powerups and bricks and bullets
        powerups.move_powerups(powerup_array , bar_player , ball_array)
        powerups.check_update_powerups(powerup_array)

        bullet.move_bullets(bullet_array , brick_grid , powerup_array)
        bullet.check_update_bullets(bullet_array)

        #update bombs
        if global_var.LEVEL == 4:
            bomb.move_bombs(bomb_array , bar_player)
            bomb.check_update_bombs(bomb_array)


        bricks_broken = brick.get_bricks_destroyed(brick_grid)
        bricks_left = brick.get_bricks_left(brick_grid)

        if global_var.LEVEL == 4:
            ufo_obj.move_to(bar_player.x_pos - int(global_var.UFO_WIDTH/2) + int(bar_player.width/2))
        
        #capture the passing of 1 second as an event
        if global_var.isPlaying:
            if time.time() - global_var.prev_time >= 1:
                global_var.played_time += 1
                if not global_var.isFalling:
                    if global_var.LEVEL != 4:
                        # falling count down
                        global_var.falling_time += 1
                        if global_var.falling_time == global_var.FALLING_TIME_LIMIT:
                            global_var.isFalling = True
                
                #spawn bullets
                if bar_player.isShoot:
                    half = int(bar_player.width/2)
                    new_bullet = bullet.Bullet(bar_player.x_pos + half , bar_player.y_pos-1 , 1 , 1)
                    bullet_array.append(new_bullet)
                
                #spaawn bombs
                if global_var.LEVEL == 4:
                    if global_var.UFO_BOMB_BUFFER == 0:
                        ufo_obj.drop_bomb(bomb_array)
                    
                    global_var.UFO_BOMB_BUFFER = (global_var.UFO_BOMB_BUFFER + 1)%4
                
                #gravity effect on poweups
                powerups.gravity_powerups(powerup_array)
                    
                global_var.prev_time = time.time()
            
            
                
        if global_var.LEVEL != 4:
            # clear level
            if bricks_left == 0:
                global_var.LEVEL += 1
                if global_var.LEVEL > 4:
                    won = 1
                    break
                    
                if global_var.LEVEL == 4:
                    ufo_obj = ufo.UFO(bar_player.x_pos - int(global_var.UFO_WIDTH/2) + int(bar_player.width/2), global_var.UFO_Y , global_var.UFO_WIDTH , global_var.UFO_HEIGHT)
                    ufo_obj.make()

                ret = util.level_cleared(ball_array , powerup_array , bullet_array , bomb_array)
                bar_player = ret[0]
                brick_grid = ret[1]
                global_var.isPlaying = False
                global_var.isFalling = False
                global_var.falling_time = 0
                reposition = "\033[{};{}H".format(global_var.WORLD_Y + global_var.HEIGHT +5 , 0)
                level_str = "\n\t\t\t\t\t\t\t\t\t\t\t  " + Back.WHITE + Fore.BLACK + Style.BRIGHT +  "LEVEL CLEARED!"
                print(reposition + level_str , end='')
                sleep(2)
                reset_str = "\n\t\t\t\t\t\t\t\t\t\t\t  " + Back.RESET + Fore.RESET  +  "              "
                print(reposition + reset_str , end='')
                continue
        
        else:
            if ufo_obj.health == 0:
                global_var.LEVEL += 1
                won = 1
                break
        
        #display time of shooting power
        if global_var.LEVEL != 4:
            if not bar_player.isShoot:
                reposition = "\033[{};{}H".format(global_var.WORLD_Y + global_var.HEIGHT +6 , 0)
                power_str = "\n\t\t\t\t\t\t\t\t\t\t\t  " + Back.RESET + Fore.RESET
                time_str = ""
                time_len = len(time_str)
                str_left = 17 - time_len
                for i in range(str_left):
                    time_str += " "
                power_str += time_str
                print(reposition + power_str , end='')
            else:
                shoot_time_rem = powerups.check_shoot_time(powerup_array)
                reposition = "\033[{};{}H".format(global_var.WORLD_Y + global_var.HEIGHT +6 , 0)
                power_str = "\n\t\t\t\t\t\t\t\t\t\t\t  " + Back.RESET + Fore.WHITE
                time_str = "SHOOT POWER: {}".format(shoot_time_rem)
                time_len = len(time_str)
                str_left = 17 - time_len
                for i in range(str_left):
                    time_str += " "
                power_str += time_str
                print(reposition + power_str , end='')
        
        else:
            # display boss health bar
            reposition = "\033[{};{}H".format(global_var.WORLD_Y + global_var.HEIGHT +6 , 0)
            main_str = "\n\t\t\t\t\t\t\t\t\t\t\tHEALTH: {}".format(ufo_obj.health) + Back.WHITE + Fore.BLACK
            health_bar = "-"*ufo_obj.health
            health_len = len(health_bar)
            str_left = global_var.UFO_HEALTH+8 - health_len
            for i in range(str_left):
                health_bar += (Back.RESET + Fore.RESET + " ")
            main_str += health_bar
            print(reposition + main_str , end='')



        if not global_var.isFalling:
            print("\033[%d;%dH"%(global_var.WORLD_Y + global_var.HEIGHT +7 , 0))
            print("\n\t\t\t\t\t\t\t\t\t\t\t  " + Back.RESET + Fore.RESET  +  "        ")
        else:
            print("\033[%d;%dH"%(global_var.WORLD_Y + global_var.HEIGHT +7 , 0))
            print("\n\t\t\t\t\t\t\t\t\t\t\t  " + Back.WHITE + Fore.BLACK + Style.BRIGHT +  "FALLING!")

        #display stats
        reposition = "\033[{};{}H".format(global_var.WORLD_Y + global_var.HEIGHT +1 , 0)
        welcome = "\t\t\t\t\t\t\t\t\t\t   WELCOME TO BRICK BREAKER"
        time_lives = "\t\t\t\t\t\t\t\t\t       Lives: {}   Time: {} seconds played".format(global_var.LIVES , global_var.played_time)
        bricks = "\t\t\t\t\t\t\t\t\t     Bricks broken:{}   Bricks Remaining:{} ".format(bricks_broken , bricks_left)
        scores = "\t\t\t\t\t\t\t\t\t\t        Level:{}  SCORE:{} ".format(global_var.LEVEL,global_var.SCORE)
        print(reposition + welcome + '\n' + time_lives + '\n' +  bricks + '\n' + scores , end='')
        
        # REFRESH WITH UPDATED STATE AND RENDER
        sys.stdin.flush()
        sys.stdout.flush()
        util.set_canvas(game_world , brick_grid, bar_player , ball_array , powerup_array , bullet_array , bomb_array)
        if global_var.LEVEL == 4:
            ufo_obj.set_on_canvas(game_world)
        game_world.draw_canvas()



    if won:
        print("\n\t\t\t\t\t\t\t\t\t\t\t    " + Back.WHITE + Fore.GREEN + Style.BRIGHT +  "YOU WIN!")
        sleep(2)
        util.clear()
    else:
        if global_var.LIVES > 0:
            break
        
        print("\n\t\t\t\t\t\t\t\t\t\t\t    " + Back.WHITE + Fore.RED + Style.BRIGHT +  "YOU LOSE!")
        sleep(2)
        util.clear()



print("\033[%d;%dH" % (global_var.WORLD_Y + global_var.HEIGHT + 10 , 0))

# redisplaying cursor and turning echo mode back on
system("stty echo")
sys.stdout.write("\033[?25h")
sys.stdout.flush()

        
        

