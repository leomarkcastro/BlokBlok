import pygame

###
'''
    Scenes:
    
    ---Main Menu---
    0 = Warning
    1 = Splash Screen
    A = Main Menu
    B = Select Story
    
    ---In between Games---
    C = Still Frame
    D = Dialogue
    E = Level Starter
    F = Win Game
    G = Lost
    
    ---Game---
    I = Intro Tutorial
    J = Game
    K = Endless
    L = Easter Egg
    M = Classic
    
    O = New Main Game
    R = Idle Mode
    S = Black Out
    
    ---Mini Menus---
    Q = Pause Interface
    P = Quit Interface

'''

#from game_variables import *
from game_sprites import *
from game_sound import *
from game_block_level import *
from game_block_level_classic import *

score = 0
test_level = None

sw = screenWidth
sh = screenHeight

def dt(x):
    x = list(x)
    x[0] = int(x[0] / 800 * sw)
    x[1] = int(x[1] / 600 * sh)
    
    return (x[0],x[1])

def dt2(x,y):
    x = list(x)
    x[0] = int(x[0] / 800 * sw)
    x[1] = int(x[1] / 600 * sh)
    
    y = list(y)
    y[0] = int(y[0] / 800 * sw)
    y[1] = int(y[1] / 600 * sh)
    
    return (x[0],x[1]),(y[0],y[1])

def block_collector(daset, mode = 'normal'):
    
    if mode == 'normal':
        retset = set()
        #print (daset)
        for phase in range(1,len(stage_layouts [daset[0]][daset[1]])+1):
            for key in (stage_layouts [daset[0]][daset[1]][phase] [0]):
                if ((stage_layouts [daset[0]][daset[1]][phase] [0][key])) != None:
                    retset.add(stage_layouts [daset[0]][daset[1]][phase] [0][key][0])
        #print (retset)
        return retset
    
    elif mode == 'classic':
        retset = set()
        #print (daset)
        
        for phase in range(1, len(classic_layouts[daset]['phases'])):
            for key in (classic_layouts[daset]['phases'][phase]['blocks']):
                if ((classic_layouts[daset]['phases'][phase]['blocks'][key])) != None:
                    retset.add(classic_layouts[daset]['phases'][phase]['blocks'][key][0])
        #print (retset)
        return retset

