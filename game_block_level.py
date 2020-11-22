import pygame

from game_variables import *
from game_sprites import *

pygame.init()

gbl_display_x = screenWidth
gbl_display_y = screenHeight

difficulty = 1

def change_dif(mode = 'increase'):
    global difficulty
    if mode == 'increase':
        difficulty *= 1.2
    elif mode == 'reset':
        difficulty = 1

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
        global difficulty
        return BlockBox(block_params[1], 
                        block_params[2], 
                        width = (0 if block_params[3] == None else block_params[3]), 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        seed = block_params[5])
    elif block_params[0] == 'Subtract':
        return SubtracBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        seed = block_params[5])
    elif block_params[0] == 'Mythic':
        return MythicBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        seed = block_params[5])
    elif block_params[0] == 'Sync':
        return SyncBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        sync_len = block_params[5],
                        switch = True if block_params[6] == None else block_params[6],
                        seed = block_params[7])
    elif block_params[0] == 'Jac':
        return JacBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        jac_num = block_params[5],
                        seed = block_params[6])
    elif block_params[0] == 'Crac':
        return CracBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        sync_len = block_params[5],
                        sync_ctr = block_params[6],
                        switch = True if block_params[7] == None else block_params[7],
                        seed = block_params[8])
    elif block_params[0] == 'Tic':
        return TicBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        wait_tic = block_params[5],
                        add_tic = block_params[6],
                        switch = True if block_params[7] == None else block_params[7],
                        seed = block_params[8])
    elif block_params[0] == 'Nic':
        return NicBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        seed = block_params[5]
                        )
    elif block_params[0] == 'Sniq':
        return SniqBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        move_tic = block_params[5],
                        switch = block_params[6],
                        seed = block_params[7])
    elif block_params[0] == 'Shuq':
        return ShuqBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        seed = block_params[5])
    elif block_params[0] == 'Mock':
        return MockBox(block_params[1], 
                        block_params[2], 
                        width = 0 if block_params[3] == None else block_params[3], 
                        level = int((6 if block_params[4] == None else block_params[4]) // difficulty),
                        sync_len = block_params[5],
                        switch = 0 if block_params[6] == None else block_params[6],
                        seed = block_params[7],
                        mode = 0 if block_params[8] == None else block_params[8],)
        
def block_gen(pos, level = None, stage = 1, phase = None, array_loc = None):

    def endless(stage):
        if stage > (12*2)-1: 
            r = random.randrange(stage//12%12,12+1)
        
        else:
            stage //= 2
            r = random.randrange(1,stage+1+1)  
        
        if r == 1: x = (BlockBox((pos[0],pos[1]),(bx,by),5))   
        elif r == 2: x = (SubtracBox((pos[0],pos[1]),(bx,by),5))  
        elif r == 3: x = (MythicBox((pos[0],pos[1]),(bx,by),5))  
        elif r == 4: x = (SyncBox((pos[0],pos[1]),(bx,by),5))   
        elif r == 5: x = (JacBox((pos[0],pos[1]),(bx,by),5)) 
        elif r == 6: x = (CracBox((pos[0],pos[1]),(bx,by),5)) 
        elif r == 7: x = (DrawBox((pos[0],pos[1]),(bx,by),5)) 
        elif r == 8: x = (NicBox((pos[0],pos[1]),(bx,by),5)) 
        elif r == 9: x = (TicBox((pos[0],pos[1]),(bx,by),5)) 
        elif r == 10: x = (SniqBox((pos[0],pos[1]),(bx,by),5)) 
        elif r == 11: x = (ShuqBox((pos[0],pos[1]),(bx,by),5)) 
        elif r == 12: x = (MockBox((pos[0],pos[1]),(bx,by),5)) 
        
        return x
    
    def story():
        x = stage_layouts[level][stage][phase][0][\
                                                  stage_layouts[level][stage][phase][1][array_loc[1]][array_loc[0]]
                                                  ]
        
        if x != None:
            x = block_translator(x)

            x.rect.topleft = pos
        
        return x
    
    if level == None:
        return endless(stage)
    else:
        return story()
    
##### Stage Layouts ##############################

stage_layouts = dict()


###Club##############

def stage_club_levels():
    
    club_level = {
        ###############Start###################
        
        ###  Level 1  ####
        1: {
            1 : ({'a' : ('Block',(0,0),(bx,by),5,2,None),
                 ' ': None},
                ('  aaaa  ',
                 '      a ',
                 '     a  ',
                 '    a   ',
                 '   a    ',
                 '  aaaaa ',)),
            2 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Block',(0,0),(bx,by),5,1,None),
                 ' ': None},
                ('        ',
                 ' aaaaaa ',
                 ' abbbba ',
                 ' abbbba ',
                 ' aaaaaa ',
                 '        ',)),
            3 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Block',(0,0),(bx,by),5,10,None),
                 ' ': None},
                (' aa  aa ',
                 ' aa  aa ',
                 '   bb   ',
                 'b  bb  b',
                 ' b    b ',
                 '  bbbb  ',)),
            4 : ({'a' : ('Block',(0,0),(bx,by),5,10,None),
                 ' ': None},
                ('  a     ',
                 ' a a a  ',
                 'a   a   ',
                 '   a a  ',
                 '  a   a ',
                 '       a',)),
            
            },
        
        ###  Level 2  ####
        
        2: {
            1 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                 ' ': None},
                ('aaaaa   ',
                 'aaaaa   ',
                 '   aa   ',
                 '   aa   ',
                 '   aaaaa',
                 '   aaaaa',)),
            2 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                 ' ': None},
                ('        ',
                 '        ',
                 '  bbbb  ',
                 '  bbbb  ',
                 '        ',
                 '        ',)),
            3 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                 ' ': None},
                ('        ',
                 ' aaaaaa ',
                 ' bbbbbb ',
                 ' aaaaaa ',
                 ' bbbbbb ',
                 '        ',)),
            4 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                 ' ': None},
                ('   a    ',
                 '  bab   ',
                 'aaaabbb ',
                 ' bbbaaaa',
                 '   babb ',
                 '    a   ',)),
            },
        
        ###  Level 3  ####
        
        3: {
            1 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                 ' ': None},
                ('ba  b  a',
                 'abab ba ',
                 '  ba ab ',
                 'ab ba  b',
                 'ba abab ',
                 '  a  ba ',)),
            2 : ({'a' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                 ' ': None},
                ('        ',
                 ' aaaaaa ',
                 ' a    a ',
                 ' a    a ',
                 ' aaaaaa ',
                 '        ',)),
            3 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,None,None),
                 ' ': None},
                ('aaaaaaaa',
                 'acccccca',
                 'acbbbbca',
                 'acbbbbca',
                 'acccccca',
                 'aaaaaaaa',)),
            4 : ({'a' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'b' : ('Mythic',(0,0),(bx,by),5,8,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,11,None),
                 ' ': None},
                ('aaaaaaaa',
                 'abbbbbba',
                 'abbccbba',
                 'abbccbba',
                 'abbbbbba',
                 'aaaaaaaa',)),
            },
        
        ###  Level 4  ####
        
        4: {
            1 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,None,None),
                 ' ': None},
                (
                    random_generator( ('a','b','c') ) 
                )),
            2 : ({'a' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,10,None),
                 ' ': None},
                ('bbbbbbbb',
                 'baaaaaab',
                 'baaaaaab',
                 'abbbbbba',
                 'abbbbbba',
                 'aaaaaaaa',)),
            3 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Sync',(0,0),(bx,by),5,None,1500,None,None),
                 ' ': None},
                ('        ',
                 ' aaaaaa ',
                 ' abbbba ',
                 ' abbbba ',
                 ' aaaaaa ',
                 '        ',)),
            4 : ({'a' : ('Sync',(0,0),(bx,by),5,5,1000,None,None),
                  'b' : ('Sync',(0,0),(bx,by),5,10,2000,None,None),
                  'c' : ('Sync',(0,0),(bx,by),5,15,3000,None,None),
                 ' ': None},
                ('aaaaaaaa',
                 'abbbbbba',
                 'abbccbba',
                 'abbccbba',
                 'abbbbbba',
                 'aaaaaaaa',)),
            },
        
        ###  Level 5  ####
        
        5: {
            1 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'd' : ('Sync',(0,0),(bx,by),5,None,None,None,None),
                 ' ': None},
                (
                    random_generator( ('a','b','c','d'), margin_y = 1 ) 
                )),
            2 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'd' : ('Sync',(0,0),(bx,by),5,None,None,None,None),
                 ' ': None},
                ('dabcacbd',
                 'dabcacbd',
                 'dabbacbd',
                 'dcabccbd',
                 'dcabcabd',
                 'dcabcabd',)),
            3 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'd' : ('Sync',(0,0),(bx,by),5,None,None,None,None),
                 ' ': None},
                (
                    random_generator( ('a','b','c','d') ) 
                )),
            4 : ({'a' : ('Sync',(0,0),(bx,by),5,15,3000,None,None),
                  'b' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'c' : ('Sync',(0,0),(bx,by),5,15,3000,None,None),
                  'd' : ('Sync',(0,0),(bx,by),5,15,4000,None,None),
                 ' ': None},
                (
                    random_generator( ('a','b','c','d') ) 
                )),
            },
        
        ###  Level 6  ####
        
        6: {
            1 : ({'a' : ('Jac',(0,0),(bx,by),5, None, None,None),
                 ' ': None},
                ('        ',
                 '        ',
                 '  aaaa  ',
                 '  aaaa  ',
                 '        ',
                 '        ',)),
            2 : ({'a' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'b' : ('Jac',(0,0),(bx,by),5,None, None,None),
                 ' ': None},
                (' aaaaaa ',
                 'a  bb  a',
                 'abbbbbba',
                 'abbbbbba',
                 'a  bb  a',
                 ' aaaaaa ',)),
            3 : ({'a' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'b' : ('Jac',(0,0),(bx,by),5,None, None,None),
                 ' ': None},
                (
                    random_generator( ('a','b') ) 
                )),
            4 : ({'a' : ('Sync',(0,0),(bx,by),5,15,5000,None,None),
                  'b' : ('Jac',(0,0),(bx,by),5,None,None,None),
                  'c' : ('Subtract',(0,0),(bx,by),5,None,None),
                 ' ': None},
                (' bbb  aa',
                 'bbbbb aa',
                 'bbbbb   ',
                 'bbccbb  ',
                 '  cc    ',
                 '  cc    ',)),
            },
        
        ###  Level 7  ####
        
        7: {
            1 : ({'a' : ('Crac',(0,0),(bx,by),5, None, 1500, 10,None,None),
                 ' ': None},
                ('        ',
                 '        ',
                 '   aa   ',
                 '   aa   ',
                 '        ',
                 '        ',)),
            2 : ({'b' : ('Block',(0,0),(bx,by),5,None,None),
                  'a' : ('Crac',(0,0),(bx,by),5, None, 3000, 10,None,None),
                 ' ': None},
                (' a    a ',
                 '  a  a  ',
                 '   aa   ',
                 '   aa   ',
                 '  a  a  ',
                 ' a    a ',)),
            3 : ({'b' : ('Block',(0,0),(bx,by),5,None,None),
                  'a' : ('Crac',(0,0),(bx,by),5, None, 3000, 10,None,None),
                 ' ': None},
                ('a  bb  a',
                 '   bb   ',
                 '  b  b  ',
                 '  b  b  ',
                 '   bb   ',
                 'a  bb  a',)),
            4 : ({'a' : ('Sync',(0,0),(bx,by),5,15,2500,False,None),
                  'b' : ('Crac',(0,0),(bx,by),5,15,5000,10,True,None),
                 ' ': None},
                (' aaaaaa ',
                 ' aaaaaa ',
                 ' aa  aa ',
                 '   bb   ',
                 ' bbbbbb ',
                 ' bbbbbb ',)),
            },
        
        ###  Level 8  ####
        
        8: {
            1 : ({'b' : ('Subtract',(0,0),(bx,by),5,15,None),
                  'd' : ('Sync',(0,0),(bx,by),5,None,1500,None,None),
                 ' ': None},
                ('bbbbbbbb',
                 'b  dd  b',
                 'b dddd b',
                 'b dddd b',
                 'b  dd  b',
                 'bbbbbbbb',)),
            2 : ({'a' : ('Sync',(0,0),(bx,by),5,None,1500,None,None),
                  'b' : ('Sync',(0,0),(bx,by),5,15,3000,None,None),
                  'c' : ('Sync',(0,0),(bx,by),5,None,2000,None,None),
                  'd' : ('Sync',(0,0),(bx,by),5,15,4000,None,None),
                  'e' : ('Sync',(0,0),(bx,by),5,20,12000,None,None),
                  'f' : ('Sync',(0,0),(bx,by),5,20,15000,None,None),
                 ' ': None},
                ('bbbacddd',
                 'bbbacddd',
                 'aaaacccc',
                 'eeeeffff',
                 'ffeeeeff',
                 'ffffeeee',)),
            3 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'd' : ('Sync',(0,0),(bx,by),5,None,None,None,None),
                  'd' : ('Crac',(0,0),(bx,by),5,15,5000,10,True,None),
                  'e' : ('Jac',(0,0),(bx,by),5,None,None,None),
                 ' ': None},
                (
                    random_generator( ('a','b','c','d','e') ) 
                )),
            4 : ({'a' : ('Sync',(0,0),(bx,by),5,20,7000,False,None),
                  'b' : ('Crac',(0,0),(bx,by),5,15,1000,15,True,None),
                 ' ': None},
                ('bbbbbbbb',
                 'baaaaaba',
                 'babbaaba',
                 'baaabbba',
                 'babbbbba',
                 'aaaaaaaa',)),
            5 : ({'a' : ('Sync',(0,0),(bx,by),5,15,15000,True,None),
                  'b' : ('Crac',(0,0),(bx,by),5,15,20000,5,False,None),
                 ' ': None},
                (' bbbbbb ',
                 'baaaaaab',
                 'babaabab',
                 ' baaaab ',
                 ' babbab ',
                 ' bbbbbb ',)),
            },
        
        ###############End###################
        }
    
    return club_level


