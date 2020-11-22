import pygame

from game_variables import *
from game_sprites import *

pygame.init()

gbl_display_x = screenWidth
gbl_display_y = screenHeight

bx = int((75/800)*gbl_display_x)
by = int((75/600)*gbl_display_y)

def random_generator(letters, x_c = 8, y_c = 6, margin_x = 0, margin_y = 0):
    rand = list()
    for y in range(y_c):
        line = ''
        
        if y < margin_y or y > y_c - margin_y-1:
            line = ' ' * x_c
        
        else:
            for x in range(x_c):
            
                if x < margin_x or x > x_c - margin_x-1:
                    line += ' '
                
                else:
                    line += (str(random.choice(letters)))
            
        rand.append(line)
    
    return rand
        
def block_translator(block_params):
    if block_params[0] == 'Block':
        return BlockBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        seed = block_params[5])
    elif block_params[0] == 'Subtract':
        return SubtracBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        seed = block_params[5])
    elif block_params[0] == 'Mythic':
        return MythicBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        seed = block_params[5])
    elif block_params[0] == 'Sync':
        return SyncBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        sync_len = block_params[5],
                        switch = True if block_params[6] == None else block_params[6],
                        seed = block_params[7])
    elif block_params[0] == 'Jac':
        return JacBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        jac_num = block_params[5],
                        seed = block_params[6])
    elif block_params[0] == 'Crac':
        return CracBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        sync_len = block_params[5],
                        sync_ctr = block_params[6],
                        switch = True if block_params[7] == None else block_params[7],
                        seed = block_params[8])
    elif block_params[0] == 'Tic':
        return TicBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        wait_tic = block_params[5],
                        add_tic = block_params[6],
                        switch = True if block_params[7] == None else block_params[7],
                        seed = block_params[8])
    elif block_params[0] == 'Nic':
        return NicBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        seed = block_params[5]
                        )
    elif block_params[0] == 'Sniq':
        return SniqBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        move_tic = block_params[5],
                        switch = block_params[6],
                        seed = block_params[7])
    elif block_params[0] == 'Shuq':
        return ShuqBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        seed = block_params[5])
    elif block_params[0] == 'Mock':
        return MockBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = 6 if block_params[4] == None else block_params[4],
                        sync_len = block_params[5],
                        switch = 0 if block_params[6] == None else block_params[6],
                        seed = block_params[7],
                        mode = 0 if block_params[8] == None else block_params[8],)
        
def block_gen_classic(pos, stage = None, phase = None, array_loc = None):

    if stage == None:
        stage = random.randint(0,len(classic_layouts))

    def classic():
        x = classic_layouts[stage]['phases'][phase]['blocks'][\
                                                      classic_layouts[stage]['phases'][phase]['grid'][array_loc[1]][array_loc[0]]
                                                      ]
        
        if x != None:
            x = block_translator(x)

            x.rect.topleft = pos
        
        return x
    
    return classic()
    
##### Classic Layouts ##############################

classic_test = None
#ARRAYS START AT 0

classic_layouts = list()

''' 
BLOCK TYPES:

#ALL CAPSLOCK ACCEPTS ~None~ VALUE

------------------------
('Block',    place,    size,    border_thickness,    DIFFICULTY(1~100),    SEED(1~9))  

== normal blue blocks 
== divisible by user input
('Block',    (0,0),    (bx,by),    5,    20,    None),

------------------------
('Subtract',    place,    size,    border_thickness,    DIFFICULTY(1~100),    SEED(1~9))  

== orange blocks 
== subtracts from user input
('Subtract',    (0,0),    (bx,by),    5,    None,    None),

------------------------
('Mythic',    place,    size,    border_thickness,    DIFFICULTY(1~100),    SEED(1~9))  

== violet blocks 
== subtracts from user input
('Mythic',    (0,0),    (bx,by),    5,    None,    None),

------------------------
('Sync',    place,    size,    border_thickness,    DIFFICULTY(1~100),    ON-OFF TIMER,    ON-OFF-START,    SEED(1~9))  

== yellow blocks 
== turns off and on during game
('Sync',    (0,0),    (bx,by),    5,    None,    3000,    True,    None),

------------------------
('Jac',    place,    size,    border_thickness,    DIFFICULTY(1~100),    JACNUM(1~9),    SEED(1~9))  

== violet blocks 
== suddenly becomes invisible under circumstances
('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),

------------------------
('Crac',    place,    size,    border_thickness,    DIFFICULTY(1~100),    BLUE/RED-TIMER,    BLOCK-BREAKER,    BLUE/RED-SWITCH,    SEED(1~9))  

== blue/red blocks 
== divides if it is color blue/multiplies if it is color red
('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),

------------------------
('Tic',    place,    size,    border_thickness,    DIFFICULTY(1~100),    WAIT-TIMER,    ADD-DELAY,    ADD-SWITCH,    SEED(1~9))  

== white/navy_green blocks 
== multiplies automatically if not dealt with quickly
('Tic',    (0,0),    (bx,by),    5,    20,    2000,    100,    True,    None),

------------------------
('Nic',    place,    size,    border_thickness,    DIFFICULTY(1~100),    SEED(1~9))  

== yellow/green blocks
== divides if input is right/multiplies if input is wrong
('Nic',    (0,0),    (bx,by),    5,    20,    None),

------------------------
('Sniq',    place,    size,    border_thickness,    DIFFICULTY(1~100),    MOVE-SPEED(1~20 => higher=faster),    MOVE-SWITCH,    SEED(1~9))  

== sky blue blocks
== moves on the screen
('Sniq',    (0,0),    (bx,by),    5,    20,    200,    True,    None),

------------------------
('Shuq',    place,    size,    border_thickness,    DIFFICULTY(1~100),    SEED(1~9))  

== light purple block
== shows random number everytime
('Shuq',    (0,0),    (bx,by),    5,    20,    None),

------------------------
('Mock',    place,    size,    border_thickness,    DIFFICULTY(1~100),    SWITCH-TIMER,    CURRENT-MODE,    SEED(1~9),    MODE(IGNORE THIS))  

    0    1    2    3
== blue/red/orange/white
== divide/multiply/subtract/add
('Mock',    (0,0),    (bx,by),    5,    3000,    1,    None,    None,    None),

'''