def block_preview(retset):
    blocksprites = set()
    
    delay = 500
    in_bet_multi = 4
    
    xy = 0
    
    for entry in retset:
        if entry == 'Block':
            blocksprites.add((LetterBox('Bl',blue,*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        elif entry == 'Subtract':
            blocksprites.add((LetterBox('Sb',(204, 153, 0),*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        elif entry == 'Mythic':
            blocksprites.add((LetterBox('My',violet,*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        elif entry == 'Sync':
            blocksprites.add((LetterBox('Sy',yellow,*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        elif entry == 'Jac':
            blocksprites.add((LetterBox('Ja',green,*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        elif entry == 'Crac':
            blocksprites.add((LetterBox('Cr',red,*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        elif entry == 'Tic':
            blocksprites.add((LetterBox('Tc',(0,62,62),*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        elif entry == 'Nic':
            blocksprites.add((LetterBox('Nc',(126,149,9),*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        elif entry == 'Sniq':
            blocksprites.add((LetterBox('Sn',(93,240,255),*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        elif entry == 'Shuq':
            blocksprites.add((LetterBox('Sh',(192,48,114),*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        elif entry == 'Mock':
            blocksprites.add((LetterBox('Mo',white,*dt2( [ 684+(52*(xy%2)) ,78+(52*(xy//2)) ] , [ 50 , 50 ]), 5 , 100*(in_bet_multi * xy)+delay,f_typo = font_typo[10])))
        
        xy += 1
        
    
    return blocksprites


class PygameTemplate:
    
    def __init__(self):
        
        pygame.init()
        
        self.gameDisplay = pygame.display.set_mode(size=(screenWidth, screenHeight), flags = display_flags)
        pygame.display.set_caption(screenCaption)
        
        self.clock = pygame.time.Clock()
        
        self.game_load()
        self.game_global_variables()
        
        self.running = '0'
        
        self.SceneLooper()
    
    def game_load(self):
        self.save_dict = json_load()
        if test_level != None:
            self.save_dict['continue'] = test_level
            
        self.settings_dict = json_load('settings.json')
    
    def game_global_variables(self):
        
        
        self.lose = 1
        
        if self.save_dict['continue'] != None: self.cur_slide = self.sel_slide = 6
        else: self.cur_slide = self.sel_slide = 1
        
        self.game_time_limit = game_time
        
        self.display_mode = 0
        
        self.lasttick = 1
        self.check = [-1,-2]
        self.classic_level = None
        self.classic_score = 0
        
        self.bg_gamefield = None
        
        self.game_timer_start = self.game_timer_end = 0
        self.click_timer_start = self.click_frequency = self.click_average = 0
        self.game_background = (0,0,0)
        self.game_music = music_array['endless']
        
        self.command = self.command_echo = ''
        
        self.game_levelname = 'CLASSIC GAME LEVEL {0}'
        self.game_leveltag = 'ENDLESS MODE'
        
        self.c_stage = ('Stage','Name')
        self.c_stage_tagline = 'Stage tag-line'
        self.c_still_frame = None
        self.c_frame_color = white
        
        self.intermission_msg = ("Classic Game", "Infinite Mode")
        
        self.d_frame_color = blue
        self.d_char_sprite = girl_sample
        self.d_char_name = 'Jess'
        self.d_messages = ({1:None, 2:"Hello", 3: None, 4:None, 5:None}, 
                         {1:None, 2:"My name is Jess", 3: None, 4:None, 5:None}, 
                         {1:"I'm so glad", 2:"to have you here", 3: "in our place", 4:None, 5:None})
     
    def SceneLooper(self):
        while len(self.running) != 0:
            if self.running == '9':
                self.ModeSetter()
            
            elif self.running == '0': #Warning
                self.Scene0()
            elif self.running == '1': #Title
                self.Scene1()
            elif self.running == '22': #Title
                self.running = '2'
            elif self.running == '2': #Settings
                self.Scene2()
            elif self.running == '3': #Title
                self.Scene3()
            elif self.running == 'A': #Play Game
                self.SceneA()
            elif self.running == 'B': #Level Select
                self.SceneB()
            elif self.running == 'C': #Still Frame of level
                self.SceneC()
            elif self.running == 'D': #Story Dialogue
                self.SceneD()
            elif self.running == 'E': #Level Label
                self.SceneE() 
            elif self.running == 'F': #Win Frame
                self.SceneF() 
            elif self.running == 'G': #Lose Frame
                self.SceneG() 
            
            elif self.running == 'I': #Old Main Game
                self.SceneI() 
            elif self.running == 'J': #Old Main Game
                self.SceneJ() 
            elif self.running == 'K': #Endless Mode
                self.SceneK() 
            elif self.running == 'L': #Weird Endless Mode
                self.SceneL() 
            elif self.running == 'M': #Classic Mode
                self.SceneM() 
            elif self.running == 'O': #Main Game
                self.SceneO() 
            elif self.running == 'R': #Idle Mode
                self.SceneR() 
            elif self.running == 'S': #Black Out
                self.SceneS() 
            
            elif self.running == 'Q': #Pause Prompt
                self.sceneQ()
            elif self.running == 'P': #Exit Prompt
                self.sceneQ()


    ### Mode #######################################################################

    def ModeSetter(self):
        
        def club_functions():
            if self.command == 'club_stillframe':
                self.c_stage = ('Azure','Club')
                self.c_stage_tagline = 'by raw energy'
                self.c_still_frame = still_frames[0]
                self.c_frame_color = blue
                self.running = 'C'
                self.command_echo = self.command
            elif self.command == 'club_dialogue':
                self.save_dict['continue'] = [1,1,1]
                json_save(self.save_dict)
                self.d_frame_color = blue
                self.c_still_frame = still_frames[0]
                self.d_char_sprite = girl_sample
                self.d_char_name = 'Jess'
                self.d_messages = ({1:None, 2:"Hey!", 3: None, 4:None, 5:None}, 
                                 {1:None, 2:"You're a new", 3: 'face here!', 4:None, 5:None}, 
                                 {1:None, 2:"My name is Jess", 3: "Nice to meet you!", 4:None, 5:None},
                                 {1:None, 2:"Welcome to the", 3: "Azure Club!", 4:None, 5:None},
                                 {1:None, 2:"Everyone's haven", 3: "for the Blok Blok", 4:"Sport", 5:None},
                                 {1:None, 2:"Some says that", 3: "Blok Blok is an", 4: "easy match", 5:None},
                                 {1:None, 2:"But you know,", 3: "under the", 4: "right hand", 5:None},
                                 {1:None, 2:"A Blok Blok", 3: "performance", 4: "can be a spectacle", 5:None},
                                 {1:None, 2:None, 3: "Can you prove that", 4: None, 5:None},
                                 )
                self.running = 'D'
                
            elif self.command == 'club_dialogue_2':
                if self.settings_dict['music']: playmusic(music_array['select_level'])
                self.save_dict['continue'] = [1,4,1]
                json_save(self.save_dict)
                self.d_frame_color = blue
                self.c_still_frame = still_frames[0]
                self.d_char_sprite = girl_sample
                self.d_char_name = 'Jess'
                self.d_messages = ({1:None, 2:"Looks like you're", 3: "enjoying your stay", 4:"here, aren't you", 5:None}, 
                                 {1:None, 2:"I've been watching", 3: 'your performance', 4:"from the back", 5:None}, 
                                 {1:None, 2:"I can say", 3: "that I am impressed", 4:"by your moves", 5:None},
                                 {1:None, 2:None, 3: "I can see...", 4:None, 5:None},
                                 {1:None, 2:None, 3: "...potential!", 4:None, 5:None},
                                 {1:None, 2:"Would you like", 3: "to have the floor", 4: "with me?", 5:None},
                                 {1:None, 2 : "I'm sure I will", 3: "be impressed", 4: None, 5:None},
                                 )
                                 
                self.running = 'D'
                
            elif self.command == 'club_dialogue_3':
                if self.settings_dict['music']: playmusic(music_array['select_level'])
                self.save_dict['continue'] = [1,6,1]
                json_save(self.save_dict)
                self.d_frame_color = blue
                self.c_still_frame = still_frames[0]
                self.d_char_sprite = girl_sample
                self.d_char_name = 'Jess'
                self.d_messages = ({1:None, 2:None, 3: "Hey!", 4:None, 5:None}, 
                                 {1:None, 2:"I would like", 3: 'to invite you to a', 4:"performance later", 5:None}, 
                                 {1:None, 2:"It will be our", 3: "solo Blok Blok performance", 4:"in front of the people", 5:None},
                                 {1:None, 2:"For now,", 3: "just stay for ", 4:"a longer bit", 5:None},
                                 {1:None, 2:"Also, I would like", 3: "to share a guide", 4:"to you", 5:None},
                                 {1:None, 2:"Blok Blok can be", 3: "performed in", 4: "many ways", 5:None},
                                 {1:None, 2 : "But a graceful player", 3: "observes the stage first", 4: "for opportunities", 5:None},
                                 {1:None, 2 : "...", 3: None, 4: None, 5:None},
                                 {1:None, 2 : None, 3: "See you later!", 4: None, 5:None},
                                 )
                                 
                self.running = 'D'
                
            elif self.command == 'club_dialogue_4':
                if self.settings_dict['music']: playmusic(music_array['select_level'])
                self.save_dict['continue'] = [1,8,1]
                json_save(self.save_dict)
                self.d_frame_color = blue
                self.c_still_frame = still_frames[0]
                self.d_char_sprite = girl_sample
                self.d_char_name = 'Jess'
                self.d_messages = ({1:None, 2:None, 3: "This is it!", 4:None, 5:None}, 
                                 {1:None, 2:"I feeel so nervous", 3: 'and excited at', 4:"the same time!", 5:None}, 
                                 {1:None, 2:"But don't mind me.", 3: "Just do your best,", 4:"I truly believe in you", 5:None},
                                 {1:None, 2:"Focus on the pattern,", 3: "Follow the rhythm", 4:None, 5:None},
                                 {1:None, 2:None, 3: "and most important...", 4:None, 5:None},
                                 {1:None, 2:"Just, enjoy the", 3: "spectacle that is", 4: "Blok Blok", 5:None},
                                 )
                                 
                self.running = 'D'
                
            elif self.command == 'club_dialogue_5':
                self.command_echo = 'end'
                self.save_dict['continue'] = None

                
                if self.save_dict['level'] == 1:
                    self.save_dict['level'] = 2
                    
                json_save(self.save_dict)
                self.d_frame_color = blue
                self.c_still_frame = still_frames[0]
                self.d_char_sprite = girl_sample
                self.d_char_name = 'Jess'
                self.d_messages = ({1:None, 2:None, 3: "THAT WAS AMAZING!!!", 4:None, 5:None}, 
                                 {1:None, 2:"I knew that I was", 3: 'right when I first saw', 4:"you perform those tricks", 5:None}, 
                                 {1:None, 2:"You were breathtaking,", 3: "swift and just glorious!", 4:None, 5:None},
                                 {1:None, 2:"You now just earned", 3: "a fanatic right here!", 4:None, 5:None},
                                 {1:None, 2:None, 3: "Hey!", 4:None, 5:None},
                                 {1:None, 2:"Why don't you try", 3: "the Blok Blok League", 4: None, 5:None},
                                 {1:None, 2:"It is being held", 3: "at the Underground City!", 4: None, 5:None},
                                 {1:None, 2:"Try earning some", 3: "well deserved recognition", 4: "for your skills", 5:None},
                                 {1:None, 2:"I will be keeping", 3: "in touch with you by then", 4: None, 5:None},
                                 {1:None, 2:"Once again,", 3: "Congratulations!", 4: "You're amazing!", 5:None},
                                 )
                                 
                self.running = 'D'
                self.command_echo = 'end'
            
            self.command = ''

        def under_functions():
            
            if self.command == 'under_stillframe':
                self.c_stage = ('Under','Scene')
                self.c_stage_tagline = 'tricks or trickery'
                self.c_still_frame = still_frames[1]
                self.c_frame_color = green
                self.running = 'C'
                self.command_echo = self.command
                
            elif self.command == 'under_dialogue':
                self.save_dict['continue'] = [2,1,1]
                json_save(self.save_dict)
                self.d_frame_color = green
                self.c_still_frame = still_frames[1]
                self.d_char_sprite = thug_sample
                self.d_char_name = 'Cross'
                self.d_messages = ({1:None, 2:None, 3: "...", 4:None, 5:None}, 
                                 {1:None, 2:"Are you sure that you", 3: 'are in the right place?', 4:None, 5:None}, 
                                 {1:None, 2:None, 3: "Oh... You must be that guy", 4:None, 5:None},
                                 {1:None, 2:"Hey let me tell", 3: "you something", 4:None, 5:None},
                                 {1:None, 2:"If you think you're", 3: "good enough just because of your", 4:"careless button mashing", 5:None},
                                 {1:None, 2:None, 3: "then... shut the hell up", 4: None, 5:None},
                                 {1:None, 2:"You're just like those", 3: "noobs who thinks they can", 4: "rule the Blok Blok scene", 5:None},
                                 {1:None, 2:"just because they", 3: "can clik clak the hell out", 4: "of their asses", 5:None},
                                 {1:None, 2:None, 3: "...", 4: None, 5:None},
                                 {1:None, 2:None, 3: "If you want respect", 4: None, 5:None},
                                 {1:None, 2:None, 3: "Prove it", 4: None, 5:None},
                                 {1:None, 2:None, 3: "We will be amazed", 4: None, 5:None},
                                 {1:None, 2:"Either by your cries", 3: "or desperation", 4: None, 5:None},
                                 {1:None, 2:None, 3: "Good luck kiddo", 4: None, 5:None},
                                 )
                self.running = 'D'
                                
            elif self.command == 'under_dialogue_2':
                if self.settings_dict['music']: playmusic(music_array['select_level'])
                self.save_dict['continue'] = [2,4,1]
                json_save(self.save_dict)
                self.d_frame_color = green
                self.c_still_frame = still_frames[1]
                self.d_char_sprite = thug_sample
                self.d_char_name = 'Cross'
                self.d_messages = ({1:None, 2:None, 3: "So you are making...", 4:None, 5:None}, 
                                 {1:None, 2:None, 3: "...quite a show right there", 4:None, 5:None}, 
                                 {1:None, 2:None, 3: "Amazing", 4:None, 5:None},
                                 {1:None, 2:None, 3: "but still average", 4:None, 5:None},
                                 {1:None, 2:None, 3: "Actually, here's a gift from me" ,4:None, 5:None},
                                 {1:None, 2:None, 3: "BECAREFUL, ITS HOT", 4: None, 5:None},
                                 )
                self.running = 'D'
                
            elif self.command == 'under_dialogue_3':
                if self.settings_dict['music']: playmusic(music_array['select_level'])
                self.save_dict['continue'] = [2,6,1]
                json_save(self.save_dict)
                self.d_frame_color = green
                self.c_still_frame = still_frames[1]
                self.d_char_sprite = crib_sample
                self.d_char_name = 'Ccino'
                self.d_messages = ({1:None, 2:None, 3: "So you are the legend, huh", 4:None, 5:None}, 
                                 {1:None, 2:"Good Morning Sir,", 3: "My name is Peroccino", 4:None, 5:None}, 
                                 {1:None, 2:"I am quite a", 3: "Blok Blok enthusiast", 4:"you see", 5:None},
                                 {1:None, 2:"And I'm interested", 3: "with people who can", 4:"really do the magic", 5:None},
                                 {1:None, 2:None, 3: "You know what I mean right" ,4:None, 5:None},
                                 {1:None, 2:None, 3: "Later", 4: None, 5:None},
                                 {1:None, 2:"Defeat that brat of", 3: "a guy named Cross", 4: "in the battle", 5:None},
                                 {1:None, 2:"I'll give you", 3: "a rather quite rate", 4: "offer", 5:None},
                                 {1:None, 2:None, 3: "Don't dissapoint me young man", 4: None, 5:None},
                                 )
                self.running = 'D'
                
            elif self.command == 'under_dialogue_4':
                if self.settings_dict['music']: playmusic(music_array['select_level'])
                self.save_dict['continue'] = [2,8,1]
                json_save(self.save_dict)
                self.d_frame_color = green
                self.c_still_frame = still_frames[1]
                self.d_char_sprite = thug_sample
                self.d_char_name = 'Cross'
                self.d_messages = ({1:None, 2:None, 3: "...", 4:None, 5:None}, 
                                 {1:None, 2:"You are quite a man", 3: "aren't you", 4:None, 5:None}, 
                                 {1:None, 2:"And I respect", 3: "your skills", 4:None, 5:None},
                                 {1:None, 2:"As of my word,", 3: "You had earned my respect", 4:None, 5:None},
                                 {1:None, 2:None, 3: "But this fight" ,4:None, 5:None},
                                 {1:None, 2:None, 3: "This is important business", 4: None, 5:None},
                                 {1:None, 2:"So I'll destroy", 3: "anything who will get", 4: "in the way", 5:None},
                                 {1:None, 2:None, 3: "Prepare your gears", 4: None, 5:None},
                                 )
                self.running = 'D'
                
            elif self.command == 'under_dialogue_5':
                self.save_dict['continue'] = None
                
                if self.save_dict['level'] < 3 :
                    self.save_dict['level'] = 3
                    
                json_save(self.save_dict)
                self.d_frame_color = green
                self.c_still_frame = still_frames[1]
                self.d_char_sprite = crib_sample
                self.d_char_name = 'Ccino'
                self.d_messages = ({1:None, 2:None, 3: "Look at you gentleman", 4:None, 5:None}, 
                                 {1:None, 2:"You are a rare talent", 3: "that only appears in a legend", 4:None, 5:None}, 
                                 {1:None, 2:"You really deserve", 3: "my attention", 4:None, 5:None},
                                 {1:None, 2:"Here's your card and", 3: "your code to the Elite's crib", 4:None, 5:None},
                                 {1:None, 2:None, 3: "You will be treated accordingly" ,4:None, 5:None},
                                 {1:None, 2:None, 3: "Once again", 4: None, 5:None},
                                 {1:None, 2:None, 3: "Congratulations", 4: None, 5:None},
                                 )
                
                self.running = 'D'
                self.command_echo = 'end'
            
            self.command = ''
        
        def crib_functions():
            
            if self.command == 'crib_stillframe':
                self.c_stage = ('Crib','Elite')
                self.c_stage_tagline = 'By the fear of no'
                self.c_still_frame = still_frames[2]
                self.c_frame_color = violet
                self.running = 'C'
                self.command_echo = self.command
                
            elif self.command == 'crib_dialogue':
                self.save_dict['continue'] = [3,1,1]
                json_save(self.save_dict)
                self.d_frame_color = violet
                self.c_still_frame = still_frames[2]
                self.d_char_sprite = crib_sample
                self.d_char_name = 'Ccino'
                self.d_messages = ({1:None, 2:None, 3: "Welcome to the crib elite", 4:None, 5:None}, 
                                 {1:None, 2:"I, again, am Peroccino", 3: 'Macciano Maximiano', 4:None, 5:None}, 
                                 {1:None, 2:None, 3: "The Sponsor of this Tournament", 4:None, 5:None},
                                 {1:None, 2:"I gather all the amazing and", 3: "breathtaking Blok Blok", 4:"performers nationwide", 5:None},
                                 {1:None, 2:None, 3: "Of course", 4:None, 5:None},
                                 {1:None, 2:"Those who will win will get", 3: "the title of", 4: "Blok Blok Master", 5:None},
                                 {1:None, 2:None, 3: "And money of course", 4: None, 5:None},
                                 {1:None, 2:"Let the battle of", 3: "wits, energy and fear", 4: "begin", 5:None},
                                 {1:None, 2:None, 3: "I will watch you my prodigy", 4: None, 5:None},
                                 )
                self.running = 'D'
                
            elif self.command == 'crib_dialogue_2':
                if self.settings_dict['music']: playmusic(music_array['select_level'])
                self.save_dict['continue'] = [3,5,1]
                json_save(self.save_dict)
                self.d_frame_color = violet
                self.c_still_frame = still_frames[2]
                self.d_char_sprite = girl_sample
                self.d_char_name = 'Jess'
                self.d_messages = ({1:None, 2:None, 3: "Hey!", 4:None, 5:None}, 
                                 {1:None, 2:"I knew that we will", 3: 'meet again sometime!', 4:None, 5:None}, 
                                 {1:None, 2:None, 3: "My name is Jess Ashford", 4:None, 5:None},
                                 {1:None, 2:"Last... Last Year's Blok Blok", 3: "Championship", 4:"Grand Master", 5:None},
                                 {1:None, 2:"I was defeated by", 3: "Cross last year", 4:None, 5:None},
                                 {1:None, 2:"And I am very determined", 3: "to get that title back", 4: "to me!", 5:None},
                                 {1:None, 2:None, 3: "Are you in for my fire?", 4: None, 5:None},
                                 )
                self.running = 'D'
                
            elif self.command == 'crib_dialogue_3':
                if self.settings_dict['music']: playmusic(music_array['select_level'])
                self.save_dict['continue'] = [3,7,1]
                json_save(self.save_dict)
                self.d_frame_color = violet
                self.c_still_frame = still_frames[2]
                self.d_char_sprite = thug_sample
                self.d_char_name = 'Cross'
                self.d_messages = ({1:None, 2:None, 3: "Surprised aren't ya?", 4:None, 5:None}, 
                                 {1:None, 2:"You just defeated a champion", 3: 'in the underground scene', 4:None, 5:None}, 
                                 {1:None, 2:None, 3: "It is pretty humiliating", 4:None, 5:None},
                                 {1:None, 2:"But don't worry", 3: "I will never let it happen", 4:"again", 5:None},
                                 {1:None, 2:None, 3: "I'll destroy you now", 4:None, 5:None},
                                 )
                self.running = 'D'
                
            elif self.command == 'crib_dialogue_4':
                if self.settings_dict['music']: playmusic(music_array['select_level'])
                self.save_dict['continue'] = [3,8,1]
                json_save(self.save_dict)
                self.d_frame_color = violet
                self.c_still_frame = still_frames[2]
                self.d_char_sprite = crib_sample
                self.d_char_name = 'Ccino'
                self.d_messages = ({1:None, 2:None, 3: "You managed to defeat the elites", 4:None, 5:None}, 
                                 {1:None, 2:"Now, I'll give to you the", 3: 'ultimate challenge', 4:None, 5:None}, 
                                 {1:None, 2:None, 3: "Win this judgement level", 4:None, 5:None},
                                 {1:None, 2:None, 3: "and you'll be the king", 4:None, 5:None},
                                 {1:None, 2:None, 3: "Get Ready", 4: None, 5:None},
                                 )
                self.running = 'D'
                
            elif self.command == 'under_dialogue_5':
                self.save_dict['continue'] = None
                
                if self.save_dict['level'] < 4 :
                    self.save_dict['level'] = 4
                    
                json_save(self.save_dict)
                self.d_frame_color = green
                self.c_still_frame = still_frames[1]
                self.d_char_sprite = crib_sample
                self.d_char_name = 'Ccino'
                self.d_messages = ({1:None, 2:None, 3: "AMAZING!", 4:None, 5:None}, 
                                 {1:None, 2:"You are a magnifico", 3: "talentado y magico", 4:None, 5:None}, 
                                 {1:None, 2:"You really are a delight", 3: "in the world of the BLok Blok", 4:"Championship", 5:None},
                                 {1:None, 2:"As a reward I'll give you the elite", 3: "access extras", 4:None, 5:None},
                                 {1:None, 2:None, 3: "You can access much things in that place" ,4:None, 5:None},
                                 {1:None, 2:None, 3: "Once again", 4: None, 5:None},
                                 {1:None, 2:None, 3: "Congratulations", 4: None, 5:None},
                                 )
                
                self.running = 'D'
                self.command_echo = 'end'
            
            self.command = ''
        
        def stage_builder_function():
            
            def club():
                self.game_background = (0,0,10)
                self.bg_gamefield = 'club'
                self.c_still_frame = still_frames[0]
                
                if self.save_dict['continue'][1] == 1:
                    self.intermission_msg = ("Welcome to the Club", "Level 1-1")
                    self.running = 'E'
                    self.game_levelname = 'AZURE CLUB 1-1 Phase:{0}of{1}'
                    self.game_leveltag = 'The Azure Club'
                    self.game_time_limit = 30
                    self.game_music = music_array['club_music']
                    
                elif self.save_dict['continue'][1] == 2:
                    self.intermission_msg = ("Give Me More", "Level 1-2")
                    self.running = 'E'
                    self.game_levelname = 'AZURE CLUB 1-2 Phase:{0}of{1}'
                    self.game_leveltag = 'Give Me More'
                    self.game_time_limit = 40
                    self.game_music = music_array['club_music']
                    
                elif self.save_dict['continue'][1] == 3:
                    self.intermission_msg = ("Start of a Myth", "Level 1-3")
                    self.running = 'E'
                    self.game_levelname = 'AZURE CLUB 1-3 Phase:{0}of{1}'
                    self.game_leveltag = 'Start of Myth'
                    self.game_time_limit = 30
                    self.game_music = music_array['club_music']
                    
                elif self.save_dict['continue'][1] == 4:
                    #self.game_background = (0,0,130)
                    self.intermission_msg = ("Time to Impress", "Level 1-4")
                    self.running = 'E'
                    self.game_levelname = 'AZURE CLUB 1-4 Phase:{0}of{1}'
                    self.game_leveltag = 'Impressions'
                    self.game_time_limit = 30
                    self.game_music = music_array['club_music']
                    
                elif self.save_dict['continue'][1] == 5:
                    #self.game_background = (0,0,100)
                    self.intermission_msg = ("Reinforcement", "Level 1-5")
                    self.running = 'E'
                    self.game_levelname = 'AZURE CLUB 1-5 Phase:{0}of{1}'
                    self.game_leveltag = 'Reinforcement'
                    self.game_time_limit = 30
                    self.game_music = music_array['club_music']
                    
                elif self.save_dict['continue'][1] == 6:
                    #self.game_background = (0,0,100)
                    self.intermission_msg = ("Taking Attentions", "Level 1-6")
                    self.running = 'E'
                    self.game_levelname = 'AZURE CLUB 1-6 Phase:{0}of{1}'
                    self.game_leveltag = 'Her Attention'
                    self.game_time_limit = 30
                    self.game_music = music_array['club_music']
                    
                elif self.save_dict['continue'][1] == 7:
                    #self.game_background = (0,0,100)
                    self.intermission_msg = ("A bit of anomaly", "Level 1-7")
                    self.running = 'E'
                    self.game_levelname = 'AZURE CLUB 1-7 Phase:{0}of{1}'
                    self.game_leveltag = 'Some Anomalies'
                    self.game_time_limit = 30
                    self.game_music = music_array['club_music']
                    
                elif self.save_dict['continue'][1] == 8:
                    self.c_frame_color = (200,0,0)
                    #self.game_background = (0,0,200)
                    self.intermission_msg = ("A DANCE OF COLORS", "Level 1 - BOSS")
                    self.running = 'E'
                    self.game_levelname = 'AZURE CLUB 1-8 Phase:{0}of{1}'
                    self.game_leveltag = 'Dance;Colors'
                    self.game_time_limit = 30
                    self.game_music = music_array['club_boss']

            def under():
                self.game_background = (0,10,0)
                self.bg_gamefield = 'under'
                self.c_still_frame = still_frames[1]
                
                if self.save_dict['continue'][1] == 1:
                    self.intermission_msg = ("Tricks for the wicked", "Level 2-1")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 2-1 Phase:{0}of{1}'
                    self.game_leveltag = 'Wicked Tricks'
                    self.game_time_limit = 30
                    self.game_music = music_array['under_music']
                    
                elif self.save_dict['continue'][1] == 2:
                    self.intermission_msg = ("Miscommunications", "Level 2-2")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 2-2 Phase:{0}of{1}'
                    self.game_leveltag = 'Miscommunicate'
                    self.game_time_limit = 30
                    self.game_music = music_array['under_music']
                    
                elif self.save_dict['continue'][1] == 3:
                    self.intermission_msg = ("A Bad Tandem", "Level 2-3")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 2-3 Phase:{0}of{1}'
                    self.game_leveltag = 'A Bad Tandem'
                    self.game_time_limit = 30
                    self.game_music = music_array['under_music']
                    
                elif self.save_dict['continue'][1] == 4:
                    self.intermission_msg = ("Hot Gift, Hot Block", "Level 2-4")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 2-4 Phase:{0}of{1}'
                    self.game_leveltag = 'The Hot Gift'
                    self.game_time_limit = 30
                    self.game_music = music_array['under_music']
                    
                elif self.save_dict['continue'][1] == 5:
                    self.intermission_msg = ("Hidden Intentions", "Level 2-5")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 2-5 Phase:{0}of{1}'
                    self.game_leveltag = 'Bad Intents'
                    self.game_time_limit = 30
                    self.game_music = music_array['under_music']
                    
                elif self.save_dict['continue'][1] == 6:
                    self.intermission_msg = ("The Proposition", "Level 2-6")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 2-6 Phase:{0}of{1}'
                    self.game_leveltag = 'Proposements'
                    self.game_time_limit = 30
                    self.game_music = music_array['under_music']
                    
                elif self.save_dict['continue'][1] == 7:
                    self.intermission_msg = ("The Calm", "Level 2-7")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 2-7 Phase:{0}of{1}'
                    self.game_leveltag = 'The Calm'
                    self.game_time_limit = 30
                    self.game_music = music_array['under_music']
                    
                elif self.save_dict['continue'][1] == 8:
                    self.intermission_msg = ("The Fear of Unknown", "Level 2-8")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 2-8 Phase:{0}of{1}'
                    self.game_leveltag = 'Unknown Fear'
                    self.game_time_limit = 30
                    self.game_music = music_array['under_boss']
            
            def crib():
                self.game_background = (0,15,0)
                self.bg_gamefield = 'crib'
                self.c_still_frame = still_frames[2]
                
                if self.save_dict['continue'][1] == 1:
                    self.intermission_msg = ("Baby Treatment", "Level 3-1")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 3-1 Phase:{0}of{1}'
                    self.game_leveltag = 'Baby Treat'
                    self.game_time_limit = 30
                    self.game_music = music_array['crib_music']
                
                elif self.save_dict['continue'][1] == 2:
                    self.intermission_msg = ("Sample Exercise", "Level 3-2")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 3-2 Phase:{0}of{1}'
                    self.game_leveltag = 'Sample Exercise'
                    self.game_time_limit = 30
                    self.game_music = music_array['crib_music']
                    
                elif self.save_dict['continue'][1] == 3:
                    self.intermission_msg = ("This again", "Level 3-3")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 3-3 Phase:{0}of{1}'
                    self.game_leveltag = 'This Again'
                    self.game_time_limit = 30
                    self.game_music = music_array['crib_music']
                    
                elif self.save_dict['continue'][1] == 4:
                    self.intermission_msg = ("Nik of Time", "Level 3-4")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 3-4 Phase:{0}of{1}'
                    self.game_leveltag = 'Nik of Time'
                    self.game_time_limit = 30
                    self.game_music = music_array['crib_music']
                    
                elif self.save_dict['continue'][1] == 5:
                    self.intermission_msg = ("Jess", "Level 3-5")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 3-5 Phase:{0}of{1}'
                    self.game_leveltag = 'Jess'
                    self.game_time_limit = 30
                    self.game_music = music_array['club_boss']
                    
                elif self.save_dict['continue'][1] == 6:
                    self.intermission_msg = ("Heavy Rotation", "Level 3-6")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 3-6 Phase:{0}of{1}'
                    self.game_leveltag = 'Heavy Rotation'
                    self.game_time_limit = 30
                    self.game_music = music_array['crib_music']
                    
                elif self.save_dict['continue'][1] == 7:
                    self.intermission_msg = ("The Dark Sage", "Level 3-7")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 3-7 Phase:{0}of{1}'
                    self.game_leveltag = 'The Dark Sage'
                    self.game_time_limit = 30
                    self.game_music = music_array['under_boss']
                    
                elif self.save_dict['continue'][1] == 8:
                    self.intermission_msg = ("The End", "Level 3 Boss")
                    self.running = 'E'
                    self.game_levelname = 'UNDER SCENE 3-8 Phase:{0}of{1}'
                    self.game_leveltag = 'The End'
                    self.game_time_limit = 30
                    self.game_music = music_array['crib_boss']
                    
                        
            if self.save_dict['continue'][0] == 1:
                club()
            elif self.save_dict['continue'][0] == 2:
                under()
            elif self.save_dict['continue'][0] == 3:
                crib()
                
                    
            self.command = ''
        
        def next_stage_function():
            
            self.command = ''
            
            def dialogue_checker():
                if self.save_dict['continue'] == [1,4,1]:
                    self.command = 'club_dialogue_2'
                elif self.save_dict['continue'] == [1,6,1]:
                    self.command = 'club_dialogue_3'
                elif self.save_dict['continue'] == [1,8,1]:
                    self.command = 'club_dialogue_4'
                elif self.save_dict['continue'] == [1,9,1]:
                    self.command = 'club_dialogue_5'
                    
                elif self.save_dict['continue'] == [2,4,1]:
                    self.command = 'under_dialogue_2'
                elif self.save_dict['continue'] == [2,6,1]:
                    self.command = 'under_dialogue_3'
                elif self.save_dict['continue'] == [2,8,1]:
                    self.command = 'under_dialogue_4'
                elif self.save_dict['continue'] == [2,9,1]:
                    self.command = 'under_dialogue_5'
                    
                elif self.save_dict['continue'] == [3,5,1]:
                    self.command = 'crib_dialogue_2'
                elif self.save_dict['continue'] == [3,7,1]:
                    self.command = 'crib_dialogue_3'
                elif self.save_dict['continue'] == [3,8,1]:
                    self.command = 'crib_dialogue_4'
                elif self.save_dict['continue'] == [3,9,1]:
                    self.command = 'crib_dialogue_5'
            
            self.save_dict['continue'][1] += 1
            self.save_dict['continue'][2] = 1
            
            
            json_save(self.save_dict)
            
            dialogue_checker()
            
            if self.command == '':
                self.command = 'play_stage'
        
        if self.command == 'endless':

            self.endless_save = self.save_dict['continue']
            
            self.save_dict['continue'] = [None,1,1]
            
            self.c_frame_color = (200,200,200)
            self.game_background = (50,50,50)
            self.intermission_msg = ("An Endless Pit", "Endless Mode")
            self.running = 'E'
            self.game_levelname = 'Endless Mode Board: {0}'
            self.game_leveltag = 'Endless Mode'
            self.game_time_limit = 20
            self.game_music = music_array['endless']
        
        elif self.command == 'idle':

            self.endless_save = self.save_dict['continue']
            
            self.save_dict['continue'] = [None,1,1]
            
            self.c_still_frame = random.choice(still_frames)
            self.bg_gamefield = random.choice(('club','under','crib'))
            self.c_frame_color = (0,200,200)
            self.game_background = (0,25,25)
            self.intermission_msg = ("Light Bonanza", "Idle Mode")
            self.running = 'E'
            self.game_levelname = 'Idle Mode Board: {0}'
            self.game_leveltag = 'Idle Mode'
            self.game_time_limit = 20
            self.game_music = random.choice(lounge_array)
            
        elif self.command == 'blackout':

            self.endless_save = self.save_dict['continue']
            
            self.save_dict['continue'] = [None,1,1]
            
            self.c_still_frame = random.choice(still_frames)
            self.bg_gamefield = random.choice(('club','under','crib'))
            self.c_frame_color = (200,200,200)
            self.game_background = (25,25,25)
            self.intermission_msg = ("Blink Slower Than You", "BlackOut Mode")
            self.running = 'E'
            self.game_levelname = 'BlackOut Mode Board: {0}'
            self.game_leveltag = 'Blackout Mode'
            self.game_time_limit = 20
            self.game_music = random.choice(lounge_array)
            
        elif self.command == 'classic':
            
            if self.save_dict['continue'] != None:
                if self.save_dict['continue'][0] != None:
                    self.endless_save = self.save_dict['continue']
            else:
                self.endless_save = self.save_dict['continue']
            
            if self.classic_level != None:
                self.check.append(self.classic_level)
                while len(self.check) > repeat_protection:
                    self.check.pop(0)
            
            while True:
                if self.classic_level == None:
                    if classic_test != None:
                        self.classic_level = classic_test
                    else:
                        self.classic_level = random.randint(0,len(classic_layouts)-1)
                else:
                    self.classic_level = random.randint(0,len(classic_layouts)-1)
                #print (self.classic_level, tuple(self.check))
                if not self.classic_level in tuple(self.check):
                    break
            #print (self.classic_level)
            
            self.save_dict['continue'] = [None,1,1]
            
            self.c_still_frame = still_frames[3]
            self.bg_gamefield = random.choice(('club','under','crib'))
            self.c_frame_color = (200,0,200)
            self.game_background = (50,0,50)
            self.intermission_msg = (classic_layouts[self.classic_level]['title'], "Classic Mode")
            self.running = 'E'
            self.game_levelname = 'Classic Board: {0} Phase: {1}'
            self.game_leveltag = classic_layouts[self.classic_level]['title']
            self.game_time_limit = classic_layouts[self.classic_level]['time']
            self.game_music = random.choice(lounge_array)
            
        elif self.command == 'funny':
                    
            self.endless_save = self.save_dict['continue']
            
            self.save_dict['continue'] = [None,50,1]
            
            self.c_frame_color = (255,20,147)
            self.game_background = (255//2,20//2,147//2)
            self.intermission_msg = ("Plok Plok Time!", "Weird Endless Mode")
            self.running = 'E'
            self.game_levelname = 'Weird Endless Mode Board: {0}'
            self.game_leveltag = 'Plok Plok Time!'
            self.game_time_limit = 20
            self.game_music = music_array['main_menu_2']
            
        elif 'club' in self.command:
            club_functions()
            
        elif 'under' in self.command:
            under_functions()
            
        elif 'crib' in self.command:
            crib_functions()
            
        elif self.command == 'play_stage':
            stage_builder_function()
        
        elif self.command == 'next_stage':
            next_stage_function()
            
        else:
            self.running = ''
            

    ### SCENES #######################################################################

    def Scene0(self):
        
        self.y_message_ctr = 0
        self.y_message_ctr_max = 2
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        if self.y_message_ctr < self.y_message_ctr_max:
                            self.text_sprite.empty()
                            self.y_message_ctr += 1
                            
                        if self.y_message_ctr >= self.y_message_ctr_max:
                            if self.save_dict['first']: self.running = 'I'
                            else: self.running = '1'
                            
                    elif event.key == pygame.K_x:
                        self.running = ''
                
        def game_system(): #try your best to put all the input functions here
            game_control()
            
            '''if not self.box.rect.collidepoint(pygame.mouse.get_pos()):
                if (pygame.mouse.get_pos()[0]) > self.box.rect.right:
                    self.box.rect.right = pygame.mouse.get_pos()[0]
                elif (pygame.mouse.get_pos()[0]) < self.box.rect.left:
                    self.box.rect.left = pygame.mouse.get_pos()[0]'''
            
            if self.lasttick + 1500 < pygame.time.get_ticks():
                if len(self.text_sprite) == 0:
                    if self.y_message_ctr == 0:
                        self.text_sprite.add(LetterBox_t("Game contains flashing lights",black,dt([0,225]), dt([800,50]),width = 1,f_typo = font_typo[10]))
                        self.text_sprite.add(LetterBox_t("and fast-paced events.",black,dt([0,250]), dt([800,50]),width = 1,f_typo = font_typo[10]))
                    if self.y_message_ctr == 1:
                        self.text_sprite.add(LetterBox_t("Presented by:",black,dt([0,225]), dt([800,50]),width = 1,f_typo = font_typo[10]))
                        self.text_sprite.add(LetterBox_t("BE-BE-SE-PE-EH-TU-BE",black,dt([0,250]), dt([800,50]),width = 1,f_typo = font_typo[10]))
                    
            
            if self.proctick + 5000 < pygame.time.get_ticks():
                if self.y_message_ctr < self.y_message_ctr_max:
                    self.text_sprite.empty()
                    self.y_message_ctr += 1
                    self.proctick = pygame.time.get_ticks()
                
                if self.y_message_ctr >= self.y_message_ctr_max:
                    if self.save_dict['first']: self.running = 'I'
                    else: self.running = '1'
                
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            for item in self.text_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            
            self.all_sprite.draw(self.gameDisplay)
            
            self.text_sprite.draw(self.gameDisplay)
            
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            self.lasttick = pygame.time.get_ticks()
            
            self.proctick = pygame.time.get_ticks()

            self.text_sprite = pygame.sprite.Group()
            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(CharacBox(bg_fade, black, *dt2([0,0],[800,600]), width = 1))
            
            
            
        def game_loop():
            
            game_start()
            
            while '0' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()


    def Scene1(self):
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_q:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.running = 'A'
                        self.command = 'cont_mus'
                    elif event.key == pygame.K_a:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.running = '2'
                    elif event.key == pygame.K_z:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.running = '3'
                    elif event.key == pygame.K_x:
                        self.running = ''
                        
                if event.type == pygame.MOUSEMOTION:
                    
                    check = self.a_text_ctr
                    
                    #print (check)
                    
                    self.a_start.updating = self.a_set.updating = self.a_help.updating = self.a_exit.updating = True
                    self.a_start.bgcolor = self.a_set.bgcolor = self.a_help.bgcolor = self.a_exit.bgcolor =(1,1,1)
                    
                    self.a_bg1.bg_play = pygame.mouse.get_pos()[0]
                    #self.a_bg2.bg_play = pygame.mouse.get_pos()[1]
                    
                    if self.a_start.rect.collidepoint(pygame.mouse.get_pos()):
                        self.a_start.updating = True
                        self.a_start.bgcolor = (0,0,175)
                        self.a_text_ctr = 1
                        
                    elif self.a_set.rect.collidepoint(pygame.mouse.get_pos()):
                        self.a_set.updating = True
                        self.a_set.bgcolor = (175,175,175)
                        self.a_text_ctr = 2
                        
                    elif self.a_help.rect.collidepoint(pygame.mouse.get_pos()):
                        self.a_help.updating = True
                        self.a_help.bgcolor = (0,175,0)
                        self.a_text_ctr = 3
                        
                    elif self.a_exit.rect.collidepoint(pygame.mouse.get_pos()):
                        self.a_exit.updating = True
                        self.a_exit.bgcolor = (175,0,0)
                        self.a_text_ctr = 4
                        
                    #print (check, self.a_text_ctr)   
                        
                    if (check != self.a_text_ctr):
                        #print ('y')
                        self.text_sprite.empty()
                        
                    
                    #gc.collect()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
                    
                    #print (pygame.mouse.get_pos())
                    
                    if self.a_start.rect.collidepoint(pygame.mouse.get_pos()):
                        """for item in self.all_sprite:
                            if isinstance(item, (LetterBox)):
                                item.kill()"""
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.running = 'A'
                        self.command = 'cont_mus'
                        
                    elif self.a_set.rect.collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.running = '2'
                        
                    elif self.a_help.rect.collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.running = '3'
                    
                    elif self.a_exit.rect.collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.running = ''
                    
                    elif self.a_b1.rect.collidepoint(pygame.mouse.get_pos()):
                        self.a_b1.text = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                        self.a_b1.anim_frame = 6
                        self.a_b1.static = False
                        self.a_b1.updating = True
                        
                    elif self.a_b2.rect.collidepoint(pygame.mouse.get_pos()):
                        self.a_b2.text = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                        self.a_b2.anim_frame = 6
                        self.a_b2.static = False
                        self.a_b2.updating = True
                            
                    if self.a_b1.text == self.a_b2.text == 'P':
                        self.command = 'funny'
                        self.running = '9'

        def game_system(): #try your best to put all the input functions here
            game_control()
            
            '''
            (83, 491)
            (462, 526)
            '''
            
            '''if not self.box.rect.collidepoint(pygame.mouse.get_pos()):
                if (pygame.mouse.get_pos()[0]) > self.box.rect.right:
                    self.box.rect.right = pygame.mouse.get_pos()[0]
                elif (pygame.mouse.get_pos()[0]) < self.box.rect.left:
                    self.box.rect.left = pygame.mouse.get_pos()[0]'''
            
            if self.a_text_ctr != 0:
                self.text_sprite.add(LetterBox_t(self.a_text[self.a_text_ctr],black,dt((246, 514)), dt((287,44)),width = 1,f_typo = font_typo[10]))
            
            self.light2.rect.x += 10 * self.sc1_l2_x
            if self.light2.rect.x > 250 or self.light2.rect.x < -2250:
                self.sc1_l2_x *= -1
                
            self.light.rect.x += 10 * self.sc1_l1_x
            if self.light.rect.x > 250 or self.light.rect.x < -5000:
                self.sc1_l1_x *= -1
            
            if self.lasttick != None:
                if self.settings_dict['music']: playmusic(music_array['main_menu_2'], repeat = -1)
                self.lasttick = None
            
            if self.blink_timer + 80 < pygame.time.get_ticks():
                x = list()
                for item in self.all_sprite:
                    if isinstance(item, LetterBox):
                        if item.text in ('B','L','O','K'):
                            x.append(item)
                
                x = random.choice(x)        
                x.color = random.choice((blue,red,green,violet,yellow,gray))
                x.updating = True
                self.blink_timer = pygame.time.get_ticks()
            
            for item in self.text_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            self.all_sprite.draw(self.gameDisplay)
            self.text_sprite.draw(self.gameDisplay)
            
            
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            self.lose = 1
            
            self.blink_timer = pygame.time.get_ticks()
            
            self.a_text = (None,
                           'Start the game',
                           'Change settings',
                           'Show Help Screen',
                           'Exit the game')
            self.a_text_ctr = 0
            
            if self.lasttick != None:
                self.lasttick = pygame.time.get_ticks()
            
            self.text_sprite = pygame.sprite.Group()

            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(CharacBox(bricks, black, *dt2([0,0],[800,600]), width = 1, static=True))
            
            self.a_bg1 = BackgroundBox2((0,0),dt((1600,1600)),(0,50,50),delay = 700,type = 1)
            self.a_bg1.image.set_alpha(100)
            self.all_sprite.add(self.a_bg1)
            
            #self.all_sprite.add(CharacBox(light_blue, black, *dt2([0,0],[800,600]), width = 1, static=True))
            self.light2 = (CharacBox(light_purple, black, *dt2([0,0],[3000,3000]), width = 1, static=True))
            self.light2.rect.topleft = (-1000,-1000)
            self.all_sprite.add(self.light2)
            self.sc1_l2_x = 1
            
            self.light = (CharacBox(light_blue, black, *dt2([0,0],[5000,5000]), width = 1, static=True))
            self.light.rect.topleft = (100,-2000)
            self.all_sprite.add(self.light)
            self.sc1_l1_x = -1
            
            #self.a_bg2 = (BackgroundBox2((0,0),dt((1600,1600)),(0,50,50),delay = 400,type = 2))
            #self.all_sprite.add(self.a_bg2)
            
            movy = 0
            
            self.box = (LetterBox_t('',white,*dt2([235,144], [309,363+movy]),5,100*13))
            
            self.all_sprite.add(self.box)
            
            
            
            self.a_b1 = (LetterBox('B',blue,dt([180+105*0,112+movy]), dt([100,100]),5,100*5,bg_color=(1,1,1)))
            self.all_sprite.add(self.a_b1)
            self.all_sprite.add(LetterBox('L',red,dt([180+105*1,112+movy]), dt([100,100]),5,100*6,bg_color=(1,1,1)))   
            self.all_sprite.add(LetterBox('O',green,dt([180+105*2,112+movy]), dt([100,100]),5,100*7,bg_color=(1,1,1)))
            self.all_sprite.add(LetterBox('K',yellow,dt([180+105*3,112+movy]), dt([100,100]),5,100*8,bg_color=(1,1,1)))
            
            self.a_b2 = (LetterBox('B',violet,dt([180,217+movy]), dt([100,100]),5,100*9,bg_color=(1,1,1)))
            self.all_sprite.add(self.a_b2)
            self.all_sprite.add(LetterBox('L',gray,dt([180+105*1,217+movy]), dt([100,100]),5,100*10,bg_color=(1,1,1)))   
            self.all_sprite.add(LetterBox('O',[0,255,255],dt([180+105*2,217+movy]), dt([100,100]),5,100*11,bg_color=(1,1,1)))
            self.all_sprite.add(LetterBox('K',yellow,dt([180+105*3,217+movy]), dt([100,100]),5,100*12,bg_color=(1,1,1)))
            
            
            self.all_sprite.add(LetterBox('Q',blue,dt([246,327]), dt([38,38]),5,100*19,bg_color=(0,0,75),f_typo = font_typo[6]))
            self.a_start = (LetterBox('Start Game',blue,dt([284,327]), dt([249,38]),5,100*23,bg_color=(1,1,1),f_typo = font_typo[6]))
            
            self.all_sprite.add(self.a_start)
            
            self.all_sprite.add(LetterBox('A',gray,dt([246,372]), dt([38,38]),5,100*20,bg_color=(75,75,75),f_typo = font_typo[6]))
            self.a_set = (LetterBox('Settings',gray,dt([284,372]), dt([249,38]),5,100*24,bg_color=(1,1,1),f_typo = font_typo[6]))
            
            self.all_sprite.add(self.a_set)
            
            self.all_sprite.add(LetterBox('Z',green,dt([246,416]), dt([38,38]),5,100*21,bg_color=(0,75,0),f_typo = font_typo[6]))
            self.a_help = (LetterBox('Help',green,dt([284,416]), dt([249,38]),5,100*25,bg_color=(1,1,1),f_typo = font_typo[6]))
            
            self.all_sprite.add(self.a_help)
            
            self.all_sprite.add(LetterBox('X',red,dt([246,459]), dt([38,38]),5,100*22,bg_color=(75,0,0),f_typo = font_typo[6]))
            self.a_exit = (LetterBox('Exit',red,dt([284,459]), dt([249,38]),5,100*26,bg_color=(1,1,1),f_typo = font_typo[6]))
            
            self.all_sprite.add(self.a_exit)
            
            
        def game_loop():
            
            game_start()
            
            while '1' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
            self.text_sprite.empty()
                
        game_loop()
        
    def Scene2(self):
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                        
                if event.type == pygame.MOUSEMOTION:
                    
                    check = self.a_text_ctr

                    if self.set_music_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sc2_sel = self.a_text_ctr = 1
                        
                    elif self.set_sound_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sc2_sel = self.a_text_ctr = 2
                        
                    elif self.set_fullscreen_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sc2_sel = self.a_text_ctr = 3
                    
                    elif self.set_stretch_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sc2_sel = self.a_text_ctr = 4
                        
                    elif self.set_exit_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sc2_sel = self.a_text_ctr = 5
                        
                    elif self.set_reset_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sc2_sel = self.a_text_ctr = 6
                    
                    #print (check, self.a_text_ctr)   
                        
                    if (check != self.a_text_ctr):
                        #print ('y')
                        self.text_sprite.empty()
                        
                    
                    #gc.collect()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.text_sprite.empty()
                        if self.sc2_sel == 1:
                            self.sc2_sel = self.a_text_ctr = 6
                        else:
                            self.sc2_sel = self.a_text_ctr = (self.sc2_sel-1)
                            self.sc2_sel = self.a_text_ctr = (self.sc2_sel%7)
                    elif event.key == pygame.K_DOWN:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.text_sprite.empty()
                        if self.sc2_sel == 6:
                            self.sc2_sel = self.a_text_ctr = 1
                        else:
                            self.sc2_sel = self.a_text_ctr = (self.sc2_sel+1)
                            self.sc2_sel = self.a_text_ctr = (self.sc2_sel%7)
                            
                    elif event.key == pygame.K_SPACE:
                        
                        if self.sc2_sel == 1:
                            beep_array['beep08'].play() if self.settings_dict['sound'] else None
                            self.set_music_toggle.updating = True
                            if self.set_music_toggle.bgcolor == (0,0,0):
                                self.set_music_toggle.bgcolor = (0,0,100)
                                self.set_music_toggle.text = "On"
                                self.settings_dict['music'] = True
                                if self.settings_dict['music']: playmusic(music_array['main_menu_2'], repeat = -1)
                            else:
                                self.set_music_toggle.bgcolor = (0,0,0)
                                self.set_music_toggle.text = "Off"
                                self.settings_dict['music'] = False
                                stopmusic()
                            json_save(self.settings_dict,os.path.join(game_folder, 'settings.json'))
                            
                        elif self.sc2_sel == 2:
                            self.set_sound_toggle.updating = True
                            if self.set_sound_toggle.bgcolor == (0,0,0):
                                self.set_sound_toggle.bgcolor = (0,100,100)
                                self.set_sound_toggle.text = "On"
                                self.settings_dict['sound'] = True
                                beep_array['beep08'].play() if self.settings_dict['sound'] else None
                            else:
                                self.set_sound_toggle.bgcolor = (0,0,0)
                                self.set_sound_toggle.text = "Off"
                                self.settings_dict['sound'] = False
                            json_save(self.settings_dict,os.path.join(game_folder, 'settings.json'))
                            
                        elif self.sc2_sel == 3:
                            beep_array['beep08'].play() if self.settings_dict['sound'] else None
                            self.set_fullscreen_toggle.updating = True
                            if self.set_fullscreen_toggle.bgcolor == (0,0,0):
                                self.set_fullscreen_toggle.bgcolor = (0,100,0)
                                self.set_fullscreen_toggle.text = "On"
                                self.settings_dict['fullscreen'] = True
                                global sw,sh
                                sw = int(sdIxy.current_w * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_w']
                                sh = int(sdIxy.current_h * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_h']
                                self.gameDisplay = pygame.display.set_mode(size=(sw,sh),flags = pygame.FULLSCREEN|pygame.HWACCEL)
                                
                            else:
                                self.set_fullscreen_toggle.bgcolor = (0,0,0)
                                self.set_fullscreen_toggle.text = "Off"
                                self.settings_dict['fullscreen'] = False
                                sw = int(sdIxy.current_w * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_w']
                                sh = int(sdIxy.current_h * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_h']
                                self.gameDisplay = pygame.display.set_mode(size=(sw,sh))
                            json_save(self.settings_dict,os.path.join(game_folder, 'settings.json'))
                            
                        elif self.sc2_sel == 4:
                            pass #A buggy mess
                            '''beep_array['beep08'].play() if self.settings_dict['sound'] else None
                            self.set_stretch_toggle.updating = True
                            if self.set_stretch_toggle.bgcolor == (0,0,0):
                                self.set_stretch_toggle.bgcolor = (100,100,0)
                                self.set_stretch_toggle.text = "On"
                                self.settings_dict['stretch'] = True
                                fs = pygame.FULLSCREEN|pygame.HWACCEL if self.settings_dict['fullscreen'] else 0
                                sw = int(sdIxy.current_w * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_w']
                                sh = int(sdIxy.current_h * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_h']
                                self.gameDisplay = pygame.display.set_mode(size=(int(sdIxy.current_w * 0.80),int(sdIxy.current_h * 0.80)),flags = fs)
                            else:
                                self.set_stretch_toggle.bgcolor = (0,0,0)
                                self.set_stretch_toggle.text = "Off"
                                self.settings_dict['stretch'] = False
                                fs = pygame.FULLSCREEN|pygame.HWACCEL if self.settings_dict['fullscreen'] else 0
                                sw = int(sdIxy.current_w * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_w']
                                sh = int(sdIxy.current_h * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_h']
                                self.gameDisplay = pygame.display.set_mode(size=(self.settings_dict['screen_w'],self.settings_dict['screen_h']),flags = fs)
                            self.running = '22'
                            json_save(self.settings_dict,os.path.join(game_folder, 'settings.json'))'''
                            
                        
                        elif self.sc2_sel == 5:
                            beep_array['beep08'].play() if self.settings_dict['sound'] else None
                            beep_array['beep08'].play() if self.settings_dict['sound'] else None
                            self.running = '1'
                        
                        elif self.sc2_sel == 6:
                            beep_array['beep08'].play() if self.settings_dict['sound'] else None
                            savedict = {
                                'continue': None,
                                'level': 1,
                                'endless': 0,
                                'classic': 0,
                                'idle': 0,
                                'blackout': 0,
                                }
                        
                            self.save_dict = savedict
                            json_save(self.save_dict)
                            
                    
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1 and self.scene2_click:
                    
                    #print (pygame.mouse.get_pos())
                    
                    self.scene2_click = False
                    
                    if self.set_music_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.set_music_toggle.updating = True
                        if self.set_music_toggle.bgcolor == (0,0,0):
                            self.set_music_toggle.bgcolor = (0,0,100)
                            self.set_music_toggle.text = "On"
                            self.settings_dict['music'] = True
                            if self.settings_dict['music']: playmusic(music_array['main_menu_2'], repeat = -1)
                        else:
                            self.set_music_toggle.bgcolor = (0,0,0)
                            self.set_music_toggle.text = "Off"
                            self.settings_dict['music'] = False
                            stopmusic()
                        json_save(self.settings_dict,os.path.join(game_folder, 'settings.json'))
                        
                        
                    elif self.set_sound_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        self.set_sound_toggle.updating = True
                        if self.set_sound_toggle.bgcolor == (0,0,0):
                            self.set_sound_toggle.bgcolor = (0,100,100)
                            self.set_sound_toggle.text = "On"
                            self.settings_dict['sound'] = True
                            beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        else:
                            self.set_sound_toggle.bgcolor = (0,0,0)
                            self.set_sound_toggle.text = "Off"
                            self.settings_dict['sound'] = False
                        json_save(self.settings_dict,os.path.join(game_folder, 'settings.json'))
                        
                    elif self.set_fullscreen_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.set_fullscreen_toggle.updating = True
                        if self.set_fullscreen_toggle.bgcolor == (0,0,0):
                            self.set_fullscreen_toggle.bgcolor = (0,100,0)
                            self.set_fullscreen_toggle.text = "On"
                            self.settings_dict['fullscreen'] = True
                            sw = int(sdIxy.current_w * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_w']
                            sh = int(sdIxy.current_h * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_h']
                            self.gameDisplay = pygame.display.set_mode(size=(sw,sh),flags = pygame.FULLSCREEN|pygame.HWACCEL)
                            
                        else:
                            self.set_fullscreen_toggle.bgcolor = (0,0,0)
                            self.set_fullscreen_toggle.text = "Off"
                            self.settings_dict['fullscreen'] = False
                            sw = int(sdIxy.current_w * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_w']
                            sh = int(sdIxy.current_h * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_h']
                            self.gameDisplay = pygame.display.set_mode(size=(sw,sh))
                        json_save(self.settings_dict,os.path.join(game_folder, 'settings.json'))
                    
                    elif self.set_stretch_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.set_stretch_toggle.updating = True
                        if self.set_stretch_toggle.bgcolor == (0,0,0):
                            self.set_stretch_toggle.bgcolor = (100,100,0)
                            self.set_stretch_toggle.text = "On"
                            self.settings_dict['stretch'] = True
                            fs = pygame.FULLSCREEN|pygame.HWACCEL if self.settings_dict['fullscreen'] else 0
                            sw = int(sdIxy.current_w * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_w']
                            sh = int(sdIxy.current_h * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_h']
                            self.gameDisplay = pygame.display.set_mode(size=(int(sdIxy.current_w * 0.80),int(sdIxy.current_h * 0.80)),flags = fs)
                        else:
                            self.set_stretch_toggle.bgcolor = (0,0,0)
                            self.set_stretch_toggle.text = "Off"
                            self.settings_dict['stretch'] = False
                            fs = pygame.FULLSCREEN|pygame.HWACCEL if self.settings_dict['fullscreen'] else 0
                            sw = int(sdIxy.current_w * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_w']
                            sh = int(sdIxy.current_h * 0.80) if self.settings_dict['stretch'] else self.settings_dict['screen_h']
                            self.gameDisplay = pygame.display.set_mode(size=(self.settings_dict['screen_w'],self.settings_dict['screen_h']),flags = fs)
                        self.running = '22'
                        json_save(self.settings_dict,os.path.join(game_folder, 'settings.json'))
                        
                    elif self.set_exit_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.running = '1'
                        
                    elif self.set_reset_toggle.rect.collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        savedict = {
                                'continue': None,
                                'level': 1,
                                'endless': 0,
                                'classic': 0,
                                'idle': 0,
                                'blackout': 0,
                                }
                        
                        self.save_dict = savedict
                        json_save(self.save_dict)
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    self.scene2_click = True

        def game_system(): #try your best to put all the input functions here
            game_control()
            
            '''
            (83, 491)
            (462, 526)
            '''
            
            '''if not self.box.rect.collidepoint(pygame.mouse.get_pos()):
                if (pygame.mouse.get_pos()[0]) > self.box.rect.right:
                    self.box.rect.right = pygame.mouse.get_pos()[0]
                elif (pygame.mouse.get_pos()[0]) < self.box.rect.left:
                    self.box.rect.left = pygame.mouse.get_pos()[0]'''
            
            if self.a_text_ctr != 0:
                self.text_sprite.add(LetterBox_t(self.a_text[self.a_text_ctr],black,dt((246, 514)), dt((287,44)),width = 1,f_typo = font_typo[10]))
            
            if (self.sc2_cur != self.sc2_sel) and (self.sc2_sel != 0):
                
                self.sc2_cur = self.sc2_sel
                
                self.set_exit_toggle.updating = self.set_reset_toggle.updating = self.set_music_toggle.updating = self.set_sound_toggle.updating = self.set_fullscreen_toggle.updating = self.set_stretch_toggle.updating = True
                self.set_exit_toggle.color = self.set_reset_toggle.color = self.set_music_toggle.color = self.set_sound_toggle.color = self.set_fullscreen_toggle.color = self.set_stretch_toggle.color = white
                
                    
                if self.sc2_cur == 1:
                    self.set_music_toggle.updating = True
                    self.set_music_toggle.color = (0,0,175)
                    self.a_text_ctr = 1
                    
                if self.sc2_cur == 2:
                    self.set_sound_toggle.updating = True
                    self.set_sound_toggle.color = (0,175,175)
                    self.a_text_ctr = 2
                    
                if self.sc2_cur == 3:
                    self.set_fullscreen_toggle.updating = True
                    self.set_fullscreen_toggle.color = (0,175,0)
                    self.a_text_ctr = 3
                
                if self.sc2_cur == 4:
                    self.set_stretch_toggle.updating = True
                    self.set_stretch_toggle.color = (175,175,0)
                    self.a_text_ctr = 4
                    
                if self.sc2_cur == 5:
                    self.set_exit_toggle.updating = True
                    self.set_exit_toggle.color = (175,0,0)
                    self.a_text_ctr = 5
                    
                if self.sc2_cur == 6:
                    self.set_reset_toggle.updating = True
                    self.set_reset_toggle.color = (175,0,175)
                    self.a_text_ctr = 6
            
            for item in self.text_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            self.all_sprite.draw(self.gameDisplay)
            self.text_sprite.draw(self.gameDisplay)
            
            
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            self.sc2_cur = self.sc2_sel = 0
            
            self.a_text = (None,
                           'Play Music on Game',
                           'Play Sounds on Game',
                           'Set Game FullScreen',
                           'Set Game Resolution',
                           "Return to Main Menu",
                           "Reset Game Progress")
            self.a_text_ctr = 0
            self.scene2_click = True
            
            self.text_sprite = pygame.sprite.Group()

            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(CharacBox(bg_fade, black, *dt2([0,0],[800,600]), width = 1, static=True))
            
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,50,50)))
            
            
            
            #self.a_bg2 = (BackgroundBox2((0,0),dt((1600,1600)),(0,50,50),delay = 400,type = 2))
            #self.all_sprite.add(self.a_bg2)
            
            movy = 0
            
            self.box = (LetterBox_t('',white,*dt2([235,144], [309,363+movy]),5))
            
            self.all_sprite.add(LetterBox_t('Settings',black,dt([246,161]), dt([287,59]),5,100*5,f_typo = font_typo[14]))
            #self.all_sprite.add(self.box)
            self.all_sprite.add(CharacBox(dlg2, black, *dt2([235,104],[309,463]), width = 1, static=True))
                        
            self.all_sprite.add(LetterBox('Music',black,dt([246,244]), dt([201,44]),5,100*10,f_typo = font_typo[6]))
            self.set_music_toggle = (LetterBox('On' if self.settings_dict['music'] else 'Off',white,dt([445,244]), dt([78,44]),5,100*10,f_typo = font_typo[6]))
            self.set_music_toggle.bgcolor = (0,0,100) if self.settings_dict['music'] else (0,0,0)
            self.all_sprite.add(self.set_music_toggle)
            
            self.all_sprite.add(LetterBox('Sound',black,dt([246,293]), dt([201,44]),5,100*12,f_typo = font_typo[6]))
            self.set_sound_toggle = (LetterBox('On' if self.settings_dict['sound'] else 'Off',white,dt([445,293]), dt([78,44]),5,100*12,f_typo = font_typo[6]))
            self.set_sound_toggle.bgcolor = (0,100,100) if self.settings_dict['sound'] else (0,0,0)
            self.all_sprite.add(self.set_sound_toggle)
            
            self.all_sprite.add(LetterBox('Full Screen',black,dt([246,353]), dt([201,44]),5,100*10,f_typo = font_typo[6]))
            self.set_fullscreen_toggle = (LetterBox('On' if self.settings_dict['fullscreen'] else 'Off',white,dt([445,353]), dt([78,44]),5,100*10,f_typo = font_typo[6]))
            self.set_fullscreen_toggle.bgcolor = (0,100,0) if self.settings_dict['fullscreen'] else (0,0,0)
            self.all_sprite.add(self.set_fullscreen_toggle)
            
            self.all_sprite.add(LetterBox('Stretch',black,dt([246,401]), dt([201,44]),5,100*12,f_typo = font_typo[6]))
            self.set_stretch_toggle = (LetterBox('On' if self.settings_dict['stretch'] else 'Off',white,dt([445,401]), dt([78,44]),5,100*12,f_typo = font_typo[6]))
            self.set_stretch_toggle.bgcolor = (100,100,0) if self.settings_dict['stretch'] else (0,0,0)
            self.all_sprite.add(self.set_stretch_toggle)
            
            self.set_reset_toggle = (LetterBox('Reset',white,dt([259,460]), dt([77,29]),5,100*14,f_typo = font_typo[2]))
            self.all_sprite.add(self.set_reset_toggle)
            
            self.set_exit_toggle = (LetterBox('Exit',white,dt([444,460]), dt([77,29]),5,100*14,f_typo = font_typo[2]))
            self.all_sprite.add(self.set_exit_toggle)
            
            
        def game_loop():
            
            game_start()
            
            while (self.running == '2'):
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
            self.text_sprite.empty()
                
        game_loop()
    
    def Scene3(self):
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                        
                if event.type == pygame.KEYDOWN:   
                    if event.key == pygame.K_SPACE:
                       self.running = '1'

        def game_system(): #try your best to put all the input functions here
            game_control()
                
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            self.all_sprite.draw(self.gameDisplay)
            self.text_sprite.draw(self.gameDisplay)
            
            
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(CharacBox(bg_fade, black, *dt2([0,0],[800,600]), width = 1, static=True))
            
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,50,50)))
            
            self.all_sprite.add(CharacBox(tutorial, black, *dt2([0,0],[800,600]), width = 1))
            self.all_sprite.add(LetterBox_t('',white,*dt2([23,83], [760,406]),5))
            
        def game_loop():
            
            game_start()
            
            while (self.running == '3'):
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
            self.text_sprite.empty()
                
        game_loop()
    
    def SceneA(self):
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                        
                if event.type == pygame.MOUSEMOTION:
                    
                    check = self.a_text_ctr
                 
                    if self.s3_story.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sel_slide = self.a_text_ctr = 1
                        
                    elif self.s3_endl.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sel_slide = self.a_text_ctr = 2
                        
                    elif self.s3_quick.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sel_slide = self.a_text_ctr = 3
                        
                    elif self.s3_idle.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sel_slide = self.a_text_ctr = 4
                        
                    elif self.s3_black.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sel_slide = self.a_text_ctr = 5
                    
                    elif self.save_dict['continue'] != None:
                        if self.s3_cont.rect.collidepoint(pygame.mouse.get_pos()):
                            self.sel_slide = self.a_text_ctr = 6
                            
                    if (check != self.a_text_ctr):
                        #print ('y')
                        self.text_sprite.empty()
                    
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_UP:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.text_sprite.empty()
                        if self.sel_slide == 1:
                            if self.save_dict['continue'] != None:
                                self.sel_slide = self.a_text_ctr = 6
                            else: 
                                self.sel_slide = self.a_text_ctr = 5
                        else:
                            self.sel_slide = self.a_text_ctr = (self.sel_slide-1)
                            
                    elif event.key == pygame.K_DOWN:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.text_sprite.empty()
                        if self.sel_slide == 5:
                            if self.save_dict['continue'] != None:
                                self.sel_slide = self.a_text_ctr = 6
                            else: 
                                self.sel_slide = self.a_text_ctr = 1
                        else:
                            self.sel_slide = self.a_text_ctr = (self.sel_slide+1)
                            self.sel_slide = self.a_text_ctr = (self.sel_slide%6)
                    
                    elif event.key == pygame.K_ESCAPE:
                        self.running = '1'
                    elif event.key == pygame.K_q and self.save_dict['continue'] != None:
                        self.command = 'play_stage'
                        self.running = '9'
                    elif event.key == pygame.K_1:
                        stopmusic()
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.running = 'B'
                    elif event.key == pygame.K_2:
                        stopmusic()
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.command = 'endless'
                        self.running = '9'
                    elif event.key == pygame.K_3:
                        stopmusic()
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.command = 'classic'
                        self.running = '9'
                        self.classic_score = 0
                    elif event.key == pygame.K_4:
                        stopmusic()
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.command = 'idle'
                        self.running = '9'
                    elif event.key == pygame.K_5:
                        stopmusic()
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.command = 'blackout'
                        self.running = '9'
                    elif event.key == pygame.K_SPACE:
                        if self.cur_slide != None:
                            if self.cur_slide == 6 and self.save_dict['continue'] != None:
                                self.command = 'play_stage'
                                self.running = '9'
                            if self.cur_slide == 1:
                                stopmusic()
                                beep_array['beep18'].play() if self.settings_dict['sound'] else None
                                self.running = 'B'
                            if self.cur_slide == 2:
                                stopmusic()
                                self.command = 'endless'
                                self.running = '9'
                            if self.cur_slide == 3:
                                stopmusic()
                                beep_array['beep18'].play() if self.settings_dict['sound'] else None
                                self.command = 'classic'
                                self.running = '9'
                                self.classic_score = 0
                            if self.cur_slide == 4:
                                stopmusic()
                                beep_array['beep18'].play() if self.settings_dict['sound'] else None
                                self.command = 'idle'
                                self.running = '9'
                            if self.cur_slide == 5:
                                stopmusic()
                                beep_array['beep18'].play() if self.settings_dict['sound'] else None
                                self.command = 'blackout'
                                self.running = '9'
                    
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1 and self.scene2_click:
                    
                    #print (pygame.mouse.get_pos())
                    
                    self.scene2_click = False
                    
                    self.s3_story.updating = self.s3_endl.updating = self.s3_quick.updating = self.s3_idle.updating = self.s3_black.updating = True
                    self.s3_story.bgcolor = self.s3_endl.bgcolor = self.s3_quick.bgcolor = self.s3_idle.bgcolor = self.s3_black.bgcolor = (1,1,1)
                    if self.save_dict['continue'] != None:
                        self.s3_cont.updating = True
                        self.s3_cont.bgcolor = (1,1,1)
                    
                    if self.s3_story.rect.collidepoint(pygame.mouse.get_pos()):
                        self.s3_story.updating = True
                        self.s3_story.bgcolor = (75,75,0)
                        self.a_text_ctr = 1
                        stopmusic()
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.running = 'B'
                        
                    elif self.s3_endl.rect.collidepoint(pygame.mouse.get_pos()):
                        self.s3_endl.updating = True
                        self.s3_endl.bgcolor = (75,75,75)
                        self.a_text_ctr = 2
                        stopmusic()
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.command = 'endless'
                        self.running = '9'
                        
                    elif self.s3_quick.rect.collidepoint(pygame.mouse.get_pos()):
                        self.s3_quick.updating = True
                        self.s3_quick.bgcolor = (0,0,75)
                        self.a_text_ctr = 3
                        stopmusic()
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.command = 'classic'
                        self.running = '9'
                        self.classic_score = 0
                        
                    elif self.s3_idle.rect.collidepoint(pygame.mouse.get_pos()):
                        self.s3_idle.updating = True
                        self.s3_idle.bgcolor = (0,75,75)
                        self.a_text_ctr = 4
                        stopmusic()
                        self.command = 'idle'
                        self.running = '9'
                        
                    elif self.s3_black.rect.collidepoint(pygame.mouse.get_pos()):
                        self.s3_black.updating = True
                        self.s3_black.bgcolor = (75,25,50)
                        self.a_text_ctr = 5
                        stopmusic()
                        self.command = 'blackout'
                        self.running = '9'
                        
                    elif self.s3_return.rect.collidepoint(pygame.mouse.get_pos()):
                        self.s3_return.updating = True
                        self.s3_return.bgcolor = (75,25,50)
                        self.a_text_ctr = 6
                        self.running = '1'
                        
                    elif self.save_dict['continue'] != None:
                        if self.s3_cont.rect.collidepoint(pygame.mouse.get_pos()):
                            self.s3_cont.updating = True
                            self.s3_cont.bgcolor = (0,0,75)
                            self.command = 'play_stage'
                            self.running = '9'
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    self.scene2_click = True

        def game_system(): #try your best to put all the input functions here
            game_control()
            
            '''
            (83, 491)
            (462, 526)
            '''
            
            '''if not self.box.rect.collidepoint(pygame.mouse.get_pos()):
                if (pygame.mouse.get_pos()[0]) > self.box.rect.right:
                    self.box.rect.right = pygame.mouse.get_pos()[0]
                elif (pygame.mouse.get_pos()[0]) < self.box.rect.left:
                    self.box.rect.left = pygame.mouse.get_pos()[0]'''
            
            if self.a_text_ctr != 0:
                self.text_sprite.add(LetterBox_t(self.a_text[self.a_text_ctr],black,dt((55, 515)), dt((287,44)),width = 1,f_typo = font_typo[10]))
            
            
            if (self.cur_slide != self.sel_slide) and (self.sel_slide != 0) or self.fresha_start:
                self.slide_group.empty()
                
                self.s3_story.updating = self.s3_endl.updating = self.s3_quick.updating = self.s3_idle.updating = self.s3_black.updating = True
                self.s3_story.color = self.s3_endl.color = self.s3_quick.color = self.s3_idle.color = self.s3_black.color = white
                
                
                if self.save_dict['continue'] != None:
                    self.s3_cont.updating = True
                    self.s3_cont.color = white
                    
                if not self.fresha_start: self.cur_slide = self.sel_slide
                
                self.fresha_start = False
                
                if self.cur_slide == 1:
                    
                    self.s3_story.updating = True
                    self.s3_story.color = (175,175,0)
                    
                    self.slide_group.add(LetterBox_t('Story Mode',black,dt([364,146]), dt([385,62]),5 ,f_typo = font_typo[14]))
                    self.slide_group.add(CharacBox(mode_banners[self.cur_slide-1], black, dt((363,215)), dt((386,140)),width = 1))
                    self.slide_group.add(LetterBox_t('Play the Blok Blok Tournament',black,dt([364,359]), dt([385,62]),5,bg_color=(0,0,50),f_typo = font_typo[10]))
                    self.slide_group.add(LetterBox_t('Unlocked Levels: {0}'.format(self.save_dict['level']),black,dt([364,427]), dt([385,62]),5,bg_color=(50,50,0),f_typo = font_typo[10]))
                
                elif self.cur_slide == 2:
                    
                    self.s3_endl.updating = True
                    self.s3_endl.color = (175,175,175)
                    
                    self.slide_group.add(LetterBox_t('Endless Mode',black,dt([364,146]), dt([385,62]),5 ,f_typo = font_typo[14]))
                    self.slide_group.add(CharacBox(mode_banners[self.cur_slide-1], black, dt((363,215)), dt((386,140)),width = 1))
                    self.slide_group.add(LetterBox_t('Survive the Best you can',black,dt([364,359]), dt([385,62]),5,bg_color=(0,0,50),f_typo = font_typo[10]))
                    self.slide_group.add(LetterBox_t('Best Score: {0}'.format(self.save_dict['endless']),black,dt([364,427]), dt([385,62]),5,bg_color=(50,50,0),f_typo = font_typo[10]))
               
                elif self.cur_slide == 3:
                    
                    self.s3_quick.updating = True
                    self.s3_quick.color = (0,0,175)
                
                    self.slide_group.add(LetterBox_t('Quick Play Mode',black,dt([364,146]), dt([385,62]),5 ,f_typo = font_typo[14]))
                    self.slide_group.add(CharacBox(mode_banners[self.cur_slide-1], black, dt((363,215)), dt((386,140)),width = 1))
                    self.slide_group.add(LetterBox_t('Play randomly generated levels',black,dt([364,359]), dt([385,62]),5,bg_color=(0,0,50),f_typo = font_typo[10]))
                    self.slide_group.add(LetterBox_t('Best Score: {0}'.format(self.save_dict['classic']),black,dt([364,427]), dt([385,62]),5,bg_color=(50,50,0),f_typo = font_typo[10]))

                elif self.cur_slide == 4:
                    
                    self.s3_idle.updating = True
                    self.s3_idle.color = (0,175,175)
                
                    self.slide_group.add(LetterBox_t('Idle Mode',black,dt([364,146]), dt([385,62]),5 ,f_typo = font_typo[14]))
                    self.slide_group.add(CharacBox(mode_banners[self.cur_slide-1], black, dt((363,215)), dt((386,140)),width = 1))
                    self.slide_group.add(LetterBox_t('Play Blok Blok with AutoClick',black,dt([364,359]), dt([385,62]),5,bg_color=(0,0,50),f_typo = font_typo[10]))
                    self.slide_group.add(LetterBox_t('Best Score: {0}'.format(self.save_dict['idle']),black,dt([364,427]), dt([385,62]),5,bg_color=(50,50,0),f_typo = font_typo[10]))
                
                elif self.cur_slide == 5:
                    
                    self.s3_black.updating = True
                    self.s3_black.color = (175,125,150)
                    
                    self.slide_group.add(LetterBox_t('Black Out Mode',black,dt([364,146]), dt([385,62]),5 ,f_typo = font_typo[14]))
                    self.slide_group.add(CharacBox(mode_banners[self.cur_slide-1], black, dt((363,215)), dt((386,140)),width = 1))
                    self.slide_group.add(LetterBox_t('Can you play with no Lights?',black,dt([364,359]), dt([385,62]),5,bg_color=(0,0,50),f_typo = font_typo[10]))
                    self.slide_group.add(LetterBox_t('Best Score: {0}'.format(self.save_dict['blackout']),black,dt([364,427]), dt([385,62]),5,bg_color=(50,50,0),f_typo = font_typo[10]))
                
                elif self.cur_slide == 6 and self.save_dict['continue'] != None:
                    
                    self.s3_cont.updating = True
                    self.s3_cont.color = (0,0,175)
                    
                    self.slide_group.add(LetterBox_t('Continue',black,dt([364,146]), dt([385,62]),5 ,f_typo = font_typo[14]))
                    self.slide_group.add(CharacBox(mode_banners[0], black, dt((363,215)), dt((386,140)),width = 1))
                    self.slide_group.add(LetterBox_t('Play the Blok Blok Tournament',black,dt([364,359]), dt([385,62]),5,bg_color=(0,0,50),f_typo = font_typo[10]))
                    self.slide_group.add(LetterBox_t('Level: {0} || Stage: {1}'.format(self.save_dict['continue'][0], self.save_dict['continue'][1]),black,dt([364,427]), dt([385,62]),5,bg_color=(50,50,0),f_typo = font_typo[10]))
                
            
            for item in self.text_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            for item in self.slide_group:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            self.all_sprite.draw(self.gameDisplay)
            self.text_sprite.draw(self.gameDisplay)
            self.slide_group.draw(self.gameDisplay)
            
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            change_dif("reset")
            if self.settings_dict['music'] and not self.command == 'cont_mus': 
                playmusic(music_array['main_menu_2'], repeat = -1)
            
            self.command = ''
            
            self.fresha_start = True
            self.slide_group = pygame.sprite.Group()
            
            self.a_text = (None,
                           'Play New Story Mode',
                           'Play Endless Mode',
                           'Play Quick Game',
                           "Play Idle Mode",
                           "Play BlackOut Mode",
                           "Continue Story Mode")
            self.a_text_ctr = 0
            self.scene2_click = True
            
            self.text_sprite = pygame.sprite.Group()

            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(CharacBox(bg_fade, black, *dt2([0,0],[800,600]), width = 1, static=True))
            
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,50,50)))
            
            self.all_sprite.add(LetterBox('B',red,*dt2([483,69], [65,71]),5,100*6,f_typo=font_typo[11]))
            self.all_sprite.add(LetterBox('L',green,*dt2([549,69], [65,71]),5,100*7,f_typo=font_typo[11]))
            self.all_sprite.add(LetterBox('O',blue,*dt2([615,69], [65,71]),5,100*8,f_typo=font_typo[11]))
            self.all_sprite.add(LetterBox('K',white,*dt2([681,69], [65,71]),5,100*9,f_typo=font_typo[11]))
            
            if self.save_dict['continue'] != None:
                self.all_sprite.add(LetterBox('Q',yellow,dt([54,215+15]), dt([40,40]),5,100*6,bg_color=(75,75,0),f_typo = font_typo[6]))
                self.s3_cont = (LetterBox('Continue',white,dt([94,215+15]), dt([126,40]),5,100*9,bg_color=(1,1,1),f_typo = font_typo[6]))
                self.all_sprite.add(self.s3_cont)
                
                self.s3_story = (LetterBox('Story Mode',white,dt([220,215+15]), dt([128,40]),5,100*9,bg_color=(1,1,1),f_typo = font_typo[6]))
                self.all_sprite.add(self.s3_story)
            else:
                self.all_sprite.add(LetterBox('1',yellow,dt([54,215+15]), dt([40,40]),5,100*7,bg_color=(75,75,0),f_typo = font_typo[6]))
                self.s3_story = (LetterBox('Story Mode',white,dt([94,215+15]), dt([253,40]),5,100*9,bg_color=(1,1,1),f_typo = font_typo[6]))
                self.all_sprite.add(self.s3_story)
            
            self.all_sprite.add(LetterBox('2',gray,dt([54,260+15]), dt([40,40]),5,100*8,bg_color=(75,75,75),f_typo = font_typo[6]))
            self.s3_endl = (LetterBox('Zen Survival',white,dt([94,260+15]), dt([253,40]),5,100*10,bg_color=(1,1,1),f_typo = font_typo[6]))
            self.all_sprite.add(self.s3_endl)
            
            self.all_sprite.add(LetterBox('3',blue,dt([54,305+15]), dt([40,40]),5,100*9,bg_color=(0,0,75),f_typo = font_typo[6]))
            self.s3_quick = (LetterBox('Quick Game',white,dt([94,305+15]), dt([253,40]),5,100*11,bg_color=(1,1,1),f_typo = font_typo[6]))
            self.all_sprite.add(self.s3_quick)
            
            self.all_sprite.add(LetterBox('4',green,dt([54,350+15]), dt([40,40]),5,100*11,bg_color=(0,75,75),f_typo = font_typo[6]))
            self.s3_idle = (LetterBox('Idle Mode',white,dt([94,350+15]), dt([253,40]),5,100*13,bg_color=(1,1,1),f_typo = font_typo[6]))
            self.all_sprite.add(self.s3_idle)
            
            self.all_sprite.add(LetterBox('5',(200,100,150),dt([54,395+15]), dt([40,40]),5,100*12,bg_color=(75,25,50),f_typo = font_typo[6]))
            self.s3_black = (LetterBox('Black Out',white,dt([94,395+15]), dt([253,40]),5,100*14,bg_color=(1,1,1),f_typo = font_typo[6]))
            self.all_sprite.add(self.s3_black)
            
            self.all_sprite.add(LetterBox('Esc',(200,0,0),dt([54,440+15]), dt([40,40]),5,100*13,bg_color=(75,0,0),f_typo = font_typo[6]))
            self.s3_return = (LetterBox('Exit',white,dt([94,440+15]), dt([253,40]),5,100*15,bg_color=(1,1,1),f_typo = font_typo[6]))
            self.all_sprite.add(self.s3_return)
            #self.a_bg2 = (BackgroundBox2((0,0),dt((1600,1600)),(0,50,50),delay = 400,type = 2))
            #self.all_sprite.add(self.a_bg2)
            
            movy = 0
            
            self.box = (LetterBox_t('',white,*dt2([43,143], [314,366+movy]),5))
            
            self.all_sprite.add(LetterBox('Play Game',black,dt([54,161]), dt([287,59]),5,100*5,f_typo = font_typo[4]))
            self.all_sprite.add(self.box)
            
                        
            
            
        def game_loop():
            
            game_start()
            
            while (self.running == 'A'):
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
            self.text_sprite.empty()
                
        game_loop()



    def SceneB(self):
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.running = '9'
                        self.command = 'club_stillframe'
                    if event.key == pygame.K_w and self.save_dict['level'] > 1:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.running = '9'
                        self.command = 'under_stillframe'
                    if event.key == pygame.K_e and self.save_dict['level'] > 2:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.running = '9'
                        self.command = 'crib_stillframe'
                    if event.key == pygame.K_ESCAPE:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        self.running = 'A'
                        
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:
                    if pygame.Rect(*dt((25,26)),*dt((245,549))).collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.running = '9'
                        self.command = 'club_stillframe'
                    if pygame.Rect(*dt((270, 26)),*dt((245,549))).collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.running = '9'
                        self.command = 'under_stillframe'
                    if pygame.Rect(*dt((510, 26)),*dt((245,549))).collidepoint(pygame.mouse.get_pos()):
                        beep_array['beep08'].play() if self.settings_dict['sound'] else None
                        self.running = '9'
                        self.command = 'crib_stillframe'
                    
                
                '''if event.type == pygame.MOUSEMOTION:
                    if pygame.Rect(*dt((25,26)),*dt((245,549))).collidepoint(pygame.mouse.get_pos()):
                        if self.level_prev == None:
                            print ('y')
                            self.level_prev = CharacBox(bg_neon['club'][0], black, dt((25,25)), dt((750,550)),width = 1,static=True)
                            self.all_sprite.add(self.level_prev)
                        else:
                            self.level_prev.kill()
                            self.level_prev = None
                            self.level_prev = CharacBox(bg_neon['club'][0], black, dt((25,25)), dt((750,550)),width = 1,static=True)
                            self.all_sprite.add(self.level_prev)
                            
                    elif pygame.Rect(*dt((270, 26)),*dt((245,549))).collidepoint(pygame.mouse.get_pos()):
                        if self.level_prev == None:
                            print ('y')
                            self.level_prev = CharacBox(bg_neon['club'][1], black, dt((25,25)), dt((750,550)),width = 1,static=True)
                            self.all_sprite.add(self.level_prev)
                        else:
                            self.level_prev.kill()
                            self.level_prev = None
                            self.level_prev = CharacBox(bg_neon['club'][1], black, dt((25,25)), dt((750,550)),width = 1,static=True)
                            self.all_sprite.add(self.level_prev)
                            
                    elif pygame.Rect(*dt((510, 26)),*dt((245,549))).collidepoint(pygame.mouse.get_pos()):
                        if self.level_prev == None:
                            print ('y')
                            self.level_prev = CharacBox(bg_neon['club'][2], black, dt((25,25)), dt((750,550)),width = 1,static=True)
                            self.all_sprite.add(self.level_prev)
                        else:
                            self.level_prev.kill()
                            self.level_prev = None
                            self.level_prev = CharacBox(bg_neon['club'][2], black, dt((25,25)), dt((750,550)),width = 1,static=True)
                            self.all_sprite.add(self.level_prev)
                            
                    else:
                        if self.level_prev != None:
                            self.level_prev.kill()
                            self.level_prev = None
                        
                    
                gc.collect()'''
                            
            
        def game_system(): #try your best to put all the input functions here
            game_control()
            
            if self.lasttick + 1500 < pygame.time.get_ticks():
                self.lasttick = pygame.time.get_ticks()
                self.border2.anim_frame = 6
                self.border2.updating = True
                
                '''
            if self.lasttick2 + 750 < pygame.time.get_ticks():
                
                self.lasttick2 = pygame.time.get_ticks()
                if random.randrange(1,100) > 50:
                    self.level_1.color = yellow
                    self.level_2.width = 5
                    self.level_1.updating = True
                    
                if random.randrange(1,100) > 75:
                    self.level_2.anim_frame = 2
                    self.level_2.static = False
                    self.level_2.updating = True
                if random.randrange(1,100) > 75:
                    self.level_3.anim_frame = 2
                    self.level_3.static = False
                    self.level_3.updating = True
                    '''
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            
            self.all_sprite.draw(self.gameDisplay)
            
            self.text_sprite.draw(self.gameDisplay)
                    
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            #self.level_prev = None
            
            self.lasttick = pygame.time.get_ticks()
            self.lasttick2 = pygame.time.get_ticks()

            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(CharacBox(bg_fade, black, *dt2([0,0],[800,600]), width = 1, static=True))
            
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,25),delay = 700))
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,25,25),delay = 400))
            
            #self.border = BorderBox(white, [30-5,30-5],[750,550], 3)
            self.border2 = BorderBox(white, *dt2([30-5-5,30-5-5],[760,560]), 3,6) 
            
            self.all_sprite.add(self.border2)
            #self.all_sprite.add(self.border)

        
            self.level_1 = CharacBox(background_level[0], black, dt((25,25)), dt((750,550)),width = 1)
            self.level_2 = CharacBox(background_level[1], black, dt((25,25)), dt((750,550)),width = 1)
            self.level_3 = CharacBox(background_level[2], black, dt((25,25)), dt((750,550)),width = 1)
        
            self.all_sprite.add(self.level_1)
            self.all_sprite.add(self.level_2)
            self.all_sprite.add(self.level_3)
            
            self.all_sprite.add(LetterBox_t("Azure",black,dt([50,183]), dt([200,80]),5,f_typo = font_typo[11],f_color = font_color[1]))
            self.all_sprite.add(LetterBox_t("Club",black,dt([50,243]), dt([200,80]),5,f_typo = font_typo[11],f_color = font_color[1]))
            
            self.all_sprite.add(LetterBox_t("Under",black,dt([300,183]), dt([200,80]),5,f_typo = font_typo[11],f_color = font_color[1] if self.save_dict['level'] > 1 else font_color[2]))
            self.all_sprite.add(LetterBox_t("scene",black,dt([300,243]), dt([200,80]),5,f_typo = font_typo[11],f_color = font_color[1] if self.save_dict['level'] > 1 else font_color[2]))
            
            self.all_sprite.add(LetterBox_t("Crib",black,dt([547,183]), dt([200,80]),5,f_typo = font_typo[11],f_color = font_color[1] if self.save_dict['level'] > 2 else font_color[2]))
            self.all_sprite.add(LetterBox_t("Elite",black,dt([547,243]), dt([200,80]),5,f_typo = font_typo[11],f_color = font_color[1] if self.save_dict['level'] > 2 else font_color[2]))
            
            self.all_sprite.add(LetterBox_t("Raw Energy",black,dt([50,325]), dt([200,44]),5,f_typo = font_typo[6],f_color = font_color[1]))
            self.all_sprite.add(LetterBox_t("Tricks",black,dt([300,325]), dt([200,44]),5,f_typo = font_typo[6],f_color = font_color[1] if self.save_dict['level'] > 1 else font_color[2]))
            self.all_sprite.add(LetterBox_t("Uncertainty",black,dt([547,325]), dt([200,44]),5,f_typo = font_typo[6],f_color = font_color[1] if self.save_dict['level'] > 2 else font_color[2]))
            
            self.all_sprite.add(LetterBox_t('Q',blue,dt([125,404]), dt([50,50]),5,bg_color=(0,0,75),f_typo = font_typo[10]))
            
            if self.save_dict['level'] > 1:
                self.all_sprite.add(LetterBox_t('W',green,dt([375,404]), dt([50,50]),5,bg_color=(0,75,0),f_typo = font_typo[10]))
            if self.save_dict['level'] > 2:
                self.all_sprite.add(LetterBox_t('E',violet,dt([622,404]), dt([50,50]),5,bg_color=(75,0,75),f_typo = font_typo[10]))
            
            self.all_sprite.add(LetterBox_t('Esc',red,dt([693,530]), dt([46,24]),5,1000,bg_color=(75,0,0),f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Quit',black,dt([715,553]), dt([46,24]),5,1000,bg_color=(75,0,0),f_typo=font_typo[8]))
            
            self.all_sprite.add(LetterBox_t("Story Mode",black,dt([218,34]), dt([380,41]),5,f_typo = font_typo[12],f_color = font_color[1]))
            
            
            if self.settings_dict['music']: playmusic(music_array['select_level'], repeat=-1)
            
        def game_loop():
            
            game_start()
            
            while 'B' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
            del self.level_1
                
        game_loop()

    def SceneC(self):

        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1):
                    beep_array['beep18'].play() if self.settings_dict['sound'] else None
                    self.running = '9'
                    self.command = self.command_echo.replace('stillframe', 'dialogue')
                    self.command_echo = ''
                            
            
        def game_system(): #try your best to put all the input functions here
            game_control()
            
            if self.lasttick + 1500 < pygame.time.get_ticks():
                self.lasttick = pygame.time.get_ticks()
                self.border2.anim_frame = 6
                self.border2.updating = True
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            
            self.all_sprite.draw(self.gameDisplay)
                    
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            self.lasttick = pygame.time.get_ticks()

            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(CharacBox(bg_fade, black, *dt2([0,0],[800,600]), width = 1, static=True))
            
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,25),delay = 700))
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,25,25),delay = 400))
            
            #self.border = BorderBox(white, [30-5,30-5],[750,550], 3)
            self.border2 = BorderBox(self.c_frame_color, dt([30-5-5,30-5-5]),dt([760,560]), 3,6) 
            
            self.all_sprite.add(self.border2)
            #self.all_sprite.add(self.border)
 
            self.level_1 = CharacBox(self.c_still_frame, black, dt((25,25)), dt((750,550)),width = 1)

        
            self.all_sprite.add(self.level_1)

            
            self.all_sprite.add(LetterBox_t(self.c_stage[0],black,dt([50,183]), dt([200,80]),5,f_typo = font_typo[11],f_color = font_color[1]))
            self.all_sprite.add(LetterBox_t(self.c_stage[1],black,dt([50,243]), dt([200,80]),5,f_typo = font_typo[11],f_color = font_color[1]))
            
            self.all_sprite.add(LetterBox_t(self.c_stage_tagline,black,dt([50,325]), dt([200,44]),5,f_typo = font_typo[6],f_color = font_color[1]))
            
            self.all_sprite.add(LetterBox_t("Story Mode",black,dt([218,34]), dt([380,41]),5,f_typo = font_typo[12],f_color = font_color[1]))
            
            self.all_sprite.add(LetterBox_t("Press space to continue",black,dt([282,527]), dt([292,30]),5,f_typo = font_typo[6],f_color = font_color[1]))
            
            
        def game_loop():
            
            game_start()
            
            while 'C' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
                
        game_loop()

    def SceneD(self):
        
        self.y_message_ctr = 0
        self.y_message_ctr_max = len(self.d_messages)
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1):
                        beep_array['beep20'].play() if self.settings_dict['sound'] else None
                        self.border2.anim_frame = 6
                        self.border2.updating = True
                        if self.y_message_ctr < self.y_message_ctr_max:
                            self.text_sprite.empty()
                            self.y_message_ctr += 1
                        elif self.command_echo == 'end':
                            self.running = 'A'
                            self.command_echo = ''
                            
                        else:
                            self.running = '9'
                            self.command = 'play_stage'

        def game_system(): #try your best to put all the input functions here
            game_control()
            
            #if self.lasttick != None:
            #        if self.settings_dict['music']: playmusic(music_array['main_menu'], start_at = 1.60)
            #        self.lasttick = None
            
            if len(self.text_sprite) == 0:
                if self.y_message_ctr < self.y_message_ctr_max:
                    if self.d_messages[self.y_message_ctr][1] != None: self.text_sprite.add(LetterBox_t(self.d_messages[self.y_message_ctr][1],black,dt([49+40,101]), dt([500,39]),width = 1,f_typo = font_typo[13],f_color=font_color[1]))
                    if self.d_messages[self.y_message_ctr][2] != None: self.text_sprite.add(LetterBox_t(self.d_messages[self.y_message_ctr][2],black,dt([49+40,149]), dt([500,39]),width = 1,f_typo = font_typo[13],f_color=font_color[1]))
                    if self.d_messages[self.y_message_ctr][3] != None: self.text_sprite.add(LetterBox_t(self.d_messages[self.y_message_ctr][3],black,dt([49+40,202]), dt([500,39]),width = 1,f_typo = font_typo[13],f_color=font_color[1]))
                    if self.d_messages[self.y_message_ctr][4] != None: self.text_sprite.add(LetterBox_t(self.d_messages[self.y_message_ctr][4],black,dt([49+40,258]), dt([500,39]),width = 1,f_typo = font_typo[13],f_color=font_color[1]))
                    if self.d_messages[self.y_message_ctr][5] != None: self.text_sprite.add(LetterBox_t(self.d_messages[self.y_message_ctr][5],black,dt([49+40,308]), dt([500,39]),width = 1,f_typo = font_typo[13],f_color=font_color[1]))
                
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            for item in self.text_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            
            self.all_sprite.draw(self.gameDisplay)
            self.text_sprite.draw(self.gameDisplay)
                    
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            self.lasttick = pygame.time.get_ticks()

            self.all_sprite = pygame.sprite.Group()
            self.text_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(CharacBox(bg_fade, black, *dt2([0,0],[800,600]), width = 1, static=True))
            
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,25),delay = 700))
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,25,25),delay = 400))
            
            if self.c_still_frame != None:
                
                self.level_1 = CharacBox(self.c_still_frame, black, *dt2((25,25), (750,550)),width = 1)
                self.all_sprite.add(self.level_1)
            
            self.border = BorderBox_t(self.d_frame_color, *dt2([30,89],[640,267]), 3)
            self.border2 = BorderBox(self.d_frame_color, *dt2([30-5,89-5],[640-5,267-5]), 3,6,alpha = 150) 
            
            self.all_sprite.add(CharacBox(dlg, black, *dt2([30,89],[640,267]), width = 1, static=False))
            
            
            #self.all_sprite.add(self.border2)
            #self.all_sprite.add(self.border)
            
            self.all_sprite.add(LetterBox_t(self.d_char_name,black,*dt2([30,522], [283,63]),5,f_typo = font_typo[9]))
        
            self.all_sprite.add(CharacBox(self.d_char_sprite, black, *dt2((450,75), (int(344*1.2),int(450*1.2))),width = 1))
            
            self.all_sprite.add(LetterBox("Press space to continue",black,*dt2([142,436], [281,25]),5,f_typo = font_typo[6],f_color = font_color[1]))
            
        def game_loop():
            
            game_start()
            
            while 'D' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
            del self.y_message_ctr
            del self.y_message_ctr_max
                
        game_loop()
        
    def SceneE(self):
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        if self.classic_score == 0:stopmusic()
                        if self.command=='endless':
                            self.command = ''
                            self.running = 'K'
                        elif self.command=='funny':
                            self.command = ''
                            self.running = 'L'
                        elif self.command=='classic':
                            self.command = ''
                            self.running = 'M'
                        elif self.command=='idle':
                            self.command = ''
                            self.running = 'R'
                        elif self.command=='blackout':
                            self.command = ''
                            self.running = 'S'
                        else:
                            self.running = 'O'

        def game_system(): #try your best to put all the input functions here
            game_control()
            
            #if self.lasttick != None:
            #        if self.settings_dict['music']: playmusic(music_array['main_menu'], start_at = 1.60)
            #        self.lasttick = None
                
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            
            self.all_sprite.draw(self.gameDisplay)
                    
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            if self.classic_score == 0:
                if self.settings_dict['music']: playmusic(music_array['get_ready'], 0)
            
            self.lasttick = pygame.time.get_ticks()

            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(CharacBox(bg_fade, black, *dt2([0,0],[800,600]), width = 1, static=True))
            
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,25),delay = 700))
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,25,25),delay = 400))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([30,522], [43,67]),5,0,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([30+48*1,522], [43,67]),5,0,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([30+48*2,522], [43,67]),5,0,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([30+48*3,522], [43,67]),5,0,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([10+224,522], [43,67]),5,200,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([10+224+48*1,522], [43,67]),5,200,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([10+224+48*2,522], [43,67]),5,200,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([10+224+48*3,522], [43,67]),5,200,f_typo=font_typo[5]))
            
            '''if self.c_still_frame != None:
                self.level_1 = CharacBox(self.c_still_frame, black, *dt2([30-5,30-5], [640+5,480+5]),width = 1)
                self.all_sprite.add(self.level_1)'''
            
            '''if self.command == 'endless':
                self.all_sprite.add(LetterBox('',white,*dt2([30-5,30-5], [640+5,480+5]),5,bg_color=(50,50,50)))
                self.all_sprite.add(LetterBox('',white,*dt2([30-5-5,30-5-5],[650+5,490+5]),5))
            if self.command == 'classic':
                self.all_sprite.add(LetterBox_t('',white,*dt2([30-5,30-5], [640+5,480+5]),5))
                self.all_sprite.add(LetterBox_t('',white,*dt2([30-5-5,30-5-5],[650+5,490+5]),5))
            else:
                self.all_sprite.add(LetterBox('',white,*dt2([30-5,30-5], [640+5,480+5]),5))
                self.all_sprite.add(LetterBox('',white,*dt2([30-5-5,30-5-5],[650+5,490+5]),5))'''
                
            if self.intermission_msg != None:
                self.all_sprite.add(LetterBox(self.intermission_msg[0],black,*dt2([48,163], [608,95]),5,f_typo = font_typo[5]))
                self.all_sprite.add(LetterBox(self.intermission_msg[1],black,*dt2([48,286], [608,39]),5,f_typo = font_typo[10]))
            
            self.all_sprite.add(CharacBox(dlg_bord, black, *dt2([25-10,25-10],[640+25,480+25]), width = 1, static=False))
            
            self.all_sprite.add(LetterBox("Press space to continue",black,*dt2([212,436], [281,25]),5,f_typo = font_typo[6],f_color = font_color[1]))
            
            if self.save_dict['continue'][0] != None:
                
                retset = block_collector(self.save_dict['continue'])
                spriteset = block_preview(retset)
                self.all_sprite.add(LetterBox_t("Blocks: ",black,dt((684,32)), dt((122,30)),width = 1,f_typo = font_typo[10]))
                for sprit in spriteset:self.all_sprite.add(sprit)
                self.all_sprite.add(LetterBox_t("Time: ",black,dt((684,335)), dt((122,30)),width = 1,f_typo = font_typo[10]))
                self.all_sprite.add(LetterBox_t(str(self.game_time_limit),black,*dt2([688,361], [92,74]),5,1000,f_typo=font_typo[14]))
            
            elif self.command == 'classic':
                
                retset = block_collector(self.classic_level, 'classic')
                spriteset = block_preview(retset)

                self.all_sprite.add(LetterBox_t("Blocks: ",black,dt((684,32)), dt((122,30)),width = 1,f_typo = font_typo[10]))
                
                for sprit in spriteset:self.all_sprite.add(sprit)
                
                self.all_sprite.add(LetterBox_t("Time: ",black,dt((684,335)), dt((122,30)),width = 1,f_typo = font_typo[10]))
                
                self.all_sprite.add(LetterBox_t(str(self.game_time_limit),black,*dt2([688,361], [92,74]),5,1000,f_typo=font_typo[14]))
            

            self.all_sprite.add(LetterBox_t(random.choice(loading_cues),black,dt((413, 537)), dt((369,32)),width = 1, delay = 300, f_typo = font_typo[17]))
            
            
        def game_loop():
            
            game_start()
            
            while 'E' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()   

    def SceneF(self):
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        beep_array['beep20'].play() if self.settings_dict['sound'] else None
                        if self.command == 'classic_end':
                            self.save_dict['continue'] = self.endless_save
                            if self.classic_score > self.save_dict['classic']:
                                self.save_dict['classic'] = self.classic_score
                            self.classic_score = 0
                            del self.endless_save
                            json_save(self.save_dict)
                            self.command = ''
                            self.running = 'A'
                        elif self.save_dict['continue'][0] == None:
                            self.save_dict['continue'] = self.endless_save
                            del self.endless_save
                            json_save(self.save_dict)
                            self.running = 'A'
                            
                        
                            
                        else:
                            self.running = '9'
                            self.command = 'next_stage'

        def game_system(): #try your best to put all the input functions here
            game_control()
            
            #if self.lasttick != None:
            #        if self.settings_dict['music']: playmusic(music_array['main_menu'], start_at = 1.60)
            #        self.lasttick = None
                
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            
            self.all_sprite.draw(self.gameDisplay)
                    
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            change_dif("reset")
            
            self.lose = 1
            
            if 'end' in self.command:
                if self.settings_dict['music']: playmusic(music_array['win'], -1)
            
            if 'classic' not in self.command:
                if self.settings_dict['music']: playmusic(music_array['win'], -1)
            
            self.lasttick = pygame.time.get_ticks()

            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(CharacBox(bg_fade, black, *dt2([0,0],[800,600]), width = 1, static=True))
            
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,25),delay = 700))
            self.all_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,25,25),delay = 400))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([30,522], [43,67]),5,0,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox_t('L',black,*dt2([30+48*1,522], [43,67]),5,0,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox_t('O',black,*dt2([30+48*2,522], [43,67]),5,0,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox_t('K',black,*dt2([30+48*3,522], [43,67]),5,0,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([10+224,522], [43,67]),5,200,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox_t('L',black,*dt2([10+224+48*1,522], [43,67]),5,200,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox_t('O',black,*dt2([10+224+48*2,522], [43,67]),5,200,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox_t('K',black,*dt2([10+224+48*3,522], [43,67]),5,200,f_typo=font_typo[5]))
            
            #self.level_1 = CharacBox(self.c_still_frame, black, [30-5,30-5], [640+5,480+5],width = 1)
            
            #self.all_sprite.add(self.level_1)
            
            self.all_sprite.add(LetterBox('',white,*dt2([30-5,30-5], [640+5,480+5]),5))
            self.all_sprite.add(LetterBox('',white,*dt2([30-5-5,30-5-5],[650+5,490+5]),5))
            
            if self.intermission_msg != None:
                self.all_sprite.add(LetterBox_t(self.intermission_msg[0],black,*dt2([49,63], [608,95]),5,f_typo = font_typo[5]))
                self.all_sprite.add(LetterBox_t(self.intermission_msg[1],black,*dt2([49,133], [608,39]),5,f_typo = font_typo[10]))
            
            self.all_sprite.add(LetterBox_t("Time Finished: ",black,*dt2([49,251], [281,31]),5,500,f_typo = font_typo[10]))
            self.all_sprite.add(LetterBox_t("Click Speed: ",black,*dt2([49,306], [281,31]),5,500,f_typo = font_typo[10]))
            
            self.all_sprite.add(LetterBox("{0}:{1}".format(((self.game_timer_end - self.game_timer_start)//1000//60), ((self.game_timer_end - self.game_timer_start)//1000%60)),black,*dt2([376,251], [281,31]),5,1000,f_typo = font_typo[13]))
            self.all_sprite.add(LetterBox("{0}clicks\sec".format(round(self.click_average,3)),black,*dt2([376,306], [281,31]),5,1000,f_typo = font_typo[13]))
            
            if self.command == 'classic' or self.command == 'classic_end':
                self.all_sprite.add(LetterBox_t("Levels Cleared: ",black,*dt2([49,361], [281,31]),5,500,f_typo = font_typo[10]))
                self.all_sprite.add(LetterBox("{0}".format(self.classic_score),black,*dt2([376,361], [281,31]),5,1000,f_typo = font_typo[13]))
            
            elif self.save_dict['continue'][0] == None:
                self.all_sprite.add(LetterBox_t("Levels Cleared: ",black,*dt2([49,361], [281,31]),5,500,f_typo = font_typo[10]))
                self.all_sprite.add(LetterBox("{0}".format(self.lvl-1),black,*dt2([376,361], [281,31]),5,1000,f_typo = font_typo[13]))
            
                
            
            self.all_sprite.add(LetterBox_t("Press space to continue",black,*dt2([213,473], [281,25]),5,f_typo = font_typo[6],f_color = font_color[1]))
            
            
        def game_loop():
            
            game_start()
            
            while 'F' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()   
    
    def SceneG(self):
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        beep_array['beep20'].play() if self.settings_dict['sound'] else None
                        self.save_dict['continue'][2] = 1
                        self.running = '9'
                        self.command = 'play_stage'
                    if event.key == pygame.K_ESCAPE:
                        beep_array['pow02'].play() if self.settings_dict['sound'] else None
                        self.save_dict['continue'][2] = 1
                        if self.save_dict['continue'][0] != None:
                            json_save(self.save_dict)
                        self.running = 'A'

        def game_system(): #try your best to put all the input functions here
            game_control()
            
            #if self.lasttick != None:
            #        if self.settings_dict['music']: playmusic(music_array['main_menu'], start_at = 1.60)
            #        self.lasttick = None
                
            for item in self.go_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.go_sprite.draw(self.gameDisplay)
                    
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            change_dif()
            self.lose *= 1.2
            
            if self.settings_dict['music']: playmusic(music_array['lose'], -1)
            
            self.lasttick = pygame.time.get_ticks()

            self.go_sprite = pygame.sprite.Group()
            #self.level_1 = CharacBox(self.c_still_frame, black, [30-5,30-5], [640+5,480+5],width = 1)
            
            #self.all_sprite.add(self.level_1)
            
            self.all_sprite.add(CharacBox(bg_fade, black, *dt2([0,0],[800,600]), width = 1, static=True))
            
            self.go_sprite.add(LetterBox('',white,*dt2([30-5,30-5], [640+5,480+5]),5,bg_color=(25,0,0)))
            self.go_sprite.add(LetterBox('',white,*dt2([30-5-5,30-5-5],[650+5,490+5]),5))
            
            if self.intermission_msg != None:
                self.go_sprite.add(LetterBox(self.intermission_msg[0],black,*dt2([46,125], [608,95]),5,f_typo = font_typo[5]))
                self.go_sprite.add(LetterBox(self.intermission_msg[1],black,*dt2([49,236], [608,39]),5,f_typo = font_typo[10]))
            
            self.go_sprite.add(LetterBox("TIME OUT",black,*dt2([46,299], [608,39]),5,500,f_color= font_color[4],f_typo = font_typo[13]))
            
            self.go_sprite.add(LetterBox("Press <SPACE> to Retry",black,*dt2([45,413], [271,39]),5,f_typo = font_typo[6],f_color = font_color[1]))
            
            self.go_sprite.add(LetterBox("Press <ESC> to Quit",black,*dt2([383,413], [271,39]),5,f_typo = font_typo[6],f_color = font_color[1]))
            
            
        def game_loop():
            
            game_start()
            
            while 'G' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()   



    def SceneI(self):
        
        self.y_message_ctr = 0
        self.y_message_ctr_max = 5
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        beep_array['beep18'].play() if self.settings_dict['sound'] else None
                        if self.y_message_ctr < self.y_message_ctr_max and (self.y_message_ctr != 1):
                            self.text_sprite.empty()
                            self.y_message_ctr += 1
                            
                        if self.y_message_ctr >= self.y_message_ctr_max:
                            self.save_dict['first'] = False
                            json_save(self.save_dict)
                            self.running = '1'
                    
                    if self.y_message_ctr in (3,4):
                        if event.key in (pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6\
                                     ,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_1,pygame.K_2,pygame.K_3\
                                     ,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9) and self.settings_dict['sound']:
                            beep_array['beep04'].set_volume(0.1)
                            beep_array['beep04'].play() if self.settings_dict['sound'] else None
                            
                        
                        if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if self.influ.rect.colliderect(item.rect):
                                            if hasattr(item, 'updating'):
                                                item.updating = True
                                            item.pending_input = 1
                                        self.rapid = True
                                
                        
                        elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if self.influ.rect.colliderect(item.rect):
                                            if hasattr(item, 'updating'):
                                                item.updating = True
                                            item.pending_input = 2
                                        self.rapid = True
                                    
                                    
                        elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if self.influ.rect.colliderect(item.rect):
                                            if hasattr(item, 'updating'):
                                                item.updating = True
                                            item.pending_input = 3
                                        self.rapid = True
                                    
                        elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if self.influ.rect.colliderect(item.rect):
                                            if hasattr(item, 'updating'):
                                                item.updating = True
                                            item.pending_input = 4
                                        self.rapid = True
                                    
                        elif event.key == pygame.K_KP5 or event.key == pygame.K_5:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if self.influ.rect.colliderect(item.rect):
                                            if hasattr(item, 'updating'):
                                                item.updating = True
                                            item.pending_input = 5
                                        self.rapid = True
                                    
                        elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if self.influ.rect.colliderect(item.rect):
                                            if hasattr(item, 'updating'):
                                                item.updating = True
                                            item.pending_input = 6
                                        self.rapid = True
                                    
                        elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if self.influ.rect.colliderect(item.rect):
                                            if hasattr(item, 'updating'):
                                                item.updating = True
                                            item.pending_input = 7
                                        self.rapid = True
                                    
                        elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if self.influ.rect.colliderect(item.rect):
                                            if hasattr(item, 'updating'):
                                                item.updating = True
                                            item.pending_input = 8
                                        self.rapid = True
                                    
                        elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if self.influ.rect.colliderect(item.rect):
                                            if hasattr(item, 'updating'):
                                                item.updating = True
                                            item.pending_input = 9
                                        self.rapid = True
                            
                        if event.type == pygame.KEYUP:
                            self.rapid = False
                    
                    if self.y_message_ctr in (1,2):
                        if event.key in (pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6\
                                         ,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_1,pygame.K_2,pygame.K_3\
                                         ,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9) and self.settings_dict['sound']:
                            beep_array['beep04'].set_volume(0.1)
                            beep_array['beep04'].play() if self.settings_dict['sound'] else None
                            
                        
                        if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 1
                                    self.rapid = True
                                
                        
                        elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 2
                                    self.rapid = True
                                    
                                    
                        elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 3
                                    self.rapid = True
                                    
                        elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 4
                                    self.rapid = True
                                    
                        elif event.key == pygame.K_KP5 or event.key == pygame.K_5:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 5
                                    self.rapid = True
                                    
                        elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 6
                                    self.rapid = True
                                    
                        elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 7
                                    self.rapid = True
                                    
                        elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 8
                                    self.rapid = True
                                    
                        elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                            if self.rapid == False:
                                for item in self.text_sprite:
                                    if hasattr(item, 'pending_input'):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 9
                                    self.rapid = True
                        
                if event.type == pygame.KEYUP:
                    self.rapid = False
                                        
        def game_system(): #try your best to put all the input functions here
            game_control()
            
            '''if not self.box.rect.collidepoint(pygame.mouse.get_pos()):
                if (pygame.mouse.get_pos()[0]) > self.box.rect.right:
                    self.box.rect.right = pygame.mouse.get_pos()[0]
                elif (pygame.mouse.get_pos()[0]) < self.box.rect.left:
                    self.box.rect.left = pygame.mouse.get_pos()[0]'''
            
            if self.lasttick + 1000 < pygame.time.get_ticks():
                if (len(self.text_sprite) == 0):
                    if self.y_message_ctr == 0:
                        self.text_sprite.add(CharacBox(tutorial_frames[0],white,dt((0,0)),dt((800,600))))
                    if self.y_message_ctr == 1:
                        self.text_sprite.add(CharacBox(tutorial_frames[1],white,dt((0,0)),dt((800,600))))
                        self.text_sprite.add(BlockBox((368,235),(75,75),5,visible=True))   
                    if self.y_message_ctr == 2:
                        self.text_sprite.add(CharacBox(tutorial_frames[1],white,dt((0,0)),dt((800,600))))
                        self.text_sprite.add(BlockBox((368,235),(75,75),5,visible=True))  
                        self.text_sprite.add(BlockBox((288,235),(75,75),5,visible=True))  
                        self.text_sprite.add(BlockBox((448,235),(75,75),5,visible=True))  
                    if self.y_message_ctr == 3:
                        self.text_sprite.add(CharacBox(tutorial_frames[2],white,dt((0,0)),dt((800,600))))
                        self.text_sprite.add(BlockBox((288,235),(75,75),5,visible=True))  
                        self.text_sprite.add(BlockBox((448,235),(75,75),5,visible=True))  
                        self.influ = (InfluBox((101,233,233,135),(73,199,656,216)))
                        self.influ.ym = 0
                        self.influ.image.set_alpha(150)
                        self.text_sprite.add(self.influ)
                    if self.y_message_ctr == 4:
                        self.text_sprite.add(CharacBox(tutorial_frames[3],white,dt((0,0)),dt((800,600))))
                        self.text_sprite.add(BlockBox((268,235),(75,75),5,visible=True))  
                        self.text_sprite.add(SubtracBox((468,235),(75,75),5,visible=True))
                        self.text_sprite.add(MythicBox((368,235),(75,75),5,visible=True))
                        self.influ = (InfluBox((101,233,233,135),(73,199,656,216)))
                        self.influ.ym = 0
                        self.influ.image.set_alpha(150)
                        self.text_sprite.add(self.influ)
                        
            
            if ((len(self.text_sprite) == 1 and self.y_message_ctr in (1,2))) or ((len(self.text_sprite) == 2 and self.y_message_ctr in (3,4))):
                self.text_sprite.empty()
                self.y_message_ctr += 1
                
            if self.y_message_ctr in (3,4):
                for item in self.text_sprite:
                    if hasattr(item, 'pending_input'):
                        if self.influ.rect.colliderect(item.rect):
                            item.image.set_alpha(255)
                            if isinstance(item, (JacBox)):
                                if not item.visc:
                                    item.image.set_colorkey((1,1,1))
                                    item.image.set_alpha(40)
                            item.updating = True
                        elif item.image.get_alpha() == 255 or item.image.get_alpha() == 25:
                            if isinstance(item, (JacBox)):
                                item.image.set_colorkey(black)
                            item.image.set_alpha(alpha_game_block)
                            item.updating = True
            
            if self.proctick + 5000 < pygame.time.get_ticks():
                if self.y_message_ctr < self.y_message_ctr_max and (self.y_message_ctr in (0,0)):
                    self.text_sprite.empty()
                    self.y_message_ctr += 1
                    self.proctick = pygame.time.get_ticks()
                
                if self.y_message_ctr >= self.y_message_ctr_max:
                    self.save_dict['first'] = False
                    json_save(self.save_dict)
                    self.running = '1'
                
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            for item in self.text_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
        def game_display_text():
            text, textRect = textdisplay('Hello', font_color[0], font_typo[1])
            textRect.topleft = (50,0)
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(black)
            
            self.all_sprite.draw(self.gameDisplay)
            
            self.text_sprite.draw(self.gameDisplay)
            
            #game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            self.rapid = True
            self.lasttick = pygame.time.get_ticks()
            
            self.proctick = pygame.time.get_ticks()

            self.text_sprite = pygame.sprite.Group()
            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(LetterBox_t('', white, *dt2([0,0],[800,600]), width = 1, bg_color = white))
            
            if self.settings_dict['music']: playmusic(music_array["tutorial"], repeat = -1)
            
        def game_loop():
            
            game_start()
            
            while 'I' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()



    def SceneO(self): 
        
        def game_control(): #put all the game logic here
            
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass #print (pygame.mouse.get_pos())

                if event.type == pygame.QUIT:
                    self.running = ''
                    
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_F1:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.autoplay ^= True
                        
                    
                    if event.key == pygame.K_SPACE:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.running += 'Q'
                        
                    elif event.key == pygame.K_ESCAPE:
                        beep_array['pow02'].play() if self.settings_dict['sound'] else None
                        self.running += 'P'
                    
                    if event.key in (pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6\
                                     ,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_1,pygame.K_2,pygame.K_3\
                                     ,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9) and self.settings_dict['sound']:
                        beep_array['beep04'].set_volume(0.1)
                        beep_array['beep04'].play() if self.settings_dict['sound'] else None
                        
                    self.click_frequency += 1
                    
                    if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 1
                                    self.rapid = True
                            
                    
                    elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 2
                                    self.rapid = True
                                
                                
                    elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 3
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 4
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP5 or event.key == pygame.K_5:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 5
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 6
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 7
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 8
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 9
                                    self.rapid = True
                        
                if event.type == pygame.KEYUP:
                    self.rapid = False

        def game_system(): #try your best to put all the input functions here
            game_control()

            if "Q" in self.running:
                self.SceneQ()
            elif "P" in self.running:
                self.SceneP()
                
            '''self.border.size = (self.border.size[0],self.border.size[1]-1)
            self.border.updating = True'''
            
            for item in self.all_sprite:
                
                if hasattr(item, 'pending_input'):
                    
                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                        
                        item.image.set_alpha(255)
                        
                        if isinstance(item, (JacBox)):
                            if not item.visc:
                                item.image.set_colorkey((1,1,1))
                                item.image.set_alpha(40)
                            
                        item.updating = True
                        
                    elif item.image.get_alpha() == 255 or item.image.get_alpha() == 25:
                        
                        if isinstance(item, (JacBox)):
                            item.image.set_colorkey(black)
                            
                        item.image.set_alpha(alpha_game_block)
                        item.updating = True
            
            if self.influ.beep == 1:
                beep_array['blip06'].set_volume(0.1)
                beep_array['blip06'].play() if self.settings_dict['sound'] else None
                self.influ.beep = 0
            elif self.influ.beep == 2:
                beep_array['blip02'].set_volume(0.1)
                beep_array['blip02'].play() if self.settings_dict['sound'] else None
                self.influ.beep = 0
            
            if self.autoplay:
                if self.auto_timer_start + autoplay_delay < pygame.time.get_ticks():
                    beep_array['beep04'].set_volume(0.1)
                    beep_array['beep04'].play() if self.settings_dict['sound'] else None
                    inp = random.randint(1,9)
                    for item in self.all_sprite:
                        if hasattr(item, 'pending_input'):
                            if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                if hasattr(item, 'updating'):
                                    item.updating = True
                                item.pending_input = inp
                        self.auto_timer_start = pygame.time.get_ticks()    
                
            if self.lasttick + 1000 < pygame.time.get_ticks():
                if self.timer <= 10:
                    beep_array['blip19'].set_volume(0.3)
                    beep_array['blip19'].play() if self.settings_dict['sound'] else None
                    self.j_time_warning = True
                self.timer -= 1
    
                self.lasttick = pygame.time.get_ticks()
            
            if self.click_timer_start + 1000 < pygame.time.get_ticks():
                self.click_average = (self.click_average + self.click_frequency)/2
                self.click_frequency = 0
                self.click_timer_start = pygame.time.get_ticks()
            
            if self.timer <= 5:
                if len(self.block_sprite) <= 3:
                    for i in self.block_sprite:
                        if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                            if hasattr(item, 'updating'):
                                item.updating = True
                            if isinstance(item,(MythicBox)):
                                item.sync_switch = True
                            if isinstance(item,(CracBox)):
                                item.sync_switch = False
                            if isinstance(item,(MockBox)):
                                item.sync_switch = 4
                            item.pending_input = item.num
            
            if self.timer < 1:
                beep_array['pow02'].play() if self.settings_dict['sound'] else None
                self.running = 'G'
            
            for item in self.bg_sprite:
                if callable(getattr(item, 'update', None)):
                    item.update()

            count = 0
            for item in self.all_sprite:
                if hasattr(item, 'visible'):
                    if item.visible == False:
                        item.visible = True
                        count += 1
                        if count > trans_speed:
                            count = 0
                            break
                
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            if len(self.block_sprite) != self.counter:
                
                #print(self.counter, len(self.all_sprite))
                self.score += self.counter - len(self.block_sprite)
                self.scorebox.score = self.score
                
                self.border.anim_frame = 6
                self.border.updating = True
                
                #self.border2.anim_frame = 6
                #self.border2.updating = True
                
                
                '''if self.bg_gamefield != None:
                    self.bg_gamefield[1] += 1
                    self.bg_gamefield[1] %= len(bg_neon[self.bg_gamefield[0]])
                    self.j_bg.char = bg_neon[self.bg_gamefield[0]][self.bg_gamefield[1]]
                    self.j_bg.updating = True'''
                    
                self.counter = len(self.block_sprite)
                beep_array['pow05'].set_volume(0.3)
                beep_array['pow05'].play() if self.settings_dict['sound'] else None
                #print (self.score % (self.box_size[0]*self.box_size[1]), self.score, (self.box_size[0]*self.box_size[1]))
                #print(self.score, self.current_block)
                    
            if self.score != 0 and self.score % self.current_block == 0:
                
                #PUT THE CODE HERE WHEN YOU FINISHED A GAME
                game_next_level()
                        
        def game_display_text():
            text, textRect = textdisplay(self.game_levelname.format(self.lvl, len(stage_layouts[self.save_dict['continue'][0]][self.save_dict['continue'][1]])), font_color[1], font_typo[6])
            textRect.topleft = dt((705,60))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(self.game_leveltag, font_color[1], font_typo[0])
            textRect.topleft = dt((730,25))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(':{0}'.format(self.timer), font_color[4] if self.j_time_warning else font_color[1], font_typo[7])
            textRect.topleft = dt((688,361))
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(self.game_background)
            
            #pygame.draw.rect(self.gameDisplay, white, [30-5,30-5,640+5,480+5], 3)
            
            self.bg_sprite.draw(self.gameDisplay)
            self.all_sprite.draw(self.gameDisplay)
            
            game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            ### Setting Up the Game
            
            self.j_time_warning = False
            
            self.auto_timer_start = pygame.time.get_ticks()
            self.autoplay = False
            
            self.game_timer_start = pygame.time.get_ticks()
            self.click_timer_start = pygame.time.get_ticks()
            self.click_frequency = 0
            
            self.lvl = 1
            self.score = 0
            self.game_pos = game_pos
            self.rapid = False
            self.block_sprite = pygame.sprite.Group()
            self.all_sprite = pygame.sprite.Group()
            self.bg_sprite = pygame.sprite.Group()
            
            self.border = BorderBox_t(self.c_frame_color, *dt2([0,0],[800,600]), 3)
            #self.border2 = BorderBox(self.c_frame_color, *dt2([self.game_pos-5-5,self.game_pos-5-5],[650+5,490+5]), 3,6) 
            #self.all_sprite.add(self.border2)
            self.all_sprite.add(self.border)
            
            '''
            if self.c_still_frame != None:
                self.level_1 = CharacBox(self.c_still_frame, black, (25,25), (750,550),width = 1)
                self.all_sprite.add(self.level_1)
            '''
            
            if self.bg_gamefield != None:
                self.j_bg = CharacBox(bg_neon[self.bg_gamefield], black, *dt2([0,0],[800,600]), width = 1,static=True)
                self.all_sprite.add(self.j_bg)
            
            
            self.all_sprite.add(CharacBox(bloom, black, *dt2([0,0],[800,600]), width = 1,static = True))
                
            
            #self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,50),2000))
            #self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(10,10,0)))

            self.all_sprite.add(LetterBox('B',black,*dt2([30,522], [43,67]),5,300,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([30+48*1,522], [43,67]),5,400,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([30+48*2,522], [43,67]),5,500,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([30+48*3,522], [43,67]),5,600,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([10+224,522], [43,67]),5,700,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([10+224+48*1,522], [43,67]),5,800,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([10+224+48*2,522], [43,67]),5,900,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([10+224+48*3,522], [43,67]),5,1000,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox_t('Space',red,*dt2([693,480], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Pause Game',black,*dt2([705,503], [90,24]),5,1500,f_typo=font_typo[8]))
            
            self.all_sprite.add(LetterBox_t('Esc',blue,*dt2([693,530], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Quit',black,*dt2([715,553], [46,24]),5,1500,f_typo=font_typo[8]))
            
            self.box_size = (8,6)
            self.max = self.box_size[0] * self.box_size[1]
            self.scorebox = (ScoreBox(yellow, *dt2((445,547),(220,17)),0,self.max,1500))
            
            
            if self.settings_dict['music']: playmusic(self.game_music, repeat = -1)
            
            ### End of SET UP
            
            game_new_level()
            
        
        def game_new_level():
            
            self.influ = (InfluBox(((80*self.box_size[0]//2.5),(80*self.box_size[1]//2.5)),(game_pos,game_pos,80*self.box_size[0],80*self.box_size[1])))
            self.all_sprite.add(self.influ)
            
            self.influ2 = (InfluBox(((80*self.box_size[0]//2.5),(80*self.box_size[1]//2.5)),(game_pos,game_pos,80*self.box_size[0],80*self.box_size[1])))
            self.influ2.xm = self.influ2.ym = -1
            self.all_sprite.add(self.influ2)
            
            self.timer = int(self.game_time_limit * 2 * self.lose)
            
            self.lasttick = pygame.time.get_ticks()
            
            self.all_sprite.add(self.scorebox)
            
            
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    #r = random.randrange(1,7+1)
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.save_dict['continue'][1], phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    '''
                    if r == 1: x = (BlockBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 2: x = (SyncBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 3: x = (SubtracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 4: x = (MythicBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 5: x = (CracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 6: x = (JacBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 7: x = (DrawBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    '''
                    
                    
                    
                    
                    if blok == None:
                        continue
                    
                         
                    blok.image.set_alpha(alpha_game_block)
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
                    
            
            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        def game_next_level():
            
            self.timer = int(self.game_time_limit * 2 * self.lose)
            self.j_time_warning = False
            self.score = 0
            self.lasttick = pygame.time.get_ticks()
            self.scorebox.score = 0
            
            self.save_dict['continue'][2] += 1
            if self.save_dict['continue'][2] > len(stage_layouts[self.save_dict['continue'][0]][self.save_dict['continue'][1]]):
                self.game_timer_end = pygame.time.get_ticks()
                self.running = 'F'
                beep_array['pow18'].play() if self.settings_dict['sound'] else None
                return None
            
            self.lvl += 1
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.save_dict['continue'][1], phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    
                    
                    if blok == None:
                        continue
                    
                    blok.image.set_alpha(alpha_game_block)
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        
        
        def game_loop():
            
            game_start()
                
            while 'O' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()
    
    def SceneJ(self): 
        
        def game_control(): #put all the game logic here
            
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass #print (pygame.mouse.get_pos())

                if event.type == pygame.QUIT:
                    self.running = ''
                    
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_F1:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.autoplay ^= True
                        
                    
                    if event.key == pygame.K_SPACE:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.running += 'Q'
                        
                    elif event.key == pygame.K_ESCAPE:
                        beep_array['pow02'].play() if self.settings_dict['sound'] else None
                        self.running += 'P'
                    
                    if event.key in (pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6\
                                     ,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_1,pygame.K_2,pygame.K_3\
                                     ,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9) and self.settings_dict['sound']:
                        beep_array['beep04'].set_volume(0.1)
                        beep_array['beep04'].play() if self.settings_dict['sound'] else None
                        
                    self.click_frequency += 1
                    
                    if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 1
                                self.rapid = True
                            
                    
                    elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 2
                                self.rapid = True
                                
                                
                    elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 3
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 4
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP5 or event.key == pygame.K_5:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 5
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 6
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 7
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 8
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 9
                                self.rapid = True
                        
                if event.type == pygame.KEYUP:
                    self.rapid = False

        def game_system(): #try your best to put all the input functions here
            game_control()

            if "Q" in self.running:
                self.SceneQ()
            elif "P" in self.running:
                self.SceneP()
                
            '''self.border.size = (self.border.size[0],self.border.size[1]-1)
            self.border.updating = True'''
                
            if self.autoplay:
                if self.auto_timer_start + autoplay_delay < pygame.time.get_ticks():
                    beep_array['beep04'].set_volume(0.1)
                    beep_array['beep04'].play() if self.settings_dict['sound'] else None
                    inp = random.randint(1,9)
                    for item in self.all_sprite:
                        if hasattr(item, 'pending_input'):
                            if hasattr(item, 'updating'):
                                item.updating = True
                            item.pending_input = inp
                        self.auto_timer_start = pygame.time.get_ticks()    
                
            if self.lasttick + 1000 < pygame.time.get_ticks():
                if self.timer <= 10:
                    beep_array['blip19'].set_volume(0.3)
                    beep_array['blip19'].play() if self.settings_dict['sound'] else None
                    self.j_time_warning = True
                self.timer -= 1
    
                self.lasttick = pygame.time.get_ticks()
            
            if self.click_timer_start + 1000 < pygame.time.get_ticks():
                self.click_average = (self.click_average + self.click_frequency)/2
                self.click_frequency = 0
                self.click_timer_start = pygame.time.get_ticks()
            
            if self.timer < 1:
                beep_array['pow02'].play() if self.settings_dict['sound'] else None
                self.running = 'G'
            
            for item in self.bg_sprite:
                if callable(getattr(item, 'update', None)):
                    item.update()

            count = 0
            for item in self.all_sprite:
                if hasattr(item, 'visible'):
                    if item.visible == False:
                        item.visible = True
                        count += 1
                        if count > trans_speed:
                            count = 0
                            break
                
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            if len(self.block_sprite) != self.counter:
                
                #print(self.counter, len(self.all_sprite))
                self.score += self.counter - len(self.block_sprite)
                self.scorebox.score = self.score
                
                self.border.anim_frame = 6
                self.border.updating = True
                
                #self.border2.anim_frame = 6
                #self.border2.updating = True
                
                
                '''if self.bg_gamefield != None:
                    self.bg_gamefield[1] += 1
                    self.bg_gamefield[1] %= len(bg_neon[self.bg_gamefield[0]])
                    self.j_bg.char = bg_neon[self.bg_gamefield[0]][self.bg_gamefield[1]]
                    self.j_bg.updating = True'''
                    
                self.counter = len(self.block_sprite)
                beep_array['pow05'].set_volume(0.3)
                beep_array['pow05'].play() if self.settings_dict['sound'] else None
                #print (self.score % (self.box_size[0]*self.box_size[1]), self.score, (self.box_size[0]*self.box_size[1]))
                #print(self.score, self.current_block)
                    
            if self.score != 0 and self.score % self.current_block == 0:
                
                #PUT THE CODE HERE WHEN YOU FINISHED A GAME
                game_next_level()
                        
        def game_display_text():
            text, textRect = textdisplay(self.game_levelname.format(self.lvl, len(stage_layouts[self.save_dict['continue'][0]][self.save_dict['continue'][1]])), font_color[1], font_typo[6])
            textRect.topleft = dt((705,60))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(self.game_leveltag, font_color[1], font_typo[0])
            textRect.topleft = dt((730,25))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(':{0}'.format(self.timer), font_color[4] if self.j_time_warning else font_color[1], font_typo[7])
            textRect.topleft = dt((688,361))
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(self.game_background)
            
            #pygame.draw.rect(self.gameDisplay, white, [30-5,30-5,640+5,480+5], 3)
            
            self.bg_sprite.draw(self.gameDisplay)
            self.all_sprite.draw(self.gameDisplay)
            
            game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            ### Setting Up the Game
            
            self.j_time_warning = False
            
            self.auto_timer_start = pygame.time.get_ticks()
            self.autoplay = False
            
            self.game_timer_start = pygame.time.get_ticks()
            self.click_timer_start = pygame.time.get_ticks()
            self.click_frequency = 0
            
            self.lvl = 1
            self.score = 0
            self.game_pos = 30
            self.rapid = False
            self.block_sprite = pygame.sprite.Group()
            self.all_sprite = pygame.sprite.Group()
            self.bg_sprite = pygame.sprite.Group()
            
            self.border = BorderBox_t(self.c_frame_color, *dt2([0,0],[800,600]), 3)
            #self.border2 = BorderBox(self.c_frame_color, *dt2([self.game_pos-5-5,self.game_pos-5-5],[650+5,490+5]), 3,6) 
            #self.all_sprite.add(self.border2)
            self.all_sprite.add(self.border)
            
            '''
            if self.c_still_frame != None:
                self.level_1 = CharacBox(self.c_still_frame, black, (25,25), (750,550),width = 1)
                self.all_sprite.add(self.level_1)
            '''
            
            if self.bg_gamefield != None:
                self.j_bg = CharacBox(bg_neon[self.bg_gamefield], black, *dt2([0,0],[800,600]), width = 1,static=True)
                self.all_sprite.add(self.j_bg)
            
            
            self.all_sprite.add(CharacBox(bloom, black, *dt2([0,0],[800,600]), width = 1,static = True))
                
            
            #self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,50),2000))
            self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(10,10,0)))

            self.all_sprite.add(LetterBox('B',black,*dt2([30,522], [43,67]),5,300,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([30+48*1,522], [43,67]),5,400,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([30+48*2,522], [43,67]),5,500,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([30+48*3,522], [43,67]),5,600,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([10+224,522], [43,67]),5,700,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([10+224+48*1,522], [43,67]),5,800,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([10+224+48*2,522], [43,67]),5,900,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([10+224+48*3,522], [43,67]),5,1000,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox_t('Space',red,*dt2([693,480], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Pause Game',black,*dt2([705,503], [90,24]),5,1500,f_typo=font_typo[8]))
            
            self.all_sprite.add(LetterBox_t('Esc',blue,*dt2([693,530], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Quit',black,*dt2([715,553], [46,24]),5,1500,f_typo=font_typo[8]))
            
            self.box_size = (8,6)
            self.max = self.box_size[0] * self.box_size[1]
            self.scorebox = (ScoreBox(yellow, *dt2((445,547),(220,17)),0,self.max,1500))
            
            
            if self.settings_dict['music']: playmusic(self.game_music)
            
            ### End of SET UP
            
            game_new_level()
            
        
        def game_new_level():
            
            self.timer = self.game_time_limit
            
            self.lasttick = pygame.time.get_ticks()
            
            self.all_sprite.add(self.scorebox)
            
            
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    #r = random.randrange(1,7+1)
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.save_dict['continue'][1], phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    '''
                    if r == 1: x = (BlockBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 2: x = (SyncBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 3: x = (SubtracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 4: x = (MythicBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 5: x = (CracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 6: x = (JacBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 7: x = (DrawBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    '''
                    
                    if blok == None:
                        continue
                         
                    
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
                    
                    
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        def game_next_level():
            
            self.timer = self.game_time_limit
            self.j_time_warning = False
            self.score = 0
            self.lasttick = pygame.time.get_ticks()
            self.scorebox.score = 0
            
            self.save_dict['continue'][2] += 1
            if self.save_dict['continue'][2] > len(stage_layouts[self.save_dict['continue'][0]][self.save_dict['continue'][1]]):
                self.game_timer_end = pygame.time.get_ticks()
                self.running = 'F'
                beep_array['pow18'].play() if self.settings_dict['sound'] else None
                return None
            
            self.lvl += 1
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.save_dict['continue'][1], phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    
                    if blok == None:
                        continue
                    
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        
        
        def game_loop():
            
            game_start()
                
            while 'J' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()


    def SceneK(self):
        
        def game_control(): #put all the game logic here
            
            for event in pygame.event.get():
                
                if event.type == MUSIC_ENDED:
                    self.game_music = random.choice(lounge_array)
                    if self.settings_dict['music']: playmusic(self.game_music)

                if event.type == pygame.QUIT:
                    self.running = ''
                    
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_F1:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.autoplay ^= True
                    
                    if event.key == pygame.K_SPACE:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.running += 'Q'
                        
                    elif event.key == pygame.K_ESCAPE:
                        beep_array['pow02'].play() if self.settings_dict['sound'] else None
                        self.running += 'P'
                    
                    if event.key in (pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6\
                                     ,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_1,pygame.K_2,pygame.K_3\
                                     ,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9) and self.settings_dict['sound']:
                        beep_array['beep04'].set_volume(0.1)
                        beep_array['beep04'].play() if self.settings_dict['sound'] else None
                        
                    self.click_frequency += 1
                    
                    if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 1
                                self.rapid = True
                            
                    
                    elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 2
                                self.rapid = True
                                
                                
                    elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 3
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 4
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP5 or event.key == pygame.K_5:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 5
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 6
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 7
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 8
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 9
                                self.rapid = True
                        
                if event.type == pygame.KEYUP:
                    self.rapid = False

        def game_system(): #try your best to put all the input functions here
            game_control()

            if "Q" in self.running:
                self.SceneQ()
            elif "P" in self.running:
                self.SceneP()
            
            if self.autoplay:
                if self.auto_timer_start + autoplay_delay < pygame.time.get_ticks():
                    beep_array['beep04'].set_volume(0.1)
                    beep_array['beep04'].play() if self.settings_dict['sound'] else None
                    inp = random.randint(1,9)
                    for item in self.all_sprite:
                        if hasattr(item, 'pending_input'):
                            if hasattr(item, 'updating'):
                                item.updating = True
                            item.pending_input = inp
                        self.auto_timer_start = pygame.time.get_ticks()
                
            if self.lasttick + 1000 < pygame.time.get_ticks():
                if self.timer <= 10:
                    self.k_time_warning = True
                    beep_array['blip19'].set_volume(0.3)
                    beep_array['blip19'].play() if self.settings_dict['sound'] else None
                self.timer -= 1
                self.lasttick = pygame.time.get_ticks()
            
            if self.click_timer_start + 1000 < pygame.time.get_ticks():
                self.click_average = (self.click_average + self.click_frequency)/2
                self.click_frequency = 0
                self.click_timer_start = pygame.time.get_ticks()
            
            if self.timer < 1:
                beep_array['pow02'].play() if self.settings_dict['sound'] else None
                if (self.lvl - 1) > self.save_dict['endless']:
                    self.save_dict['endless'] = self.lvl - 1
                self.game_timer_end = pygame.time.get_ticks()
                self.running = 'F'
            
            for item in self.bg_sprite:
                if callable(getattr(item, 'update', None)):
                    item.update()
            
            count = 0
            for item in self.all_sprite:
                if hasattr(item, 'visible'):
                    if item.visible == False:
                        item.visible = True
                        count += 1
                        if count > trans_speed:
                            count = 0
                            break
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            if len(self.block_sprite) != self.counter:
                #print(self.counter, len(self.all_sprite))
                self.score += self.counter - len(self.block_sprite)
                self.scorebox.score = self.score
                self.border.anim_frame = 6
                self.border.updating = True
                self.border2.anim_frame = 6
                self.border.updating = True
                self.counter = len(self.block_sprite)
                beep_array['pow05'].set_volume(0.3)
                beep_array['pow05'].play() if self.settings_dict['sound'] else None
                #print (self.score % (self.box_size[0]*self.box_size[1]), self.score, (self.box_size[0]*self.box_size[1]))
                #print(self.score, self.current_block)
                    
            if self.score != 0 and self.score % self.current_block == 0:
                
                #PUT THE CODE HERE WHEN YOU FINISHED A GAME
                game_next_level()
                        
        def game_display_text():
            text, textRect = textdisplay(self.game_levelname.format(self.lvl), font_color[1], font_typo[6])
            textRect.topleft = dt((705,60))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(self.game_leveltag, font_color[1], font_typo[0])
            textRect.topleft = dt((730,25))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(':{0}'.format(self.timer), font_color[4] if self.k_time_warning else font_color[1], font_typo[7])
            textRect.topleft = dt((688,361))
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(self.game_background)
            
            #pygame.draw.rect(self.gameDisplay, white, [30-5,30-5,640+5,480+5], 3)
            
            self.bg_sprite.draw(self.gameDisplay)
            self.all_sprite.draw(self.gameDisplay)
            
            game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            ### Setting Up the Game
            
            self.k_time_warning = False
            
            self.auto_timer_start = pygame.time.get_ticks()
            self.autoplay = False
            
            self.game_timer_start = pygame.time.get_ticks()
            self.click_timer_start = pygame.time.get_ticks()
            self.click_frequency = 0
            
            self.lvl = 1
            self.score = 0
            self.game_pos = 30
            self.rapid = False
            self.block_sprite = pygame.sprite.Group()
            self.all_sprite = pygame.sprite.Group()
            self.bg_sprite = pygame.sprite.Group()
            
            self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,50),2000))
            self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(50,50,0)))
            
            
            '''
            if self.c_still_frame != None:
                self.level_1 = CharacBox(self.c_still_frame, black, (25,25), (750,550),width = 1)
                self.all_sprite.add(self.level_1)
            '''
            
            self.border = BorderBox(self.c_frame_color, *dt2([self.game_pos-5,self.game_pos-5],[640+5,480+5]), 3)
            self.border2 = BorderBox(self.c_frame_color, *dt2([self.game_pos-5-5,self.game_pos-5-5],[650+5,490+5]), 3,6) 
            
            self.all_sprite.add(self.border2)
            self.all_sprite.add(self.border)
            
            self.all_sprite.add(LetterBox('B',black,*dt2([30,522], [43,67]),5,300,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([30+48*1,522], [43,67]),5,400,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([30+48*2,522], [43,67]),5,500,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([30+48*3,522], [43,67]),5,600,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([10+224,522], [43,67]),5,700,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([10+224+48*1,522], [43,67]),5,800,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([10+224+48*2,522], [43,67]),5,900,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([10+224+48*3,522], [43,67]),5,1000,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox_t('Space',red,*dt2([693,480], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Pause Game',black,*dt2([705,503], [90,24]),5,1500,f_typo=font_typo[8]))
            
            self.all_sprite.add(LetterBox_t('Esc',blue,*dt2([693,530], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Quit',black,*dt2([715,553], [46,24]),5,1500,f_typo=font_typo[8]))
            
            self.box_size = (8,6)
            self.max = self.box_size[0] * self.box_size[1]
            self.scorebox = (ScoreBox(yellow, *dt2((445,547),(220,17)),0,self.max,1500))
            
            
            if self.settings_dict['music']: playmusic(self.game_music)
            
            ### End of SET UP
            
            game_new_level()
            
        
        def game_new_level():
            
            self.timer = self.game_time_limit
            
            self.lasttick = pygame.time.get_ticks()
            
            self.all_sprite.add(self.scorebox)
            
            
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    #r = random.randrange(1,7+1)
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.lvl, phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    '''
                    if r == 1: x = (BlockBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 2: x = (SyncBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 3: x = (SubtracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 4: x = (MythicBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 5: x = (CracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 6: x = (JacBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 7: x = (DrawBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    '''
                    
                    if blok == None:
                        continue
                    
                    
                    
                    
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
                    
            
            
            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        def game_next_level():
            
            self.timer = self.game_time_limit
            self.k_time_warning = False
            self.score = 0
            self.lasttick = pygame.time.get_ticks()
            self.scorebox.score = 0
            

            self.lvl += 1
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.lvl, phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    
                    if blok == None:
                        continue
                    
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        
        
        def game_loop():
            
            game_start()
                
            while 'K' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()

    def SceneL(self): 

        
        def game_control(): #put all the game logic here
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = ''
                    
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_F1:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.autoplay ^= True
                    
                    if event.key == pygame.K_SPACE:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.running += 'Q'
                        
                    elif event.key == pygame.K_ESCAPE:
                        beep_array['pow02'].play() if self.settings_dict['sound'] else None
                        self.running += 'P'
                    
                    if event.key in (pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6\
                                     ,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_1,pygame.K_2,pygame.K_3\
                                     ,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9) and self.settings_dict['sound']:
                        beep_array['pew'].set_volume(50)
                        beep_array['pew'].play() if self.settings_dict['sound'] else None
                        
                    self.click_frequency += 1
                    
                    if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 1
                                self.rapid = True
                            
                    
                    elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 2
                                self.rapid = True
                                
                                
                    elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 3
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 4
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP5 or event.key == pygame.K_5:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 5
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 6
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 7
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 8
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 9
                                self.rapid = True
                        
                if event.type == pygame.KEYUP:
                    self.rapid = False

        def game_system(): #try your best to put all the input functions here
            game_control()

            if "Q" in self.running:
                self.SceneQ()
            elif "P" in self.running:
                self.SceneP()
                
            if self.lasttick + 1000 < pygame.time.get_ticks():
                if self.timer <= 10:
                    self.k_time_warning = True
                    beep_array['blip19'].set_volume(0.3)
                    beep_array['blip19'].play() if self.settings_dict['sound'] else None
                self.timer -= 1
                self.lasttick = pygame.time.get_ticks()
            
            if self.autoplay:
                if self.auto_timer_start + autoplay_delay < pygame.time.get_ticks():
                    beep_array['beep04'].set_volume(0.1)
                    beep_array['beep04'].play() if self.settings_dict['sound'] else None
                    inp = random.randint(1,9)
                    for item in self.all_sprite:
                        if hasattr(item, 'pending_input'):
                            if hasattr(item, 'updating'):
                                item.updating = True
                            item.pending_input = inp
                        self.auto_timer_start = pygame.time.get_ticks()
            
            if self.click_timer_start + 1000 < pygame.time.get_ticks():
                self.click_average = (self.click_average + self.click_frequency)/2
                self.click_frequency = 0
                self.click_timer_start = pygame.time.get_ticks()
            
            if self.timer < 1:
                beep_array['pow02'].play() if self.settings_dict['sound'] else None
                self.game_timer_end = pygame.time.get_ticks()
                self.running = 'F'
            
            for item in self.bg_sprite:
                if callable(getattr(item, 'update', None)):
                    item.update()
                    
            count = 0
            for item in self.all_sprite:
                if hasattr(item, 'visible'):
                    if item.visible == False:
                        item.visible = True
                        count += 1
                        if count > 1:
                            count = 0
                            break
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            if len(self.block_sprite) != self.counter:
                #print(self.counter, len(self.all_sprite))
                self.score += self.counter - len(self.block_sprite)
                self.scorebox.score = self.score
                self.border.anim_frame = 6
                self.border.updating = True
                self.border2.anim_frame = 6
                self.border.updating = True
                self.counter = len(self.block_sprite)
                beep_array['ahoo'].set_volume(3)
                beep_array['ahoo'].play() if self.settings_dict['sound'] else None
                #print (self.score % (self.box_size[0]*self.box_size[1]), self.score, (self.box_size[0]*self.box_size[1]))
                #print(self.score, self.current_block)
                    
            if self.score != 0 and self.score % self.current_block == 0:
                
                #PUT THE CODE HERE WHEN YOU FINISHED A GAME
                game_next_level()
                        
        def game_display_text():
            text, textRect = textdisplay(self.game_levelname.format(self.lvl), font_color[1], font_typo[6])
            textRect.topleft = dt((705,60))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(self.game_leveltag, font_color[1], font_typo[0])
            textRect.topleft = dt((730,25))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(':{0}'.format(self.timer), font_color[4] if self.k_time_warning else font_color[1], font_typo[7])
            textRect.topleft = dt((688,361))
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(self.game_background)
            
            #pygame.draw.rect(self.gameDisplay, white, [30-5,30-5,640+5,480+5], 3)
            
            self.bg_sprite.draw(self.gameDisplay)
            self.all_sprite.draw(self.gameDisplay)
            
            game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            ### Setting Up the Game
            
            self.k_time_warning = False
            
            self.auto_timer_start = pygame.time.get_ticks()
            self.autoplay = False
            
            self.game_timer_start = pygame.time.get_ticks()
            self.click_timer_start = pygame.time.get_ticks()
            self.click_frequency = 0
            
            self.lvl = self.save_dict['continue'][1]
            self.score = 0
            self.game_pos = 30
            self.rapid = False
            self.block_sprite = pygame.sprite.Group()
            self.all_sprite = pygame.sprite.Group()
            self.bg_sprite = pygame.sprite.Group()
            
            self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,50),2000))
            self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(50,50,0)))
            
            
            '''
            if self.c_still_frame != None:
                self.level_1 = CharacBox(self.c_still_frame, black, (25,25), (750,550),width = 1)
                self.all_sprite.add(self.level_1)
            '''
            
            self.border = BorderBox(self.c_frame_color, *dt2([self.game_pos-5,self.game_pos-5],[640+5,480+5]), 3)
            self.border2 = BorderBox(self.c_frame_color, *dt2([self.game_pos-5-5,self.game_pos-5-5],[650+5,490+5]), 3,6) 
            
            self.all_sprite.add(self.border2)
            self.all_sprite.add(self.border)
            
            self.all_sprite.add(LetterBox('B',black,*dt2([30,522], [43,67]),5,300,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([30+48*1,522], [43,67]),5,400,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([30+48*2,522], [43,67]),5,500,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([30+48*3,522], [43,67]),5,600,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([10+224,522], [43,67]),5,700,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([10+224+48*1,522], [43,67]),5,800,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([10+224+48*2,522], [43,67]),5,900,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([10+224+48*3,522], [43,67]),5,1000,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox_t('Space',red,*dt2([693,480], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Pause Game',black,*dt2([705,503], [90,24]),5,1500,f_typo=font_typo[8]))
            
            self.all_sprite.add(LetterBox_t('Esc',blue,*dt2([693,530], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Quit',black,*dt2([715,553], [46,24]),5,1500,f_typo=font_typo[8]))
            
            self.box_size = (8,6)
            self.max = self.box_size[0] * self.box_size[1]
            self.scorebox = (ScoreBox(yellow, *dt2((445,547),(220,17)),0,self.max,1500))
            
            
            if self.settings_dict['music']: playmusic(self.game_music, repeat = -1)
            
            ### End of SET UP
            
            game_new_level()
            
        
        def game_new_level():
            
            self.timer = self.game_time_limit
            
            self.lasttick = pygame.time.get_ticks()
            
            self.all_sprite.add(self.scorebox)
            
            
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    #r = random.randrange(1,7+1)
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.lvl, phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    '''
                    if r == 1: x = (BlockBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 2: x = (SyncBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 3: x = (SubtracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 4: x = (MythicBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 5: x = (CracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 6: x = (JacBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 7: x = (DrawBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    '''
                    
                    if blok == None:
                        continue
                    
                    
                    
                    
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
                    
            
            
            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        def game_next_level():
            
            self.timer = self.game_time_limit
            self.k_time_warning = False
            self.score = 0
            self.lasttick = pygame.time.get_ticks()
            self.scorebox.score = 0
            

            self.lvl += 1
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.lvl, phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    
                    if blok == None:
                        continue
                    
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        
        
        def game_loop():
            
            game_start()
                
            while 'L' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()


    def SceneM(self): 
        
        def game_control(): #put all the game logic here
            
            for event in pygame.event.get():
                
                if event.type == MUSIC_ENDED:
                    self.game_music = random.choice(lounge_array)
                    if self.settings_dict['music']: playmusic(self.game_music)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass #print (pygame.mouse.get_pos())

                if event.type == pygame.QUIT:
                    self.running = ''
                    
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_F1:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.autoplay ^= True
                    
                    if event.key == pygame.K_SPACE:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.running += 'Q'
                        
                    elif event.key == pygame.K_ESCAPE:
                        beep_array['pow02'].play() if self.settings_dict['sound'] else None
                        self.running += 'P'
                    
                    if event.key in (pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6\
                                     ,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_1,pygame.K_2,pygame.K_3\
                                     ,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9) and self.settings_dict['sound']:
                        beep_array['beep04'].set_volume(0.1)
                        beep_array['beep04'].play() if self.settings_dict['sound'] else None
                        
                    self.click_frequency += 1
                    
                    if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 1
                                self.rapid = True
                            
                    
                    elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 2
                                self.rapid = True
                                
                                
                    elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 3
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 4
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP5 or event.key == pygame.K_5:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 5
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 6
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 7
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 8
                                self.rapid = True
                                
                    elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if hasattr(item, 'updating'):
                                        item.updating = True
                                    item.pending_input = 9
                                self.rapid = True
                        
                if event.type == pygame.KEYUP:
                    self.rapid = False

        def game_system(): #try your best to put all the input functions here
            game_control()

            if "Q" in self.running:
                self.SceneQ()
            elif "P" in self.running:
                self.SceneP()
                
            '''self.border.size = (self.border.size[0],self.border.size[1]-1)
            self.border.updating = True'''
                
            if self.lasttick + 1000 < pygame.time.get_ticks():
                if self.timer <= 10:
                    beep_array['blip19'].set_volume(0.3)
                    beep_array['blip19'].play() if self.settings_dict['sound'] else None
                    self.j_time_warning = True
                self.timer -= 1
    
                self.lasttick = pygame.time.get_ticks()
            
            if self.autoplay:
                if self.auto_timer_start + autoplay_delay < pygame.time.get_ticks():
                    beep_array['beep04'].set_volume(0.1)
                    beep_array['beep04'].play() if self.settings_dict['sound'] else None
                    inp = random.randint(1,9)
                    for item in self.all_sprite:
                        if hasattr(item, 'pending_input'):
                            if hasattr(item, 'updating'):
                                item.updating = True
                            item.pending_input = inp
                        self.auto_timer_start = pygame.time.get_ticks()
            
            if self.click_timer_start + 1000 < pygame.time.get_ticks():
                self.click_average = (self.click_average + self.click_frequency)/2
                self.click_frequency = 0
                self.click_timer_start = pygame.time.get_ticks()
            
            if self.timer < 1:
                beep_array['pow02'].play() if self.settings_dict['sound'] else None
                self.command = 'classic_end'
                self.game_timer_end = pygame.time.get_ticks()
                self.running = 'F'
            
            for item in self.bg_sprite:
                if callable(getattr(item, 'update', None)):
                    item.update()

            count = 0
            for item in self.all_sprite:
                if hasattr(item, 'visible'):
                    if item.visible == False:
                        item.visible = True
                        count += 1
                        if count > trans_speed:
                            count = 0
                            break
                
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            if len(self.block_sprite) != self.counter:
                
                #print(self.counter, len(self.all_sprite))
                self.score += self.counter - len(self.block_sprite)
                self.scorebox.score = self.score
                
                self.border.anim_frame = 6
                self.border.updating = True
                
                #self.border2.anim_frame = 6
                #self.border2.updating = True
                
                
                '''if self.bg_gamefield != None:
                    self.bg_gamefield[1] += 1
                    self.bg_gamefield[1] %= len(bg_neon[self.bg_gamefield[0]])
                    self.j_bg.char = bg_neon[self.bg_gamefield[0]][self.bg_gamefield[1]]
                    self.j_bg.updating = True'''
                    
                self.counter = len(self.block_sprite)
                beep_array['pow05'].set_volume(0.3)
                beep_array['pow05'].play() if self.settings_dict['sound'] else None
                #print (self.score % (self.box_size[0]*self.box_size[1]), self.score, (self.box_size[0]*self.box_size[1]))
                #print(self.score, self.current_block)
                    
            if self.score != 0 and self.score % self.current_block == 0:
                
                #PUT THE CODE HERE WHEN YOU FINISHED A GAME
                game_next_level()
                        
        def game_display_text():
            text, textRect = textdisplay(self.game_levelname.format(self.classic_score+1, self.lvl), font_color[1], font_typo[6])
            textRect.topleft = dt((705,60))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(self.game_leveltag, font_color[1], font_typo[0])
            textRect.topleft = dt((730,25))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(':{0}'.format(self.timer), font_color[4] if self.j_time_warning else font_color[1], font_typo[7])
            textRect.topleft = dt((688,361))
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(self.game_background)
            
            #pygame.draw.rect(self.gameDisplay, white, [30-5,30-5,640+5,480+5], 3)
            
            self.bg_sprite.draw(self.gameDisplay)
            self.all_sprite.draw(self.gameDisplay)
            
            game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            ### Setting Up the Game
            
            self.command = 'classic'
            
            self.j_time_warning = False
            
            self.auto_timer_start = pygame.time.get_ticks()
            self.autoplay = False
            
            self.game_timer_start = pygame.time.get_ticks()
            self.click_timer_start = pygame.time.get_ticks()
            self.click_frequency = 0
            
            self.lvl = 1
            self.score = 0
            self.game_pos = 30
            self.rapid = False
            self.block_sprite = pygame.sprite.Group()
            self.all_sprite = pygame.sprite.Group()
            self.bg_sprite = pygame.sprite.Group()
            
            self.border = BorderBox_t(self.c_frame_color, *dt2([0,0],[800,600]), 3)
            #self.border2 = BorderBox(self.c_frame_color, *dt2([self.game_pos-5-5,self.game_pos-5-5],[650+5,490+5]), 3,6) 
            #self.all_sprite.add(self.border2)
            self.all_sprite.add(self.border)
            
            '''
            if self.c_still_frame != None:
                self.level_1 = CharacBox(self.c_still_frame, black, (25,25), (750,550),width = 1)
                self.all_sprite.add(self.level_1)
            '''
            
            if self.bg_gamefield != None:
                self.j_bg = CharacBox(bg_neon[self.bg_gamefield], black, *dt2([0,0],[800,600]), width = 1,static=True)
                self.all_sprite.add(self.j_bg)
            
            
            self.all_sprite.add(CharacBox(bloom, black, *dt2([0,0],[800,600]), width = 1,static = True))
                
            
            #self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,50),2000))
            self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(10,10,0)))

            self.all_sprite.add(LetterBox('B',black,*dt2([30,522], [43,67]),5,300,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([30+48*1,522], [43,67]),5,400,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([30+48*2,522], [43,67]),5,500,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([30+48*3,522], [43,67]),5,600,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([10+224,522], [43,67]),5,700,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([10+224+48*1,522], [43,67]),5,800,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([10+224+48*2,522], [43,67]),5,900,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([10+224+48*3,522], [43,67]),5,1000,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox_t('Space',red,*dt2([693,480], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Pause Game',black,*dt2([705,503], [90,24]),5,1500,f_typo=font_typo[8]))
            
            self.all_sprite.add(LetterBox_t('Esc',blue,*dt2([693,530], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Quit',black,*dt2([715,553], [46,24]),5,1500,f_typo=font_typo[8]))
            
            self.box_size = (8,6)
            self.max = self.box_size[0] * self.box_size[1]
            self.scorebox = (ScoreBox(yellow, *dt2((445,547),(220,17)),0,self.max,1500))
            
            if self.classic_score == 0:
                if self.settings_dict['music']: playmusic(self.game_music)
            
            ### End of SET UP
            
            game_new_level()
            
        
        def game_new_level():
            
            self.timer = self.game_time_limit
            
            self.lasttick = pygame.time.get_ticks()
            
            self.all_sprite.add(self.scorebox)
            
            
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    #r = random.randrange(1,7+1)
                    
                    blok = block_gen_classic(dt((self.game_pos + 80*x,self.game_pos + 80*y)), stage = self.classic_level, phase = self.lvl, array_loc = (x,y))
                    
                    '''
                    if r == 1: x = (BlockBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 2: x = (SyncBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 3: x = (SubtracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 4: x = (MythicBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 5: x = (CracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 6: x = (JacBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 7: x = (DrawBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    '''
                    
                    if blok == None:
                        continue
                         
                    
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
                    
                    
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        def game_next_level():
            
            self.timer = self.game_time_limit
            self.j_time_warning = False
            self.score = 0
            self.lasttick = pygame.time.get_ticks()
            self.scorebox.score = 0
            
            self.lvl += 1
            if self.lvl > len(classic_layouts[self.classic_level]['phases']):
                self.game_timer_end = pygame.time.get_ticks()
                self.command = 'classic'
                self.running = '9'
                beep_array['pow18'].play() if self.settings_dict['sound'] else None
                self.classic_score += 1
                return None
            
            
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    blok = block_gen_classic(dt((self.game_pos + 80*x,self.game_pos + 80*y)), stage = self.classic_level, phase = self.lvl, array_loc = (x,y))
                    
                    if blok == None:
                        continue
                    
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
            
            
        
        
        
        def game_loop():
            
            game_start()
                
            while 'M' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()
    
    
    def SceneR(self): 
        
        def game_control(): #put all the game logic here
            
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass #print (pygame.mouse.get_pos())

                if event.type == pygame.QUIT:
                    self.running = ''
                    
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_F1:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.autoplay ^= True
                        
                    
                    if event.key == pygame.K_SPACE:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.running += 'Q'
                        
                    elif event.key == pygame.K_ESCAPE:
                        beep_array['pow02'].play() if self.settings_dict['sound'] else None
                        self.running += 'P'
                    
                    if event.key in (pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6\
                                     ,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_1,pygame.K_2,pygame.K_3\
                                     ,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9) and self.settings_dict['sound']:
                        beep_array['beep04'].set_volume(0.1)
                        beep_array['beep04'].play() if self.settings_dict['sound'] else None
                        
                    self.click_frequency += 1
                    
                    if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                        if self.scr_but[1].color != white:
                            self.scr_but[1].color = white
                            self.scr_but[1].updating = True
                        else:
                            self.scr_but[1].color = black
                            self.scr_but[1].updating = True
                            
                    
                    elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                        if self.scr_but[2].color != white:
                            self.scr_but[2].color = white
                            self.scr_but[2].updating = True
                        else:
                            self.scr_but[2].color = black
                            self.scr_but[2].updating = True
                                
                    elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                        if self.scr_but[3].color != white:
                            self.scr_but[3].color = white
                            self.scr_but[3].updating = True
                        else:
                            self.scr_but[3].color = black
                            self.scr_but[3].updating = True
                                
                    elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                        if self.scr_but[4].color != white:
                            self.scr_but[4].color = white
                            self.scr_but[4].updating = True
                        else:
                            self.scr_but[4].color = black
                            self.scr_but[4].updating = True
                                
                    elif event.key == pygame.K_KP5 or event.key == pygame.K_5:
                        if self.scr_but[5].color != white:
                            self.scr_but[5].color = white
                            self.scr_but[5].updating = True
                        else:
                            self.scr_but[5].color = black
                            self.scr_but[5].updating = True
                                
                    elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                        if self.scr_but[6].color != white:
                            self.scr_but[6].color = white
                            self.scr_but[6].updating = True
                        else:
                            self.scr_but[6].color = black
                            self.scr_but[6].updating = True
                                
                    elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                        if self.scr_but[7].color != white:
                            self.scr_but[7].color = white
                            self.scr_but[7].updating = True
                        else:
                            self.scr_but[7].color = black
                            self.scr_but[7].updating = True
                                
                    elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                        if self.scr_but[8].color != white:
                            self.scr_but[8].color = white
                            self.scr_but[8].updating = True
                        else:
                            self.scr_but[8].color = black
                            self.scr_but[8].updating = True
                                
                    elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                        if self.scr_but[9].color != white:
                            self.scr_but[9].color = white
                            self.scr_but[9].updating = True
                        else:
                            self.scr_but[9].color = black
                            self.scr_but[9].updating = True
                        
                if event.type == pygame.KEYUP:
                    self.rapid = False

        def game_system(): #try your best to put all the input functions here
            game_control()

            if "Q" in self.running:
                self.SceneQ()
            elif "P" in self.running:
                self.SceneP()
                
            '''self.border.size = (self.border.size[0],self.border.size[1]-1)
            self.border.updating = True'''
            
            for item in self.all_sprite:
                
                if hasattr(item, 'pending_input'):
                    
                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                        
                        item.image.set_alpha(255)
                        
                        if isinstance(item, (JacBox)):
                            #print (item.visible)
                            if not item.visc:
                                item.image.set_colorkey((1,1,1))
                                item.image.set_alpha(40)
                            
                        item.updating = True
                        
                    elif item.image.get_alpha() == 255 or item.image.get_alpha() == 25:
                        
                        if isinstance(item, (JacBox)):
                            item.image.set_colorkey(black)
                            
                        item.image.set_alpha(alpha_game_block)
                        item.updating = True
            
            if self.influ.beep == 1:
                beep_array['blip06'].set_volume(0.1)
                beep_array['blip06'].play() if self.settings_dict['sound'] else None
                self.influ.beep = 0
            elif self.influ.beep == 2:
                beep_array['blip02'].set_volume(0.1)
                beep_array['blip02'].play() if self.settings_dict['sound'] else None
                self.influ.beep = 0
            
            if len(self.proc_queue) == 0:
                for i in self.scr_but:
                    if self.scr_but[i].color == white:
                        self.inp_queue.append(i)
                self.proc_queue = self.inp_queue
            
            if len(self.proc_queue) != 0:
                if self.auto_timer_start + autoplay_delay//3 < pygame.time.get_ticks():
                    beep_array['beep04'].set_volume(0.1)
                    beep_array['beep04'].play() if self.settings_dict['sound'] else None
                    
                    x = self.proc_queue.pop(0)
                    inp = x
                    self.scr_but[x].anim_frame = 3
                    self.scr_but[x].updating = True
                    self.scr_but[x].static = False
                    
                    for item in self.all_sprite:
                        if hasattr(item, 'pending_input'):
                            if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                if hasattr(item, 'updating'):
                                    item.updating = True
                                item.pending_input = inp
                        self.auto_timer_start = pygame.time.get_ticks()    
                
            if self.lasttick + 1000 < pygame.time.get_ticks():
                if self.timer <= 10:
                    beep_array['blip19'].set_volume(0.3)
                    beep_array['blip19'].play() if self.settings_dict['sound'] else None
                    self.j_time_warning = True
                self.timer -= 1
    
                self.lasttick = pygame.time.get_ticks()
            
            if self.click_timer_start + 1000 < pygame.time.get_ticks():
                self.click_average = (self.click_average + self.click_frequency)/2
                self.click_frequency = 0
                self.click_timer_start = pygame.time.get_ticks()
            
            if self.timer < 1:
                beep_array['pow02'].play() if self.settings_dict['sound'] else None
                if (self.lvl - 1) > self.save_dict['idle']:
                    self.save_dict['idle'] = self.lvl - 1
                self.game_timer_end = pygame.time.get_ticks()
                self.running = 'F'
            
            for item in self.bg_sprite:
                if callable(getattr(item, 'update', None)):
                    item.update()

            count = 0
            for item in self.all_sprite:
                if hasattr(item, 'visible'):
                    if item.visible == False:
                        item.visible = True
                        count += 1
                        if count > trans_speed:
                            count = 0
                            break
                
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            if len(self.block_sprite) != self.counter:
                
                #print(self.counter, len(self.all_sprite))
                self.score += self.counter - len(self.block_sprite)
                self.scorebox.score = self.score
                
                self.border.anim_frame = 6
                self.border.updating = True
                
                #self.border2.anim_frame = 6
                #self.border2.updating = True
                
                
                '''if self.bg_gamefield != None:
                    self.bg_gamefield[1] += 1
                    self.bg_gamefield[1] %= len(bg_neon[self.bg_gamefield[0]])
                    self.j_bg.char = bg_neon[self.bg_gamefield[0]][self.bg_gamefield[1]]
                    self.j_bg.updating = True'''
                    
                self.counter = len(self.block_sprite)
                beep_array['pow05'].set_volume(0.3)
                beep_array['pow05'].play() if self.settings_dict['sound'] else None
                #print (self.score % (self.box_size[0]*self.box_size[1]), self.score, (self.box_size[0]*self.box_size[1]))
                #print(self.score, self.current_block)
                    
            if self.score != 0 and self.score % self.current_block == 0:
                
                #PUT THE CODE HERE WHEN YOU FINISHED A GAME
                game_next_level()
                        
        def game_display_text():
            text, textRect = textdisplay(self.game_levelname.format(self.lvl), font_color[1], font_typo[6])
            textRect.topleft = dt((705,60))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(self.game_leveltag, font_color[1], font_typo[0])
            textRect.topleft = dt((730,25))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(':{0}'.format(self.timer), font_color[4] if self.j_time_warning else font_color[1], font_typo[7])
            textRect.topleft = dt((688,361))
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(self.game_background)
            
            #pygame.draw.rect(self.gameDisplay, white, [30-5,30-5,640+5,480+5], 3)
            
            self.bg_sprite.draw(self.gameDisplay)
            self.all_sprite.draw(self.gameDisplay)
            
            game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            ### Setting Up the Game
            
            self.inp_queue = []
            self.proc_queue = []
            
            self.j_time_warning = False
            
            self.auto_timer_start = pygame.time.get_ticks()
            self.autoplay = False
            
            self.game_timer_start = pygame.time.get_ticks()
            self.click_timer_start = pygame.time.get_ticks()
            self.click_frequency = 0
            
            self.lvl = 1
            self.score = 0
            self.game_pos = game_pos
            self.rapid = False
            self.block_sprite = pygame.sprite.Group()
            self.all_sprite = pygame.sprite.Group()
            self.bg_sprite = pygame.sprite.Group()
            
            self.border = BorderBox_t(self.c_frame_color, *dt2([0,0],[800,600]), 3)
            #self.border2 = BorderBox(self.c_frame_color, *dt2([self.game_pos-5-5,self.game_pos-5-5],[650+5,490+5]), 3,6) 
            #self.all_sprite.add(self.border2)
            self.all_sprite.add(self.border)
            
            '''
            if self.c_still_frame != None:
                self.level_1 = CharacBox(self.c_still_frame, black, (25,25), (750,550),width = 1)
                self.all_sprite.add(self.level_1)
            '''
            
            if self.bg_gamefield != None:
                self.j_bg = CharacBox(bg_neon[self.bg_gamefield], black, *dt2([0,0],[800,600]), width = 1,static=True)
                self.all_sprite.add(self.j_bg)
            
            
            self.all_sprite.add(CharacBox(bloom, black, *dt2([0,0],[800,600]), width = 1,static = True))
                
            
            #self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,50),2000))
            #self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(10,10,0)))

            self.all_sprite.add(LetterBox('B',black,*dt2([30,522], [43,67]),5,300,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([30+48*1,522], [43,67]),5,400,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([30+48*2,522], [43,67]),5,500,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([30+48*3,522], [43,67]),5,600,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([10+224,522], [43,67]),5,700,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([10+224+48*1,522], [43,67]),5,800,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([10+224+48*2,522], [43,67]),5,900,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([10+224+48*3,522], [43,67]),5,1000,f_typo=font_typo[5]))
            
            self.scr_but = dict()
            
            self.scr_but[7] = (LetterBox('7',black,*dt2([686,250+20], [30,30]),5,300,f_typo=font_typo[17]))
            self.scr_but[8] = (LetterBox('8',black,*dt2([720,250+20], [30,30]),5,300,f_typo=font_typo[17]))
            self.scr_but[9] = (LetterBox('9',black,*dt2([754,250+20], [30,30]),5,300,f_typo=font_typo[17]))
            self.scr_but[4] = (LetterBox('4',black,*dt2([686,284+20], [30,30]),5,300,f_typo=font_typo[17]))
            self.scr_but[5] = (LetterBox('5',black,*dt2([720,284+20], [30,30]),5,300,f_typo=font_typo[17]))
            self.scr_but[6] = (LetterBox('6',black,*dt2([754,284+20], [30,30]),5,300,f_typo=font_typo[17]))
            self.scr_but[1] = (LetterBox('1',black,*dt2([686,317+20], [30,30]),5,300,f_typo=font_typo[17]))
            self.scr_but[2] = (LetterBox('2',black,*dt2([720,317+20], [30,30]),5,300,f_typo=font_typo[17]))
            self.scr_but[3] = (LetterBox('3',black,*dt2([754,317+20], [30,30]),5,300,f_typo=font_typo[17]))
            
            for i in self.scr_but:
                self.all_sprite.add(self.scr_but[i])
            
            self.all_sprite.add(LetterBox_t('Space',red,*dt2([693,480], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Pause Game',black,*dt2([705,503], [90,24]),5,1500,f_typo=font_typo[8]))
            
            self.all_sprite.add(LetterBox_t('Esc',blue,*dt2([693,530], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Quit',black,*dt2([715,553], [46,24]),5,1500,f_typo=font_typo[8]))
            
            self.box_size = (8,6)
            self.max = self.box_size[0] * self.box_size[1]
            self.scorebox = (ScoreBox(yellow, *dt2((445,547),(220,17)),0,self.max,1500))
            
            
            if self.settings_dict['music']: playmusic(self.game_music)
            
            ### End of SET UP
            
            game_new_level()
            
        
        def game_new_level():
            
            self.influ = (InfluBox(((80*self.box_size[0]//3),(80*self.box_size[1]//3)),(game_pos,game_pos,80*self.box_size[0],80*self.box_size[1])))
            self.all_sprite.add(self.influ)
            
            self.influ2 = (InfluBox(((80*self.box_size[0]//2),(80*self.box_size[1]//2)),(game_pos,game_pos,80*self.box_size[0],80*self.box_size[1])))
            self.influ2.xm = self.influ2.ym = -1
            self.all_sprite.add(self.influ2)
            
            self.timer = int(self.game_time_limit * 2)
            
            self.lasttick = pygame.time.get_ticks()
            
            self.all_sprite.add(self.scorebox)
            
            
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.lvl, phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    if blok == None:
                        continue
                    
                    blok.image.set_alpha(alpha_game_block)
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 

            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        def game_next_level():
            
            self.timer = int(self.game_time_limit * 2)
            self.j_time_warning = False
            self.score = 0
            self.lasttick = pygame.time.get_ticks()
            self.scorebox.score = 0
            
            self.lvl += 1
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.lvl, phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    if blok == None:
                        continue
                    
                    blok.image.set_alpha(alpha_game_block)
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        
        
        def game_loop():
            
            game_start()
                
            while 'R' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()

    def SceneS(self): 
        
        def game_control(): #put all the game logic here
            
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass #print (pygame.mouse.get_pos())

                if event.type == pygame.QUIT:
                    self.running = ''
                    
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_F1:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.autoplay ^= True
                        
                    
                    if event.key == pygame.K_SPACE:
                        beep_array['pow11'].play() if self.settings_dict['sound'] else None
                        self.running += 'Q'
                        
                    elif event.key == pygame.K_ESCAPE:
                        beep_array['pow02'].play() if self.settings_dict['sound'] else None
                        self.running += 'P'
                    
                    if event.key in (pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6\
                                     ,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_1,pygame.K_2,pygame.K_3\
                                     ,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9) and self.settings_dict['sound']:
                        beep_array['beep04'].set_volume(0.1)
                        beep_array['beep04'].play() if self.settings_dict['sound'] else None
                        
                    self.click_frequency += 1
                    
                    if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 1
                                    self.rapid = True
                            
                    
                    elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 2
                                    self.rapid = True
                                
                                
                    elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 3
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 4
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP5 or event.key == pygame.K_5:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 5
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 6
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 7
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 8
                                    self.rapid = True
                                
                    elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                        if self.rapid == False:
                            for item in self.all_sprite:
                                if hasattr(item, 'pending_input'):
                                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                        if hasattr(item, 'updating'):
                                            item.updating = True
                                        item.pending_input = 9
                                    self.rapid = True
                        
                if event.type == pygame.KEYUP:
                    self.rapid = False

        def game_system(): #try your best to put all the input functions here
            game_control()

            if "Q" in self.running:
                self.SceneQ()
            elif "P" in self.running:
                self.SceneP()
                
            for item in self.all_sprite:
                
                if hasattr(item, 'pending_input'):
                    
                    if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                        
                        item.image.set_alpha(255)
                        
                        if isinstance(item, (JacBox)):
                            #print (item.visible)
                            if not item.visc:
                                item.image.set_colorkey((1,1,1))
                                item.image.set_alpha(40)
                            
                        item.updating = True
                        
                    elif item.image.get_alpha() == 255 or item.image.get_alpha() == 25:
                        
                        if isinstance(item, (JacBox)):
                            item.image.set_colorkey(black)
                            
                        item.image.set_alpha(alpha_game_block)
                        item.updating = True
            
            if self.blacktick + 5000 < pygame.time.get_ticks():
                self.blacktick = pygame.time.get_ticks()
                for i in range(len(self.black)):
                    x = random.randint(1,7)
                    y = random.randint(1,5)
                    self.black[i] = pygame.Rect((30+(80*x),30+(80*y),80*random.randint(1,8-x),80*random.randint(1,6-y)))

            
            if self.influ.beep == 1:
                beep_array['blip06'].set_volume(0.1)
                beep_array['blip06'].play() if self.settings_dict['sound'] else None
                self.influ.beep = 0
            elif self.influ.beep == 2:
                beep_array['blip02'].set_volume(0.1)
                beep_array['blip02'].play() if self.settings_dict['sound'] else None
                self.influ.beep = 0
            
            if self.autoplay:
                if self.auto_timer_start + autoplay_delay < pygame.time.get_ticks():
                    beep_array['beep04'].set_volume(0.1)
                    beep_array['beep04'].play() if self.settings_dict['sound'] else None
                    inp = random.randint(1,9)
                    for item in self.all_sprite:
                        if hasattr(item, 'pending_input'):
                            if self.influ.rect.colliderect(item.rect) or self.influ2.rect.colliderect(item.rect):
                                if hasattr(item, 'updating'):
                                    item.updating = True
                                item.pending_input = inp
                        self.auto_timer_start = pygame.time.get_ticks()    
                
            if self.lasttick + 1000 < pygame.time.get_ticks():
                if self.timer <= 10:
                    beep_array['blip19'].set_volume(0.3)
                    beep_array['blip19'].play() if self.settings_dict['sound'] else None
                    self.j_time_warning = True
                self.timer -= 1
    
                self.lasttick = pygame.time.get_ticks()
            
            if self.click_timer_start + 1000 < pygame.time.get_ticks():
                self.click_average = (self.click_average + self.click_frequency)/2
                self.click_frequency = 0
                self.click_timer_start = pygame.time.get_ticks()
            
            if self.timer < 1:
                beep_array['pow02'].play() if self.settings_dict['sound'] else None
                if (self.lvl - 1) > self.save_dict['idle']:
                    self.save_dict['blackout'] = self.lvl - 1
                self.game_timer_end = pygame.time.get_ticks()
                self.running = 'F'
            
            for item in self.bg_sprite:
                if callable(getattr(item, 'update', None)):
                    item.update()

            count = 0
            for item in self.all_sprite:
                if hasattr(item, 'visible'):
                    if item.visible == False:
                        item.visible = True
                        count += 1
                        if count > trans_speed:
                            count = 0
                            break
                
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
            if len(self.block_sprite) != self.counter:
                
                #print(self.counter, len(self.all_sprite))
                self.score += self.counter - len(self.block_sprite)
                self.scorebox.score = self.score
                
                self.border.anim_frame = 6
                self.border.updating = True
               
                self.counter = len(self.block_sprite)
                beep_array['pow05'].set_volume(0.3)
                beep_array['pow05'].play() if self.settings_dict['sound'] else None
                #print (self.score % (self.box_size[0]*self.box_size[1]), self.score, (self.box_size[0]*self.box_size[1]))
                #print(self.score, self.current_block)
                    
            if self.score != 0 and self.score % self.current_block == 0:
                
                #PUT THE CODE HERE WHEN YOU FINISHED A GAME
                game_next_level()
                        
        def game_display_text():
            text, textRect = textdisplay(self.game_levelname.format(self.lvl), font_color[1], font_typo[6])
            textRect.topleft = dt((705,60))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(self.game_leveltag, font_color[1], font_typo[0])
            textRect.topleft = dt((730,25))
            text = pygame.transform.rotate(text, 270)
            self.gameDisplay.blit(text, textRect)
            
            text, textRect = textdisplay(':{0}'.format(self.timer), font_color[4] if self.j_time_warning else font_color[1], font_typo[7])
            textRect.topleft = dt((688,361))
            self.gameDisplay.blit(text, textRect)
        
        def game_display(): #put all the game output here

            self.gameDisplay.fill(self.game_background)
            
            #pygame.draw.rect(self.gameDisplay, white, [30-5,30-5,640+5,480+5], 3)
            
            self.bg_sprite.draw(self.gameDisplay)
            self.all_sprite.draw(self.gameDisplay)
            
            for i in self.black:
                pygame.draw.rect(self.gameDisplay,black,i)
            
            game_display_text()
            
            pygame.display.flip()
        
        ##Main Game Loop
        
        def game_start():
            
            ### Setting Up the Game

            self.blacktick = pygame.time.get_ticks()
            
            self.black = list()
            for i in range(5):
                x = random.randint(1,7)
                y = random.randint(1,5)
                self.black.append(pygame.Rect((30+(80*x),30+(80*y),80*random.randint(1,8-x),80*random.randint(1,6-y))))
            
            
            self.j_time_warning = False
            
            self.auto_timer_start = pygame.time.get_ticks()
            self.autoplay = False
            
            self.game_timer_start = pygame.time.get_ticks()
            self.click_timer_start = pygame.time.get_ticks()
            self.click_frequency = 0
            
            self.lvl = 1
            self.score = 0
            self.game_pos = game_pos
            self.rapid = False
            self.block_sprite = pygame.sprite.Group()
            self.all_sprite = pygame.sprite.Group()
            self.bg_sprite = pygame.sprite.Group()
            
            self.border = BorderBox_t(self.c_frame_color, *dt2([0,0],[800,600]), 3)
            #self.border2 = BorderBox(self.c_frame_color, *dt2([self.game_pos-5-5,self.game_pos-5-5],[650+5,490+5]), 3,6) 
            #self.all_sprite.add(self.border2)
            self.all_sprite.add(self.border)
            
            '''
            if self.c_still_frame != None:
                self.level_1 = CharacBox(self.c_still_frame, black, (25,25), (750,550),width = 1)
                self.all_sprite.add(self.level_1)
            '''
            
            if self.bg_gamefield != None:
                self.j_bg = CharacBox(bg_neon[self.bg_gamefield], black, *dt2([0,0],[800,600]), width = 1,static=True)
                self.all_sprite.add(self.j_bg)
            
            
            self.all_sprite.add(CharacBox(bloom, black, *dt2([0,0],[800,600]), width = 1,static = True))
                
            
            #self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(0,0,50),2000))
            #self.bg_sprite.add(BackgroundBox((0,0),dt((1600,1600)),(10,10,0)))

            self.all_sprite.add(LetterBox('B',black,*dt2([30,522], [43,67]),5,300,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([30+48*1,522], [43,67]),5,400,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([30+48*2,522], [43,67]),5,500,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([30+48*3,522], [43,67]),5,600,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox('B',black,*dt2([10+224,522], [43,67]),5,700,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('L',black,*dt2([10+224+48*1,522], [43,67]),5,800,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('O',black,*dt2([10+224+48*2,522], [43,67]),5,900,f_typo=font_typo[5]))
            self.all_sprite.add(LetterBox('K',black,*dt2([10+224+48*3,522], [43,67]),5,1000,f_typo=font_typo[5]))
            
            self.all_sprite.add(LetterBox_t('Space',red,*dt2([693,480], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Pause Game',black,*dt2([705,503], [90,24]),5,1500,f_typo=font_typo[8]))
            
            self.all_sprite.add(LetterBox_t('Esc',blue,*dt2([693,530], [46,24]),5,1500,f_typo=font_typo[8]))
            self.all_sprite.add(LetterBox_t('Quit',black,*dt2([715,553], [46,24]),5,1500,f_typo=font_typo[8]))
            
            self.box_size = (8,6)
            self.max = self.box_size[0] * self.box_size[1]
            self.scorebox = (ScoreBox(yellow, *dt2((445,547),(220,17)),0,self.max,1500))
            
            
            if self.settings_dict['music']: playmusic(self.game_music)
            
            ### End of SET UP
            
            game_new_level()
            
        
        def game_new_level():
            
            self.influ = (InfluBox(((80*self.box_size[0]//3),(80*self.box_size[1]//3)),(game_pos,game_pos,80*self.box_size[0],80*self.box_size[1])))
            self.all_sprite.add(self.influ)
            
            self.influ2 = (InfluBox(((80*self.box_size[0]//2),(80*self.box_size[1]//2)),(game_pos,game_pos,80*self.box_size[0],80*self.box_size[1])))
            self.influ2.xm = self.influ2.ym = -1
            self.all_sprite.add(self.influ2)
            
            self.timer = int(self.game_time_limit * 2)
            
            self.lasttick = pygame.time.get_ticks()
            
            self.all_sprite.add(self.scorebox)
            
            
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    #r = random.randrange(1,7+1)
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.save_dict['continue'][1], phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    '''
                    if r == 1: x = (BlockBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 2: x = (SyncBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))   
                    elif r == 3: x = (SubtracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 4: x = (MythicBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5))  
                    elif r == 5: x = (CracBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 6: x = (JacBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    elif r == 7: x = (DrawBox((self.game_pos + 80*x,self.game_pos + 80*y),(75,75),5)) 
                    '''
                    
                    if blok == None:
                        continue
                         
                    blok.image.set_alpha(alpha_game_block)
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 

            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        def game_next_level():
            
            self.timer = int(self.game_time_limit * 2)
            self.j_time_warning = False
            self.score = 0
            self.lasttick = pygame.time.get_ticks()
            self.scorebox.score = 0
            
            self.lvl += 1
            for y in range(self.box_size[1]):
                for x in range(self.box_size[0]):
                    
                    blok = block_gen(dt((self.game_pos + 80*x,self.game_pos + 80*y)), level = self.save_dict['continue'][0] ,stage = self.save_dict['continue'][1], phase = self.save_dict['continue'][2], array_loc = (x,y))
                    
                    
                    if blok == None:
                        continue
                    
                    blok.image.set_alpha(alpha_game_block)
                    self.block_sprite.add(blok) 
                    self.all_sprite.add(blok) 
            
            self.counter = len(self.block_sprite)
            self.current_block = self.counter
            self.scorebox.max = self.current_block
        
        
        
        def game_loop():
            
            game_start()
                
            while 'S' in self.running:
                
                game_system()
                game_display()
                
                self.clock.tick(fps)
                
        game_loop()
    

    def SceneQ(self):
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.unpause()
                        self.running = self.running.replace('Q', '')
                        
        def game_system(): #try your best to put all the input functions here
            game_control()
            
            for item in self.pause_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
        def game_display_text():
            text, textRect = textdisplay('Hello#2' , (black, None), font_typo[1])
            textRect.topleft = (200,200)
            self.gameDisplay.blit(text, textRect)    
            
        def game_display(): #put all the game output here
            
            self.pause_sprite.draw(self.gameDisplay)
            
            #game_display_text()
            
            pygame.display.flip()
            
        def game_loop():
            
            pygame.mixer.music.pause()
            
            self.lasttick = pygame.time.get_ticks()

            self.pause_sprite = pygame.sprite.Group()
            
            self.pause_sprite.add(LetterBox('',self.c_frame_color,*dt2([30-5,30-5], [640+5,480+5]),5, bg_color=self.game_background))
            self.pause_sprite.add(LetterBox('',self.c_frame_color,*dt2([30-5-5,30-5-5],[650+5,490+5]),5,bg_color=self.game_background))
            
            if self.intermission_msg != None:
                self.pause_sprite.add(LetterBox(self.intermission_msg[0],black,*dt2([48,163], [608,95]),5,f_typo = font_typo[5]))
                self.pause_sprite.add(LetterBox(self.intermission_msg[1],black,*dt2([48,246], [608,39]),5,f_typo = font_typo[10]))
                
            self.pause_sprite.add(LetterBox('Paused',black,*dt2([48,296], [608,39]),5,f_typo = font_typo[13]))
            
            self.pause_sprite.add(LetterBox("Press space to continue",black,*dt2([212,436], [281,25]),5,f_typo = font_typo[6],f_color = font_color[1]))
            
            
            while 'Q' in self.running:
                
                game_system()
                game_display()
    
                self.clock.tick(fps)    
        
        game_loop()

    def SceneP(self):
        
        def game_control(): #put all the game logic here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.unpause()
                        self.running = self.running.replace('P', '')
                    elif event.key == pygame.K_ESCAPE:
                        if self.save_dict['continue'][0] != None:
                            self.save_dict['continue'][2] = 1
                            if self.command == 'classic':
                                self.save_dict['classic']
                            json_save(self.save_dict)
                        else:
                            self.save_dict['continue'] = self.endless_save
                            self.classic_score = 0
                            del self.endless_save
                            json_save(self.save_dict)
                        
                        self.running = 'A'
#                         
        def game_system(): #try your best to put all the input functions here
            game_control()
            
            for item in self.pause_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                    
        def game_display_text():
            text, textRect = textdisplay('Hello#2' , (black, None), font_typo[1])
            textRect.topleft = (200,200)
            self.gameDisplay.blit(text, textRect)    
            
        def game_display(): #put all the game output here
            
            self.pause_sprite.draw(self.gameDisplay)
            
            #game_display_text()
            
            pygame.display.flip()
            
        def game_loop():
            
            pygame.mixer.music.pause()
            
            self.lasttick = pygame.time.get_ticks()

            self.pause_sprite = pygame.sprite.Group()
            
            self.pause_sprite.add(LetterBox('',self.c_frame_color,*dt2([30-5,30-5], [640+5,480+5]),5, bg_color=(50,0,0)))
            self.pause_sprite.add(LetterBox('',self.c_frame_color,*dt2([30-5-5,30-5-5],[650+5,490+5]),5,bg_color=(100,0,0)))
            
            self.pause_sprite.add(LetterBox('Confirm Quit',black,*dt2([205, 172], [291,62]),5,f_typo = font_typo[13]))
            
            self.pause_sprite.add(LetterBox("Press Esc to quit",black,*dt2([205,308], [291,25]),5,f_typo = font_typo[10],f_color = font_color[1]))
            self.pause_sprite.add(LetterBox("Press Space to cancel",black,*dt2([205,348], [291,25]),5,f_typo = font_typo[10],f_color = font_color[1]))

            while 'P' in self.running:
                
                game_system()
                game_display()
    
                self.clock.tick(fps)    
        
        game_loop()

        
PygameTemplate()

pygame.quit()