stage_layouts[1] = stage_club_levels()

###Under##############

def stage_under_levels():
    under_level = {
        ###############Start###################
        
        ###  Level 1  ####
        1: {
            1 : ({'a' : ('Crac',(0,0),(bx,by),5,15,20000,5,False,None),
                  'b' : ('Crac',(0,0),(bx,by),5,15,20000,5,True,None),
                 ' ': None},
                ('   bb   ',
                 'aa bb   ',
                 'aaabbaa ',
                 'a  bb  a',
                 ' a    a ',
                 '  aaaa  ',)),
            2 : ({'a' : ('Block',(0,0),(bx,by),5,12,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,12,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,12,None),
                 ' ': None},
                ('baaaaacb',
                 'bccccacb',
                 'bcaaaabb',
                 'baaccbcc',
                 'ccaaabaa',
                 'bbbccbcc',)),
            3 : ({'a' : ('Sync',(0,0),(bx,by),5,15,5678,False,None),
                  'b' : ('Crac',(0,0),(bx,by),5,15,1234,5,False,None),
                 ' ': None},
                (' aa  aa ',
                 ' aa  aa ',
                 '   bb   ',
                 'b  bb  b',
                 ' b    b ',
                 '  bbbb  ',)),
            4 : ({'a' : ('Sync',(0,0),(bx,by),5,25,250,False,None),
                  'b' : ('Sync',(0,0),(bx,by),5,20,500,True,None),
                  'c' : ('Sync',(0,0),(bx,by),5,17,750,False,None),
                  'd' : ('Sync',(0,0),(bx,by),5,15,1000,True,None),
                  'e' : ('Sync',(0,0),(bx,by),5,10,2000,False,None),
                  'f' : ('Sync',(0,0),(bx,by),5,5,4000,True,None),
                 ' ': None},
                ('eeeeeeef',
                 'ecccccdf',
                 'ecaaabdf',
                 'ecbbbbdf',
                 'eddddddf',
                 'ffffffff',)),
            
            },
        
        ###  Level 2  ####
        
        2: {
            3 : ({'a' : ('Jac',(0,0),(bx,by),5,12,None,None),
                  'b' : ('Jac',(0,0),(bx,by),5,12,(5),(5,7)),
                 ' ': None},
                ('        ',
                 '  bbbb  ',
                 '  baab  ',
                 '  baab  ',
                 '  bbbb  ',
                 '        ',)),
            2 : ({'a' : ('Block',(0,0),(bx,by),5,10,None),
                  'b' : ('Jac',(0,0),(bx,by),5,12,(2),None),
                 ' ': None},
                ('bbbbbbbb',
                 'baaaaaab',
                 'babbbbab',
                 'babbbbab',
                 'baaaaaab',
                 'bbbbbbbb',)),
            1 : ({'a' : ('Block',(0,0),(bx,by),5,None,(5)),
                  'b' : ('Jac',(0,0),(bx,by),5,12,(5),(5,7)),
                 ' ': None},
                ('bbbaabbb',
                 'bbbaabbb',
                 'aaaaaaaa',
                 'aaaaaaaa',
                 'bbbaabbb',
                 'bbbaabbb',)),
            4 : ({'a' : ('Jac',(0,0),(bx,by),5,12,None,(2,3)),
                  'b' : ('Jac',(0,0),(bx,by),5,12,(3),(3,5)),
                  'c' : ('Jac',(0,0),(bx,by),5,12,(5),(5,7)),
                  'd' : ('Jac',(0,0),(bx,by),5,12,(7),(7,9)),
                 ' ': None},
                ('aaaacccc',
                 'aaaacccc',
                 'aaaacccc',
                 'ddddbbbb',
                 'ddddbbbb',
                 'ddddbbbb',)),
            },
        
        ###  Level 3  ####
        
        3: {
            1 : ({'b' : ('Sync',(0,0),(bx,by),5,None,1500,False,None),
                  'a' : ('Crac',(0,0),(bx,by),5,None,3000,30,False,None),
                 ' ': None},
                ('aaaaaaaa',
                 'abbbbbba',
                 'abbbbbba',
                 'abbbbbba',
                 'abbbbbba',
                 'aaaaaaaa',)),
            2 : ({'a' : ('Sync',(0,0),(bx,by),5,None,1500,True,None),
                  'b' : ('Crac',(0,0),(bx,by),5,None,3000,30,False,None),
                  'c' : ('Jac',(0,0),(bx,by),5,12,(5),None),
                  'd' : ('Jac',(0,0),(bx,by),5,12,(7),None),
                 ' ': None},
                ('bbbbdddd',
                 'baaadddd',
                 'baaadddd',
                 'ccccaaab',
                 'ccccaaab',
                 'ccccbbbb',)),
            4 : ({'a' : ('Sync',(0,0),(bx,by),5,7,1000,True,None),
                  'b' : ('Crac',(0,0),(bx,by),5,7,2000,30,True,None),
                  'c' : ('Jac',(0,0),(bx,by),5,12,(2),None),
                 ' ': None},
                ('cccccccc',
                 'caaaaaac',
                 'cbbbbbbc',
                 'cbbbbbbc',
                 'caaaaaac',
                 'cccccccc',)),
            3 : ({'a' : ('Sync',(0,0),(bx,by),5,7,10000,False,None),
                  'b' : ('Jac',(0,0),(bx,by),5,12,(2),None),
                 ' ': None},
                ('bbbbbbbb',
                 'aaaaaaaa',
                 'a a a a ',
                 ' a a a a',
                 'aaaaaaaa',
                 'bbbbbbbb',)),
            },
        
        ###  Level 4  ####
        
        4: {
            1 : ({'a' : ('Subtract',(0,0),(bx,by),5,12,None),
                  'b' : ('Mythic',(0,0),(bx,by),5,12,None),
                  'c' : ('Jac',(0,0),(bx,by),5,12,(2),None),
                 ' ': None},
                (random_generator( ('a','b','c') ) )),
            2 : ({'a' : ('Tic',(0,0),(bx,by),5,None,500,500,False,None),
                 ' ': None},
                ('        ',
                 '        ',
                 '  aaaa  ',
                 '  aaaa  ',
                 '        ',
                 '        ',)),
            3 : ({'a' : ('Tic',(0,0),(bx,by),5,None,2000,100,False,None),
                  'b' : ('Tic',(0,0),(bx,by),5,None,500,500,False,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,12,None),
                 ' ': None},
                ( random_generator( ('a','b','c') ) )),
            4 : ({'a' : ('Sync',(0,0),(bx,by),5,7,1500,False,None),
                  'b' : ('Tic',(0,0),(bx,by),5,None,500,500,False,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,12,None),
                 ' ': None},
                ('abababab',
                 'cbcacbca',
                 'cbcacbca',
                 'cbcacbca',
                 'cbcacbca',
                 'abababab',)),
            },
        
        ###  Level 5  ####
        
        5: {
            1 : ({'a' : ('Block',(0,0),(bx,by),5,12,(3,5)),
                  'b' : ('Block',(0,0),(bx,by),5,12,(5,7)),
                 ' ': None},
                (random_generator( ('a','b') ) )),
            2 : ({'a' : ('Block',(0,0),(bx,by),5,12,None),
                  'b' : ('Block',(0,0),(bx,by),5,12,None),
                  'c' : ('Crac',(0,0),(bx,by),5,7,3000,30,True,None),
                 ' ': None},
                (random_generator( ('a','b','c') ) )),
            3 : ({'a' : ('Block',(0,0),(bx,by),5,20,None),
                  'b' : ('Crac',(0,0),(bx,by),5,12,10000,30,True,None),
                  'c' : ('Crac',(0,0),(bx,by),5,15,5000,30,True,None),
                 ' ': None},
                (random_generator( ('a','b','c') ) )),
            4 : ({'a' : ('Jac',(0,0),(bx,by),5,20,(2),(2,3)),
                  'b' : ('Jac',(0,0),(bx,by),5,20,(2),(2,5)),
                  'c' : ('Jac',(0,0),(bx,by),5,20,(2),(2,7)),
                  'd' : ('Jac',(0,0),(bx,by),5,20,(3),(3,8)),
                 ' ': None},
                ('abababab',
                 'cbcacbca',
                 'cbcacbca',
                 'cbcacbca',
                 'cbcacbca',
                 'abababab',)),
            },
        
        ###  Level 6  ####
        
        6: {
            1 : ({'a' : ('Sync',(0,0),(bx,by),5,7,1500,False,None),
                  'b' : ('Sync',(0,0),(bx,by),5,7,2000,False,None),
                  'c' : ('Sync',(0,0),(bx,by),5,7,3500,False,None),
                 ' ': None},
                ('ccabbbbb',
                 'ccabbbbb',
                 'aaaaaaaa',
                 'bbaccccc',
                 'bbaccccc',
                 'bbaccccc',)),
            2 : ({'d' : ('Sniq',(0,0),(bx,by),5,14,1,None,None),
                  'a' : ('Sync',(0,0),(bx,by),5,7,1500,False,None),
                  'b' : ('Sync',(0,0),(bx,by),5,7,2000,False,None),
                  'c' : ('Sync',(0,0),(bx,by),5,7,3500,False,None),
                 ' ': None},
                ('dcdbbbbd',
                 'ccabbbbb',
                 'daaaaaad',
                 'bbaccccc',
                 'bbaccccc',
                 'dbdccccd',)),
            3 : ({'a' : ('Sniq',(0,0),(bx,by),5,14,1,None,None),
                 ' ': None},
                (random_generator( ('a') ) )),
            4 : ({'a' : ('Tic',(0,0),(bx,by),5,None,500,500,False,None),
                  'b' : ('Sniq',(0,0),(bx,by),5,14,1,None,None),
                 ' ': None},
                (random_generator( ('a','b') ) )),
            },
        
        ###  Level 7  ####
        
        7: {
            1 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'd' : ('Crac',(0,0),(bx,by),5,15,5000,10,True,None),
                  'g' : ('Sniq',(0,0),(bx,by),5,14,1,None,None),
                 ' ': None},
                (random_generator( ('a','d','g') ) )),
            2 : ({'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                  'd' : ('Sync',(0,0),(bx,by),5,None,None,None,None),
                  'e' : ('Jac',(0,0),(bx,by),5,None,None,None),
                 ' ': None},
                (random_generator( ('b','d','e') ) )),
            3 : ({'c' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'f' : ('Tic',(0,0),(bx,by),5,None,500,500,False,None),
                  'h' : ('Jac',(0,0),(bx,by),5,None,(2),None),
                 ' ': None},
                (random_generator( ('c','f','h') ) )),
            4 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Subtract',(0,0),(bx,by),5,None,None),
                  'c' : ('Mythic',(0,0),(bx,by),5,None,None),
                  'd' : ('Sync',(0,0),(bx,by),5,None,None,None,None),
                  'd' : ('Crac',(0,0),(bx,by),5,15,5000,10,True,None),
                  'e' : ('Jac',(0,0),(bx,by),5,None,None,None),
                  'f' : ('Tic',(0,0),(bx,by),5,None,500,500,False,None),
                  'g' : ('Sniq',(0,0),(bx,by),5,14,1,None,None),
                  'h' : ('Jac',(0,0),(bx,by),5,None,(2),None),
                 ' ': None},
                (random_generator( ('a','b','c','d','e','f','g') ) )),
            },
        
        
        ###  Level 8  ####
        
        8: {
            1 : ({'a' : ('Jac',(0,0),(bx,by),5,15,(2,3),(5,7,9)),
                  'b' : ('Sniq',(0,0),(bx,by),5,14,1,None,None),
                 ' ': None},
                ('b      b',
                 ' aaaaaa ',
                 ' ababaa ',
                 ' aababa ',
                 ' aaaaaa ',
                 'b      b',)),
            2 : ({'a' : ('Tic',(0,0),(bx,by),5,None,500,100,False,None),
                  'b' : ('Crac',(0,0),(bx,by),5,10,3000,10,True,None),
                 ' ': None},
                ('abbbbbbb',
                 'aabbbbaa',
                 'aaaabaaa',
                 'aaabbbaa',
                 'aabbbbba',
                 'bbbbbbba',)),
            3 : ({'a' : ('Tic',(0,0),(bx,by),5,10,500,100,True,None),
                  'b' : ('Crac',(0,0),(bx,by),5,10,3000,10,True,None),
                  'c' : ('Sync',(0,0),(bx,by),5,None,1000,False,None),
                  'd' : ('Jac',(0,0),(bx,by),5,15,(2,3),(5,7,9)),
                 ' ': None},
                ('cccccccc',
                 'bddddddb',
                 'bdaaaadb',
                 'bdaaaadb',
                 'bddddddb',
                 'cccccccc',)),
            4 : ({'b' : ('Subtract',(0,0),(bx,by),5,25,None),
                  'a' : ('Crac',(0,0),(bx,by),5,5,1500,10,True,None),
                  'g' : ('Sniq',(0,0),(bx,by),5,14,1,None,None),
                  'd' : ('Shuq',(0,0),(bx,by),5,30,None),
                 ' ': None},
                ('gggggggg',
                 'adddddda',
                 'adbbbbda',
                 'adbbbbda',
                 'adddddda',
                 'gggggggg',)),
            5 : ({'a' : ('Subtract',(0,0),(bx,by),5,45,None),
                  'b' : ('Sniq',(0,0),(bx,by),5,25,1,None,None),
                 ' ': None},
                (random_generator( ('a','b') ) )),
            },
        
        
        ###############End###################
        }
    
    return under_level


