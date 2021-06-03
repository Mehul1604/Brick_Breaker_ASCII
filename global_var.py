import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


HEIGHT = 40
WIDTH = 90
WORLD_X = 50
WORLD_Y = 0
INF = 999999999



LEVEL = 1
LIVES = 8

BRICK_LEFT = WORLD_X+5
BRICK_UP = WORLD_Y+4
BRICK_WIDTH = 5
BRICK_HEIGHT = 2
BRICK_ROW = 16

BRICKS_FELL = False

isPlaying = False
prev_time = 0.0
played_time = 0

FALLING_TIME_LIMIT = 30
falling_time = 0
isFalling = False

POWERUP_DURATION = 15
GROW_BAR = 'GB'
SHRINK_BAR = 'SB'
STICKY_BAR = 'ST'
FAST_BALL = 'FB'
THRU_BALL = 'TB'
MULTI_BALL = 'MB'
SHOOT_BAR = 'SH'
POWERUP_TYPES = [SHOOT_BAR]
GROW_BAR_SYM = '+'
SHRINK_BAR_SYM = '-'
STICKY_BAR_SYM = 'S'
FAST_BALL_SYM = '^'
THRU_BALL_SYM = 'T'
MULTI_BALL_SYM = '8'
SHOOT_BAR_SYM = 'H'
GROW_BAR_COL = Back.LIGHTWHITE_EX + Fore.GREEN
SHRINK_BAR_COL = Back.RED + Fore.WHITE + Style.BRIGHT
STICKY_BAR_COL = Back.BLUE + Fore.RED + Style.BRIGHT
FAST_BALL_COL = Back.YELLOW + Fore.RED + Style.BRIGHT
THRU_BALL_COL = Back.MAGENTA + Fore.YELLOW + Style.BRIGHT
MULTI_BALL_COL = Back.WHITE + Fore.BLACK + Style.BRIGHT
SHOOT_BAR_COL = Back.LIGHTBLACK_EX + Fore.WHITE + Style.BRIGHT

# Object class - Bar , Ball , Brick
class Object:
    def __init__(self , x , y , width , height):
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
    
    def make(self):
        pass
    
    def set_on_canvas(self):
        pass

UFO_ARR = []
UFO_HEALTH = 12
UFO_BOMB_BUFFER = 0
UFO_WIDTH = 0
UFO_HEIGHT = 0
UFO_Y = 2
f_ufo = open('./ufo.txt' , 'r')
rows = f_ufo.readlines()
for r in rows:
    UFO_HEIGHT += 1
    arr_row = []
    for c in r:
        if c != '\n':
            arr_row.append(c)

    UFO_WIDTH = max(UFO_WIDTH , len(arr_row))

    UFO_ARR.append(arr_row)

SCORE = 0