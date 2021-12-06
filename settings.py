width = 480
height = 600
FPS = 60
title = "Jumpin' Plats"
hs_file = "highscore.txt"
spritesheet = "spritesheet_jumper.png"
cn_file = "snd.txt"

# Player properties
player_acc = 0.5
player_friction = -0.12
player_grav = 0.8
player_jump = 23

# Game properties
BOOST_POWER = 30
pow_spawn_pct = 7
coin_spawn_pct = 3
mob_freq = 4500
player_layer = 2
platform_layer = 1
mob_layer = 2
powerup_layer = 1
cloud_layer = 0
coins_layer = 1
# Starting platforms
Platform_list = [(0, 550),
                 (190, 360),
                 (125, 250),
                 (350, 200),
                 (175, 100)
                 ]
font_name = "freesansbold.ttf"
# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 200, 255)
yellow = (252, 255, 0)
bgcolor1 = (0, 180, 255)
bgcolor2 = (29, 172, 184)