stage_layouts[2] = stage_under_levels()

###Crib Elite##############
    
def stage_crib_levels():
    crib_level = {
        ###############Start###################
        
        ###  Level 1  ####
        1: {
            1 : ({'a' : ('Tic',(0,0),(bx,by),5,None,100,50,False,(2,3)),
                  'b' : ('Tic',(0,0),(bx,by),5,None,1500,10,False,(5,7)),
                 ' ': None},
                ('bbbbbbbb',
                 'b      b',
                 'b aaaa b',
                 'b aaaa b',
                 'b      b',
                 'bbbbbbbb',)),
            2 : ({'a' : ('Sync',(0,0),(bx,by),5,25,500,False,None),
                  'b' : ('Sync',(0,0),(bx,by),5,25,500,True,None),
                 ' ': None},
                (' ababab ',
                 ' bababa ',
                 ' ababab ',
                 ' bababa ',
                 ' ababab ',
                 ' bababa ',)),
            3 : ({'a' : ('Crac',(0,0),(bx,by),5,None,500,90,False,None),
                  'b' : ('Crac',(0,0),(bx,by),5,None,10000,90,True,None),
                 ' ': None},
                ('  a     ',
                 ' aaa b  ',
                 'aaaaab  ',
                 '  abbbbb',
                 '  a bbb ',
                 '     b  ',)),
            4 : ({'a' : ('Sniq',(0,0),(bx,by),5,25,10,None,None),
                 ' ': None},
                ('    a   ',
                 '    a   ',
                 '  a a   ',
                 '  aaaaa ',
                 '   aaa  ',
                 '        ',)),
            
            },
        
        ###  Level 2  ####
        
        2: {
            1 : ({'a' : ('Jac',(0,0),(bx,by),5,15,(2,3),(5,7,9)),
                  'b' : ('Sniq',(0,0),(bx,by),5,14,1,None,None),
                 ' ': None},
                ('b      b',
                 ' aaaaaa ',
                 ' ababaa ',
                 ' aababa ',
                 ' aaaaaa ',
                 'b      b',)),
            2 : ({'a' : ('Tic',(0,0),(bx,by),5,None,500,100,False,None),
                  'b' : ('Crac',(0,0),(bx,by),5,10,3000,10,True,None),
                 ' ': None},
                ('abbbbbbb',
                 'aabbbbaa',
                 'aaaabaaa',
                 'aaabbbaa',
                 'aabbbbba',
                 'bbbbbbba',)),
            3 : ({'a' : ('Tic',(0,0),(bx,by),5,10,500,100,True,None),
                  'b' : ('Crac',(0,0),(bx,by),5,10,3000,10,True,None),
                  'c' : ('Sync',(0,0),(bx,by),5,None,1000,False,None),
                  'd' : ('Jac',(0,0),(bx,by),5,15,(2,3),(5,7,9)),
                 ' ': None},
                ('cccccccc',
                 'bddddddb',
                 'bdaaaadb',
                 'bdaaaadb',
                 'bddddddb',
                 'cccccccc',)),
            4 : ({'b' : ('Subtract',(0,0),(bx,by),5,25,None),
                  'a' : ('Crac',(0,0),(bx,by),5,5,1500,10,True,None),
                  'g' : ('Sniq',(0,0),(bx,by),5,14,1,None,None),
                  'd' : ('Shuq',(0,0),(bx,by),5,30,None),
                 ' ': None},
                ('gggggggg',
                 'adddddda',
                 'adbbbbda',
                 'adbbbbda',
                 'adddddda',
                 'gggggggg',)),
            
            },
        
        ###  Level 3  ####
        
        3: {
            1 : ({'b' : ('Subtract',(0,0),(bx,by),5,15,None),
                  'd' : ('Sync',(0,0),(bx,by),5,None,1500,None,None),
                 ' ': None},
                ('bbbbbbbb',
                 'b  dd  b',
                 'b dddd b',
                 'b dddd b',
                 'b  dd  b',
                 'bbbbbbbb',)),
            2 : ({'a' : ('Sync',(0,0),(bx,by),5,None,1500,None,None),
                  'b' : ('Sync',(0,0),(bx,by),5,15,3000,None,None),
                  'c' : ('Sync',(0,0),(bx,by),5,None,2000,None,None),
                  'd' : ('Sync',(0,0),(bx,by),5,15,4000,None,None),
                  'e' : ('Sync',(0,0),(bx,by),5,20,12000,None,None),
                  'f' : ('Sync',(0,0),(bx,by),5,20,15000,None,None),
                 ' ': None},
                ('bbbacddd',
                 'bbbacddd',
                 'aaaacccc',
                 'eeeeffff',
                 'ffeeeeff',
                 'ffffeeee',)),
            3 : ({'a' : ('Sync',(0,0),(bx,by),5,20,7000,False,None),
                  'b' : ('Crac',(0,0),(bx,by),5,15,2000,15,True,None),
                 ' ': None},
                ('bbbbbbbb',
                 'baaaaaba',
                 'babbaaba',
                 'baaabbba',
                 'babbbbba',
                 'aaaaaaaa',)),
            4 : ({'a' : ('Sync',(0,0),(bx,by),5,15,15000,True,None),
                  'b' : ('Crac',(0,0),(bx,by),5,15,20000,5,False,None),
                 ' ': None},
                (' bbbbbb ',
                 'baaaaaab',
                 'babaabab',
                 ' baaaab ',
                 ' babbab ',
                 ' bbbbbb ',)),
            },
        
        
        ###  Level 4  ####
        
        4: {
            1 : ({'a' : ('Block',(0,0),(bx,by),5,2,None),
                 ' ': None},
                (random_generator( ('a') ) )),
            2 : ({'a' : ('Nic',(0,0),(bx,by),10,2,None),
                 ' ': None},
                ('        ',
                 '        ',
                 '  aaaa  ',
                 '  aaaa  ',
                 '        ',
                 '        ',)),
            3 : ({'b' : ('Block',(0,0),(bx,by),5,2,None),
                  'a' : ('Nic',(0,0),(bx,by),10,2,None),
                 ' ': None},
                ('        ',
                 ' bbbbbb ',
                 ' baaaab ',
                 ' baaaab ',
                 ' bbbbbb ',
                 '        ',)),
            4 : ({'b' : ('Subtract',(0,0),(bx,by),5,15,None),
                  'a' : ('Nic',(0,0),(bx,by),10,2,None),
                 ' ': None},
                ('        ',
                 ' bbbbbb ',
                 ' baaaab ',
                 ' baaaab ',
                 ' bbbbbb ',
                 '        ',)),
            },
        
        ###  Level 5  ####
        
        5: {
            1 : ({'a' : ('Tic',(0,0),(bx,by),5,None,500,50,False,(2,3)),
                  'b' : ('Tic',(0,0),(bx,by),5,None,500,50,True,(3,5)),
                  'c' : ('Tic',(0,0),(bx,by),5,None,500,50,False,(5,7)),
                  'd' : ('Tic',(0,0),(bx,by),5,None,500,50,True,(2,9)),
                 ' ': None},
                ('dddddddd',
                 'abbbbbbd',
                 'abcbcbcd',
                 'acbcbcbd',
                 'accccccd',
                 'aaaaaaad',)),
            2 : ({'a' : ('Mock',(0,0),(bx,by),5,5,5000,0,None,2),
                  'b' : ('Nic',(0,0),(bx,by),5,None,None),
                  'c' : ('Jac',(0,0),(bx,by),5,None,(2),None),
                 ' ': None},
                ('aabbbbaa',
                 'acc  cca',
                 'bccc ccb',
                 'bccccccb',
                 'acc  cca',
                 'aabbbbaa',)),
            3 : ({'a' : ('Mock',(0,0),(bx,by),5,5,5000,2,None,2),
                  'b' : ('Crac',(0,0),(bx,by),5,10,5000,10,False,None),
                 ' ': None},
                ('   aa   ',
                 '  a  a  ',
                 '  a  a  ',
                 'bbb  bbb',
                 'b      b',
                 'bbbbbbbb',)),
            4 : ({'b' : ('Subtract',(0,0),(bx,by),5,25,None),
                  'a' : ('Crac',(0,0),(bx,by),5,5,1500,10,True,None),
                  'g' : ('Sniq',(0,0),(bx,by),5,14,1,None,None),
                  'd' : ('Shuq',(0,0),(bx,by),5,30,None),
                 ' ': None},
                ('gggggggg',
                 'adddddda',
                 'adbbbbda',
                 'adbbbbda',
                 'adddddda',
                 'gggggggg',)),
            },
            
        
        ###  Level 6  ####
        
        6: {
            1 : ({'a' : ('Mock',(0,0),(bx,by),5,3,2000,3,None,None), 
                 ' ': None},
                ('a      a',
                 ' a    a ',
                 '        ',
                 '        ',
                 ' a    a ',
                 'a      a',)),
            2 : ({'a' : ('Mock',(0,0),(bx,by),5,3,2000,1,None,None),
                  'b' : ('Sync',(0,0),(bx,by),5,None,2000,None,None),
                 ' ': None},
                ('a      a',
                 ' b    b ',
                 '  a  a  ',
                 '  b  b  ',
                 ' a    a ',
                 'b      b',)),
            3 : ({'a' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Crac',(0,0),(bx,by),5,None,2000,30,True,None),
                  'c' : ('Mock',(0,0),(bx,by),5,3,2000,0,None,None),
                 ' ': None},
                (random_generator( ('a','b','c') ) )),
            4 : ({'a' : ('Mock',(0,0),(bx,by),5,3,2000,0,None,1),
                  'c' : ('Block',(0,0),(bx,by),5,None,None),
                  'b' : ('Jac',(0,0),(bx,by),5,20,(2),None),
                 ' ': None},
                ('        ',
                 ' bbbbbb ',
                 ' bbcabb ',
                 ' bbacbb ',
                 ' bbbbbb ',
                 '        ',)),
            },
        
        ###  Level 7  ####
        
        7: {
            1 : ({'a' : ('Sync',(0,0),(bx,by),5,None,2000,False,(2,3)),
                      'b' : ('Sync',(0,0),(bx,by),5,None,2000,True,(5,7)),
                      'c' : ('Nic',(0,0),(bx,by),5,None,None),
                      'd' : ('Shuq',(0,0),(bx,by),5,30,None),
                     ' ': None},
                    ('aaaabbbb',
                     'addddddb',
                     'ad cc db',
                     'ad cc db',
                     'addddddb',
                     'aaaabbbb',)),
                2 : ({'a' : ('Jac',(0,0),(bx,by),5,20,(2),None),
                      'b' : ('Jac',(0,0),(bx,by),5,20,(3),None),
                      'c' : ('Sniq',(0,0),(bx,by),5,14,3,None,None),
                     ' ': None},
                    ('aaaaaaaa',
                     'abbbbbab',
                     'abccccab',
                     'abccccab',
                     'aaaaaaab',
                     'abbbbbbb',)),
                3 : ({'a' : ('Shuq',(0,0),(bx,by),5,30,None),
                     ' ': None},
                    (random_generator( ('a') ) )),
                4 : ({'a' : ('Sync',(0,0),(bx,by),5,20,1500,None,None),
                      'b' : ('Sync',(0,0),(bx,by),5,15,3000,None,None),
                      'c' : ('Sync',(0,0),(bx,by),5,10,4500,None,None),
                      'd' : ('Crac',(0,0),(bx,by),5,15,6000,10,False,None),
                      'e' : ('Tic',(0,0),(bx,by),5,None,500,100,False,None),
                     ' ': None},
                    ('addbbeec',
                     'addbbeec',
                     'addbbeec',
                     'addbbeec',
                     'addbbeec',
                     'addbbeec',)),
                
            },
        
        
        
        ###  Level 8  ####
        
        8: {
            1 : ({'b' : ('Nic',(0,0),(bx,by),5,10,None),
                  'a' : ('Shuq',(0,0),(bx,by),5,30,None),
                  'c' : ('Tic',(0,0),(bx,by),5,None,500,50,False,None),
                 ' ': None},
                ('aaaaaaaa',
                 'abbbbbba',
                 'abccccba',
                 'abccccba',
                 'abbbbbba',
                 'aaaaaaaa',)),
            2 : ({'a' : ('Jac',(0,0),(bx,by),5,20,(2),None),
                  'b' : ('Mythic',(0,0),(bx,by),5,10,None),
                  'c' : ('Nic',(0,0),(bx,by),5,10,None),
                 ' ': None},
                ('ccbbbbbb',
                 'accbbbbb',
                 'aaccbbbb',
                 'aaaccbbb',
                 'aaaaccbb',
                 'aaaaaccb',)),
            3 : ({'a' : ('Sniq',(0,0),(bx,by),5,14,3,None,None),
                  'b' : ('Nic',(0,0),(bx,by),5,10,None),
                  'c' : ('Jac',(0,0),(bx,by),5,None,(3),None),
                  'd' : ('Mock',(0,0),(bx,by),5,3,2000,0,None,None),
                 ' ': None},
                ('ccbddbcc',
                 'ccbddbcc',
                 'ccbccbcc',
                 'cabccdac',
                 'accaacca',
                 'aaaccaaa',)),
            4 : ({'a' : ('Mock',(0,0),(bx,by),5,3,1000,0,None,1),
                 ' ': None},
                (random_generator( ('a'), margin_x = 2, margin_y = 2 ) )),
            5 : ({'a' : ('Mock',(0,0),(bx,by),5,5,8500,0,None,2),
                 ' ': None},
                (random_generator( ('a') ) )),
            },
        
        
        ###############End###################
        }
    
    return crib_level


stage_layouts[3] = stage_crib_levels()