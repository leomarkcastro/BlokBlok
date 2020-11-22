import pygame
import os
import json

all_block = 1


repeat_protection = 5
trans_speed = 2
autoplay_delay = 100

pygame.init()

game_folder = os.path.dirname(__file__)   

#Load JSON
def json_load(file = 'blokblok.json'):
    try:
        with open(file, "r") as read_file:
            savedict = json.load(read_file)
        return savedict
    
    except:
        if file == 'blokblok.json':
            savedict = {
                'continue': None,
                'level': 1,
                'endless': 0,
                'classic': 0,
                'idle': 0,
                'blackout': 0,
                'first': True
                }
            
            with open(file, "w+") as write_file:
                json.dump(savedict, write_file)
                
            return savedict
        
        elif file == 'settings.json':
            savedict = {
                'screen_w': 800,
                'screen_h': 600,
                'fullscreen': False,
                'stretch': False,
                'music': True,
                'sound': True
                
                }
            
            with open(file, "w+") as write_file:
                json.dump(savedict, write_file)
                
            return savedict

#Save JSON
def json_save(savedict, file = os.path.join(game_folder, 'blokblok.json')):      
    with open(file, "w+") as write_file:
            json.dump(savedict, write_file)  
        

#############################################################
#Try to put all the variables used in the game here
#############################################################

#Colors

white = (255,255,255)
gray = (128,128,128)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
yellow = (255,255,0)
violet = (255,0,255)
block_color = (0,0,42)
sync_color = (42,42,0)
subtrac_color = (26,26,0)
mythic_color = (42,0,42)
crac_color = (0,0,42)
crac_color_2 = (42,0,0)
jac_color = (0,42,0)
tic_color = (32,32,32)
tic_color_2 = (0,16,16)
nic_color = (26,25,1)
nic_color_2 = (25,0,0)
sniq_color = (16,60,42)
shuq_color = (32,8,18)
mock_color = (0,0,42)
mock_color_2 = (42,0,0)
mock_color_3 = (34,26,0)
mock_color_4 = (25,25,25)

#Loading Screen Guides

loading_cues = (
    "When in doubt, spam the 2 3 5 7 buttons",
    "The strategy in this game is to SPAM",
    "Blue Blocks divide when you put number",
    "Orange Blocks subtract instead",
    "Purple Blocks likes to keep secrets",
    "Be punctual dealing with Yellow Blocks",
    "Red Blocks multiply, stupid block",
    "You could sometimes harass red blocks",
    "Red blocks will break if you harass them",
    "Green Blocks have 1 of two forms",
    "Sometimes, Green Blocks suddenly vanish",
    "Green Block hides when they are too low",
    "Some Green Blocks hide when it contains...",
    "green blocks ...factors of certain number",
    "Gray Blocks turn navy green when ignored",
    "Gray Blocks are impatient",
    "Gray Blok multiply itself to gain atention",
    "Mustard Box are nerds, hates wrong answers",
    "Mustard Box multiplies when inputted wrong",
    "Skyblue Box moves, eating away some RAM",
    "The dark weird purple block is weird",
    "Dark purple block reinitialize when held",
    "There is an Avatar Block, has 4 behaviors",
    "The avatar block is the hardest block",
    "Press F1 to turn AutoClick in any game",
    "Someone left the fridge open",
    "<insert your shit here>",
    'Thanks Neil for the Art!',
    "I did this shit for almost a month",
    "I want to put an audio_vis in main menu",
    "Mark! Tapusin mo na yung Classic Level",
    "Yey!!! Exempted from finals!!!",
    "BG Main Menu: Your Love (Frankie Knuckles)",
    'Ganda ni ano ________',
    'Putek, binabasa mo to?',
    '177063',
    "I hand hold you through out the game",
    "The avatar block knows the 4 math ops",
    "Having a hard time? Press F1 when playing",
    "This game is a mess, just like its coder",
    "This game tries hard to be a complete game",
    "Please Maam Ena iperfect niyo to!",
    "Gusto ko ng pancit cantutan",
    "Irritated by sounds, turn it off in settings",
    "The music used in this game is illegal",
    "OST from Kakegrurui and Gran Turismo",
    "This game was inspired by Block Breaker",
    "Ang dami ko pa dapat gawin sa laro na to",
    "Plok Plok and I'll reward you",
    "69 is the best",
    )

#Principal Pygame Variables


sdIxy = pygame.display.Info()

sdFullRatio = False
sdFull = False


settings = json_load('settings.json')
#print (settings)

screenWidth = int(sdIxy.current_w * 0.80) if settings['stretch'] else settings['screen_w']
screenHeight = int(sdIxy.current_h * 0.80) if settings['stretch'] else settings['screen_h']
display_flags = (pygame.FULLSCREEN|pygame.HWACCEL) if settings['fullscreen'] else 0 #(pygame.FULLSCREEN|pygame.HWACCEL) if sdFull else 0
#print (sdIxy.current_w, sdIxy.current_h)
screenCaption = 'Blok Blok'
fps = 60

game_pos = 32

trans = False
jac_trans = True
alpha_low = True
alpha_block = 220
alpha_game_block = 50

## Movement Variables
up = 1
right = 2
down = 3
left = 4
idle = 0

#Fonts

font_folder = os.path.join(game_folder, 'font')

font_array = {
    'webpixel' : os.path.join(font_folder, "webpixel bitmap_light.otf"),
    'agency' : os.path.join(font_folder, "AGENCYB.TTF"),
    'game_over': os.path.join(font_folder, "game_over.ttf"),
    'potra' : os.path.join(font_folder, "Potra.ttf")
    }

font_typo = {0: (font_array['webpixel'],60), 
             1:(font_array['agency'],50), 
             2:(font_array['game_over'],48),
             3:(font_array['potra'],85),
             4:(font_array['game_over'],100),
             5:(font_array['potra'],50),
             6:(font_array['game_over'],50),
             7:(font_array['game_over'],180),
             8: (font_array['webpixel'],18),
             9: (font_array['webpixel'],98), 
             10: (font_array['webpixel'],30),
             11:(font_array['potra'],60), 
             12:(font_array['potra'],25),
             13:(font_array['game_over'],50),
             15:(font_array['game_over'],150),
             14:(font_array['game_over'],120),
             16:(font_array['potra'],65),
             17: (font_array['webpixel'],20),}
font_color = {0: (black, white),
              1: (white, None),
              2: ((50,50,50),None),
              3: (black, None),
              4: ((200,0,0), None),
              5: ((1,1,1),None)}

#Global variables

score = 0
game_time = 20


############################################################# 
#FUNCTIONS
#############################################################

#Text Display Function

def textdisplay(message, color, fontset):
    font = pygame.font.Font(fontset[0],fontset[1])
    text = font.render(message, True, color[0], color[1])
    textRect = text.get_rect()
    
    return text,textRect