classic_layouts.append(
    {
    'title' : "Blue Boxes",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Another easy level",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Level Eater",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Block',(0,0),(bx,by),5,2,None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Subtractor",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Negative Actions",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })


classic_layouts.append(
    {
    'title' : "Purple Clicks",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "2357 cuz you know",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "You don't own me!",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Sync',    (0,0),    (bx,by),    5,    None,    3000,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Sync',    (0,0),    (bx,by),    5,    None,    3000,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Sync',    (0,0),    (bx,by),    5,    None,    3000,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Sync',    (0,0),    (bx,by),    5,    None,    3000,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Blinkers",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Sync',    (0,0),    (bx,by),    5,    None,    3000,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Sync',    (0,0),    (bx,by),    5,    None,    3000,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Sync',    (0,0),    (bx,by),    5,    None,    3000,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Sync',    (0,0),    (bx,by),    5,    None,    3000,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })


classic_layouts.append(
    {
    'title' : "Error Loading",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "<insert title here>",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Just another level",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Tickers",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Tic',    (0,0),    (bx,by),    5,    20,    2000,    100,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Tic',    (0,0),    (bx,by),    5,    20,    2000,    100,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Tic',    (0,0),    (bx,by),    5,    20,    2000,    100,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Tic',    (0,0),    (bx,by),    5,    20,    2000,    100,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Impatient Bastards",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Tic',    (0,0),    (bx,by),    5,    20,    2000,    100,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Tic',    (0,0),    (bx,by),    5,    20,    2000,    100,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Tic',    (0,0),    (bx,by),    5,    20,    2000,    100,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Tic',    (0,0),    (bx,by),    5,    20,    2000,    100,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Not waiting for you",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Nic',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Nic',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Nic',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Nic',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "No sense to be here",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Sniq',    (0,0),    (bx,by),    5,    20,    200,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Sniq',    (0,0),    (bx,by),    5,    20,    200,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Sniq',    (0,0),    (bx,by),    5,    20,    200,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Sniq',    (0,0),    (bx,by),    5,    20,    200,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Sniqity Sniq",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Sniq',    (0,0),    (bx,by),    5,    20,    200,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Sniq',    (0,0),    (bx,by),    5,    20,    200,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Sniq',    (0,0),    (bx,by),    5,    20,    200,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Sniq',    (0,0),    (bx,by),    5,    20,    200,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Hard Negotiations",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Shuq',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Shuq',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Shuq',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Shuq',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Liar",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                2: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                3: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                4: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Guess Who",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                2: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                3: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                4: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "The secret league",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                2: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                3: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                4: {'blocks': {'a' : ('Mythic',    (0,0),    (bx,by),    5,    None,    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Two Jacs",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                2: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                3: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                4: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3),    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Someone's not going",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3,5,7),    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                2: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3,5,7),    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                3: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3,5,7),    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                4: {'blocks': {'a' : ('Jac',    (0,0),    (bx,by),    5,    None,    (2,3,5,7),    None),
                               'b' : ('Jac',    (0,0),    (bx,by),    5,    None,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "More bitchin",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Nic',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                2: {'blocks': {'a' : ('Nic',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                3: {'blocks': {'a' : ('Nic',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                4: {'blocks': {'a' : ('Nic',    (0,0),    (bx,by),    5,    20,    None),
                               'b' : ('Crac',    (0,0),    (bx,by),    5,    None,      1500,     10,    True,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a','b') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Crunchin Numbers",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Subtract',    (0,0),    (bx,by),    5,    20,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })

classic_layouts.append(
    {
    'title' : "Level Ender",
    'time'  : 15,
    'phases': {
                1: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    1,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                2: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    1,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                3: {'blocks': {'a' : ('Block',    (0,0),    (bx,by),    5,    1,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                4: {'blocks': {'a' : ('Mock',    (0,0),    (bx,by),    5,    3,     3000,    4,    None,    None,    None),
                               ' ': None},
                    'grid'  : (random_generator( ('a') ))},
                
                
            }
        
    })