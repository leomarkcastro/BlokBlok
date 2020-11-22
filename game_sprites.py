import pygame
import random
import os
from game_variables import *


game_folder = os.path.dirname(__file__)         #__file__ refers to the current directory of your script


############################################################# 
#SPRITES
#############################################################

#Import the images

img_folder = os.path.join(game_folder, 'img')   # 'img' refers to the folder in the current game dir
char_folder = os.path.join(img_folder, 'char')
blk_folder = os.path.join(img_folder, 'blocks')
still_folder = os.path.join(img_folder, 'frames')
bg_folder = os.path.join(img_folder, 'backgrounds')
tut_folder = os.path.join(img_folder, 'tutorial')

pygame.display.init()
pygame.display.set_mode((screenWidth, screenHeight))

block_sample = pygame.image.load(os.path.join(blk_folder, "blocks.png")).convert()
block_sample.set_colorkey((0,0,0))

player_anim = {'blockA': []}

for frame in range(7):
    block_sample_cut = block_sample.subsurface(pygame.Rect((6+104*frame,6),(101,101)))
    player_anim['blockA'].append(block_sample_cut)
    
girl_sample = pygame.image.load(os.path.join(char_folder, "girl.png")).convert_alpha()
girl_sample = girl_sample.subsurface(pygame.Rect((0,0),(344,450)))

thug_sample = pygame.image.load(os.path.join(char_folder, "under.png")).convert_alpha()

crib_sample = pygame.image.load(os.path.join(char_folder, "crib.png")).convert_alpha()

background_level = (
    pygame.image.load(os.path.join(still_folder, "Club.png")).convert_alpha(),
    pygame.image.load(os.path.join(still_folder, "Under.png")).convert_alpha(),
    pygame.image.load(os.path.join(still_folder, "elite.png")).convert_alpha()
    )

mode_banners = (
    pygame.image.load(os.path.join(still_folder, "banner1.png")).convert_alpha(),
    pygame.image.load(os.path.join(still_folder, "banner2.png")).convert_alpha(),
    pygame.image.load(os.path.join(still_folder, "banner3.png")).convert_alpha(),
    pygame.image.load(os.path.join(still_folder, "banner4.png")).convert_alpha(),
    pygame.image.load(os.path.join(still_folder, "banner6.png")).convert_alpha(),
    )

still_frames= (
    pygame.image.load(os.path.join(still_folder, "club_full.png")).convert_alpha(),
    pygame.image.load(os.path.join(still_folder, "Under_full.png")).convert_alpha(),
    pygame.image.load(os.path.join(still_folder, "elite_full.png")).convert_alpha(),
    pygame.image.load(os.path.join(still_folder, "casual_bg.jpg")).convert_alpha()
    )

tutorial_frames= (
    pygame.image.load(os.path.join(tut_folder, "Slide1.png")),
    pygame.image.load(os.path.join(tut_folder, "Slide2.png")),
    pygame.image.load(os.path.join(tut_folder, "Slide3.png")),
    pygame.image.load(os.path.join(tut_folder, "Slide4.png")),
    pygame.image.load(os.path.join(tut_folder, "Slide5.png"))
    )

bloom = pygame.image.load(os.path.join(img_folder, "SceneJ_bloom.png")).convert_alpha()
tutorial = pygame.image.load(os.path.join(img_folder, "Tutorial.png")).convert_alpha()
bg_fade = pygame.image.load(os.path.join(img_folder, "BG_fade.png")).convert()

bricks = pygame.image.load(os.path.join(img_folder, "bricks.png")).convert_alpha()
light_blue = pygame.image.load(os.path.join(img_folder, "lightBlue.png")).convert_alpha()
light_purple = pygame.image.load(os.path.join(img_folder, "lightPurple.png")).convert_alpha()

dlg = pygame.image.load(os.path.join(img_folder, "dlg.png")).convert_alpha()
dlg2 = pygame.image.load(os.path.join(img_folder, "dlg2.png")).convert_alpha()
dlg_bord = pygame.image.load(os.path.join(img_folder, "dlg_border.png")).convert_alpha()

##BG FODLER###############


bg_neon = {
    'club' : pygame.image.load(os.path.join(bg_folder, "club_neon.png")).convert_alpha(),
    'under' : pygame.image.load(os.path.join(bg_folder, "under_neon.png")).convert_alpha(),
    'crib' : pygame.image.load(os.path.join(bg_folder, "crib_neon.png")).convert_alpha(),
    }



##########################
#Functions

blip_intensity = 1

def blip(array):
    na1 = int(array[0]*blip_intensity) if array[0] != 0 else 0
    na2 = int(array[1]*blip_intensity) if array[1] != 0 else 0
    na3 = int(array[2]*blip_intensity) if array[2] != 0 else 0
    return (na1,na2,na3)


##########################

# Simple Color Box

class ColorBox(pygame.sprite.Sprite):
    def __init__(self, color, pos, size):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.fill(white)
        self.image.set_colorkey(white)
        
        pygame.draw.rect(self.image, color, [0, 0, size[0], size[1]])
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def update(self):
        #self.rect.x += 1
        pass
    
class CharacBox(pygame.sprite.Sprite):
    def __init__(self, char, color, pos, size, width = 0, delay = 0, bg_color = black, static = False, flash = False):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        
        self.bgcolor = bg_color
        self.char = char
        self.color = color
        self.pos = pos
        self.size = size
        self.width = width
        
        self.static = static
        
        self.flash = flash
        self.color_tense = 1
        
        self.cur_color = 0
        
        self.updating = True
        
        self.anim_frame = 6
        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps
        
        self.delay = delay
        self.delay_lasttick = pygame.time.get_ticks()

        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    
    def update(self):
        if (pygame.time.get_ticks() < self.delay_lasttick + self.delay):
            pass
        elif self.static == False:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.blit(pygame.transform.scale(self.char, (self.size[0],self.size[1])),(0,0))
                if self.flash: pygame.draw.rect(self.image, [7*self.color_tense*self.anim_frame*(1 if self.cur_color == 0 else 0) , 7*self.color_tense*self.anim_frame*(1 if self.cur_color == 1 else 0) , 7*self.color_tense*self.anim_frame*(1 if self.cur_color == 2 else 0)], [0, 0, self.size[0], self.size[1]])  
                else: self.image.set_alpha((6-self.anim_frame)/6*alpha_block)
                
                pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
                self.anim_frame -= 1
                
            if self.anim_frame == 0:
                self.static = True
                
        elif self.static:
            self.image = pygame.transform.scale(self.char, (self.size[0],self.size[1]))
            self.updating = False



class BackgroundBox2(pygame.sprite.Sprite):
    def __init__(self, pos, size, color = blue, delay = 0, type = 0):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        
        self.pos = pos
        self.size = size
        self.color = color
        
        self.bg_play = 0
        self.bg_play_type = type
        
        self.top_x = self.max_topx = pos[0] - 375
        self.top_y = self.max_topy = pos[1] - 132
        self.bot_x = size[0] + 31
        self.bot_y = size[1] + 58
        
        self.max_botx = size[0] + 416
        self.max_boty = size[1] + 141
        
        self.move_x = 1
        self.move_y = 1
        
        self.move_sw_tick = pygame.time.get_ticks()
        self.move_sw = 0
        
        self.delay = delay
        self.delay_lasttick = pygame.time.get_ticks()
        
        #print (self.top_x, self.top_y, self.bot_x, self.bot_y, self.max_botx, self.max_boty, (self.max_boty - self.top_y), (self.max_botx - self.top_x))
        
        self.boxsize = (50,50)

        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps 
        
        self.render_bg()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.top_x,self.top_y)
    
    def render_bg(self):
        
        self.image.fill(black)
        
        for y in range((self.max_boty - self.top_y)//self.boxsize[1]):
            for x in range((self.max_botx - self.top_x)//self.boxsize[0]):
                pygame.draw.rect(self.image, (self.color[0], int(self.color[1] * (self.bg_play / screenWidth)) if self.bg_play_type == 1 else self.color[1], int(self.color[2] * (self.bg_play / screenHeight)) if self.bg_play_type == 2 else self.color[2]), \
                                 (self.top_x + self.boxsize[0] * x, self.top_y + self.boxsize[1] * y, self.boxsize[0], self.boxsize[1]),\
                                 3)
        
    
    def update(self):
        
        self.render_bg()
        
        if (pygame.time.get_ticks() > self.delay_lasttick + self.delay):
        
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                
                self.top_x += self.move_x
                self.top_y += self.move_y
                
                self.rect.topleft = (self.top_x,self.top_y)
                
            if (self.move_sw_tick + 3000 - self.delay/2 < pygame.time.get_ticks()):
                self.move_sw_tick = pygame.time.get_ticks()
                if self.move_sw == 0:
                    self.move_x *= -1
                elif self.move_sw == 1:
                    self.move_y *= -1
                
                self.move_sw += 1
                self.move_sw %= 2
       

class BackgroundBox(pygame.sprite.Sprite):
    def __init__(self, pos, size, color = blue, delay = 0, anim_speed = 0):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        
        self.pos = pos
        self.size = size
        self.color = color
        
        self.top_x = self.max_topx = pos[0] - 375
        self.top_y = self.max_topy = pos[1] - 132
        self.bot_x = size[0] + 31
        self.bot_y = size[1] + 58
        
        self.max_botx = size[0] + 416
        self.max_boty = size[1] + 141
        
        self.move_x = 1
        self.move_y = 1
        
        self.move_sw_tick = pygame.time.get_ticks()
        self.move_sw = 0
        
        self.delay = delay
        self.delay_lasttick = pygame.time.get_ticks()
        
        #print (self.top_x, self.top_y, self.bot_x, self.bot_y, self.max_botx, self.max_boty, (self.max_boty - self.top_y), (self.max_botx - self.top_x))
        
        self.boxsize = (50,50)

        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps if anim_speed == 0 else anim_speed
        
        self.render_bg()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.top_x,self.top_y)
    
    def render_bg(self):
        
        for y in range((self.max_boty - self.top_y)//self.boxsize[1]):
            for x in range((self.max_botx - self.top_x)//self.boxsize[0]):
                pygame.draw.rect(self.image, self.color, \
                                 (self.top_x + self.boxsize[0] * x, self.top_y + self.boxsize[1] * y, self.boxsize[0], self.boxsize[1]),\
                                 3)
        
    
    def update(self):
        
        if (pygame.time.get_ticks() > self.delay_lasttick + self.delay):
        
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                
                self.top_x += self.move_x
                self.top_y += self.move_y
                
                self.rect.topleft = (self.top_x,self.top_y)
                
            if (self.move_sw_tick + 3000 - self.delay/2 < pygame.time.get_ticks()):
                self.move_sw_tick = pygame.time.get_ticks()
                if self.move_sw == 0:
                    self.move_x *= -1
                elif self.move_sw == 1:
                    self.move_y *= -1
                
                self.move_sw += 1
                self.move_sw %= 2
                
class BorderBox(pygame.sprite.Sprite):
    def __init__(self, color, pos, size, width, color_tense = 1, bg_color = (1,1,1), alpha = 255):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        self.image.set_alpha(alpha)
        
        self.color = color
        self.pos = pos
        self.size = size
        self.width = width
        self.color_tense = color_tense
        self.bg_color = bg_color
        
        self.cur_color = 0
        
        self.anim_frame = 6
        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.updating = True
        
    def update(self):
        if self.anim_frame == 6:
            self.cur_color += 1
            self.cur_color %= 3
        
        if self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [7*self.color_tense*self.anim_frame*(1 if self.cur_color == 0 else 0) , 7*self.color_tense*self.anim_frame*(1 if self.cur_color == 1 else 0) , 7*self.color_tense*self.anim_frame*(1 if self.cur_color == 2 else 0)], [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
                pygame.draw.rect(self.image, self.color, [0-3, 0-3, self.size[0]+3, self.size[1]+3], self.width+3)
                self.anim_frame -= 1
                
                
        elif self.anim_frame == 0:
            pygame.draw.rect(self.image, self.bg_color, [0, 0, self.size[0], self.size[1]])  
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
            self.updating = False
            
class BorderBox_t(pygame.sprite.Sprite):
    def __init__(self, color, pos, size, width, color_tense = 1):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        self.image.set_alpha(128)
        
        self.color = color
        self.pos = pos
        self.size = size
        self.width = width
        self.color_tense = color_tense
        
        self.cur_color = 0
        
        self.anim_frame = 6
        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.updating = True
        
    def update(self):
        if self.anim_frame == 6:
            self.cur_color += 1
            self.cur_color %= 3
        
        if self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [7*self.color_tense*self.anim_frame*(1 if self.cur_color == 0 else 0) , 7*self.color_tense*self.anim_frame*(1 if self.cur_color == 1 else 0) , 7*self.color_tense*self.anim_frame*(1 if self.cur_color == 2 else 0)], [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
                pygame.draw.rect(self.image, self.color, [0-3, 0-3, self.size[0]+3, self.size[1]+3], self.width+3)
                self.anim_frame -= 1
                
                
        elif self.anim_frame == 0:
            pygame.draw.rect(self.image, black, [0, 0, self.size[0], self.size[1]])  
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
            self.updating = False

class ScoreBox(pygame.sprite.Sprite):
    def __init__(self, color, pos, size, score , max, delay):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        
        self.color = color
        self.pos = pos
        self.size = size
        self.score = score
        self.max = max
        
        self.anim_frame = 6
        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps*3
        
        self.delay = delay
        self.delay_lasttick = pygame.time.get_ticks()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def update(self):
        if (pygame.time.get_ticks() > self.delay_lasttick + self.delay):
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, black, [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, (self.color if True else (0,0,0)), [0, 0, self.size[0]*(self.score/self.max), self.size[1]])
                pygame.draw.rect(self.image, white, [0, 0, self.size[0], self.size[1]], 2)
                self.anim_frame -= 1
            if self.anim_frame < 1:
                self.anim_frame = 6
    
# Letter Box Templates

class LetterBox(pygame.sprite.Sprite):
    def __init__(self, text, color, pos, size, width = 0, delay = 0, f_color = font_color[1], f_typo = font_typo[3], bg_color = black):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        
        self.bgcolor = bg_color
        self.text = text
        self.color = color
        self.pos = pos
        self.size = size
        self.width = width
        self.f_color = f_color
        self.f_typo = f_typo
        
        self.static = False
        
        self.updating = True
        
        self.anim_frame = 6
        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps
        
        self.delay = delay
        self.delay_lasttick = pygame.time.get_ticks()

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def game_display_text(self, text):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.textSurf, self.textRect)
    
    def update(self):
        if (pygame.time.get_ticks() < self.delay_lasttick + self.delay):
            pass
        elif self.static == False:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [42*self.anim_frame,42*self.anim_frame,42*self.anim_frame], [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
                self.game_display_text(self.text)
                self.anim_frame -= 1
                
            if self.anim_frame == 0:
                self.static = True
                
        elif self.static:
            pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
            self.game_display_text(self.text)
            self.updating = False
            
class LetterBox_t(pygame.sprite.Sprite):
    def __init__(self, text, color, pos, size, width = 0, delay = 0, f_color = font_color[1], f_typo = font_typo[3], bg_color = black):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        
        self.bgcolor = bg_color
        self.text = text
        self.color = color
        self.pos = pos
        self.size = size
        self.width = width
        self.f_color = f_color
        self.f_typo = f_typo
        
        self.static = False
        
        self.updating = True
        
        self.anim_frame = 6
        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps
        
        self.delay = delay
        self.delay_lasttick = pygame.time.get_ticks()

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def game_display_text(self, text):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.textSurf, self.textRect)
    
    def update(self):
        if (pygame.time.get_ticks() < self.delay_lasttick + self.delay):
            pass
        elif self.static == False:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.image.fill(black)
                self.anim_frame -= 1
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((6-self.anim_frame)/6*alpha_block)
                pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
                self.game_display_text(self.text)
                
            if self.anim_frame == 0:
                self.static = True
                
        elif self.static:
            self.image.fill(black)
            pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
            self.game_display_text(self.text)
            self.updating = False

class NumPutBox(pygame.sprite.Sprite):
    def __init__(self, text, pos, size, cur_color = 0, delay = 0):
        super().__init__()
        
        self.image = pygame.Surface(size)
        
        self.text = text
        self.pos = pos
        self.size = size

        self.cur_color = cur_color
        
        self.anim_frame = 0
        
        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps
        
        self.delay = delay
        self.delay_lasttick = pygame.time.get_ticks()

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def game_display_text(self, text):
        self.textSurf, self.textRect = textdisplay(text, font_color[1], font_typo[4])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.textSurf, self.textRect)
    
    def update(self):   
        if self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, black, [0, 0, self.size[0], self.size[1]])
                self.game_display_text(self.text)
                self.rect.y -= 3
                self.anim_frame -= 1
                if self.anim_frame == 0:
                    self.kill()

        elif self.anim_frame == 0:
            #pygame.draw.rect(self.image, black, [0, 0, self.size[0], self.size[1]])
            self.game_display_text(self.text)     
            
        if (pygame.time.get_ticks() > self.delay_lasttick + self.delay) and self.anim_frame == 0:
            self.anim_frame = 6 

# Game Sprite Box Template

class InfluBox(pygame.sprite.Sprite):
    def __init__(self, size, bord, width = 5, color_tense = 1):
        super().__init__()
        
        self.image = pygame.Surface([size[0],size[1]])
        self.image.set_colorkey(black)
        self.image.set_alpha(200)
        
        self.color = ((150,0,0),(150,150,0),(150,0,150),(0,150,0),(0,150,150),(0,0,150))
        self.i = 0
        self.size = [size[0],size[1]]
        self.border = pygame.Rect(bord)
        self.xm = self.ym = 1
        self.beep = 0
        self.spd = 6
        self.width = width
        self.color_tense = color_tense
        
        self.cur_color = 0
        
        self.anim_frame = 12
        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps
        
        self.rect = self.image.get_rect()
        self.rect.center = self.border.center
        
        self.updating = True
        
        
        pygame.draw.rect(self.image,self.color[self.i],(0,0,*self.size))
        #print ('y')
    
    def update(self):
        self.image.fill(black)
        pygame.draw.rect(self.image,(int(self.rect.left/800*255),75,int(self.rect.top/600*255),75),(0,0,*self.size))
        if (self.rect.top < self.border.top) or (self.rect.bottom > self.border.bottom):
            #print ((self.rect.top,self.border.top),(self.rect.bottom,self.border.bottom))
            self.ym *= -1
            self.i += 1
            self.i %= len(self.color)
            self.beep = 1
        if (self.rect.left < self.border.left) or (self.rect.right > self.border.right):
            self.xm *= -1
            self.i += 1
            self.i %= len(self.color)
            self.beep = 2
        self.rect.left += self.xm * self.spd
        self.rect.top += self.ym * self.spd    


class BlockBox(pygame.sprite.Sprite):	  #(self, pos, size, width = 0, level = 6)
    def __init__(self, pos, size, width = 0, level = 6, seed = None, colored = all_block, visible = False):
        super().__init__()
        
        self.visible = True
        
        self.image = pygame.Surface(size)
        if trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
                
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = block_color
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = blue
        self.pos = pos
        self.size = size
        self.width = width
        
        self.updating = True
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        
        
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        if self.visible:
            
            if self.num == 1:
                if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                    self.anim_lasttick = pygame.time.get_ticks()
                    self.image.set_alpha((self.anim_frame)/6*alpha_block)
                    pygame.draw.rect(self.image, [0,0,42*self.anim_frame], [0, 0, self.size[0], self.size[1]],self.width)
                    self.anim_frame -= 1
                    
                if self.anim_frame == 0: 
                    self.kill()
            
            elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
                self.image.fill(self.bgcolor)
                pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
                self.game_display_text(str(int(self.num)))
                self.updating = False
                
                
            elif self.pending_input != 0:
                self.anim_start = False
                if (self.num % self.pending_input == 0):
                    self.num /= self.pending_input
                    self.pending_input = 0
                    self.anim_lasttick = pygame.time.get_ticks()
                    self.anim_frame = 6
                    pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
                    pygame.draw.rect(self.image, [0,0,42*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                    self.game_display_text(str(int(self.num)))
                    self.anim_frame -= 1
                    
                else:
                    self.pending_input = 0
                    
            if self.anim_start == True:
                
                if self.anim_frame < 1:
                    self.anim_start = False 
                
                elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                    self.anim_lasttick = pygame.time.get_ticks()
                    pygame.draw.rect(self.image, [0,0,42*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]], self.width)
                    self.game_display_text(str(int(self.num)))
                    self.anim_frame -= 1
                    
                         
            elif self.anim_frame != 0:
                if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                    self.anim_lasttick = pygame.time.get_ticks()
                    pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                    pygame.draw.rect(self.image, [0,0,42*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                    self.game_display_text(str(int(self.num)))
                    self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level):
            self.num *= random.choice(self.seed)

        
    def update(self):
        
        self.draw_box()
    
class SyncBox(pygame.sprite.Sprite):	#(self, pos, size, width = 0, level = 6, sync_len = None, switch = True)
    def __init__(self, pos, size, width = 0, level = 6, sync_len = None, switch = True, seed = None, colored = all_block):
        super().__init__()
        
        self.visible = False
        
        self.image = pygame.Surface(size)
        if trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        self.sync_lasttick = pygame.time.get_ticks()
        if sync_len == None:
            self.sync_len = random.randrange(500,5000)
        else:
            self.sync_len = sync_len
        self.sync_switch = switch
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
                
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = sync_color
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = yellow
        self.pos = pos
        self.size = size
        self.width = width
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
          
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        
        if self.visible:
            if self.sync_switch == False:
                self.anim_start = False
                self.anim_frame = 0
                pygame.draw.rect(self.image, [42*(6-self.anim_frame),42*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]])
                #self.game_display_text(str(int(self.num)))
                  
            elif self.num == 1:
                if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                    self.anim_lasttick = pygame.time.get_ticks()
                    self.image.set_alpha((self.anim_frame)/6*alpha_block)
                    pygame.draw.rect(self.image, [42*self.anim_frame,42*self.anim_frame,0], [0, 0, self.size[0], self.size[1]],self.width)
                    self.anim_frame -= 1
                    
                if self.anim_frame == 0: 
                    self.kill()
            
            elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
                self.image.fill(self.bgcolor)
                pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
                self.game_display_text(str(int(self.num)))
                
                
            elif self.pending_input != 0:
                self.anim_start = False
                if (self.num % self.pending_input == 0):
                    self.num /= self.pending_input
                    self.pending_input = 0
                    self.anim_lasttick = pygame.time.get_ticks()
                    self.anim_frame = 6
                    pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
                    pygame.draw.rect(self.image, [42*(6-self.anim_frame),42*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]],self.width)
                    self.game_display_text(str(int(self.num)))
                    self.anim_frame -= 1
                    
                else:
                    self.pending_input = 0
                    
            elif self.anim_start == True:
                
                if self.anim_frame < 1:
                    self.anim_start = False 
                
                elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                    self.anim_lasttick = pygame.time.get_ticks()
                    pygame.draw.rect(self.image, [42*(6-self.anim_frame),42*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]], self.width)
                    self.game_display_text(str(int(self.num)))
                    self.anim_frame -= 1
                         
            elif self.anim_frame != 0:
                if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                    self.anim_lasttick = pygame.time.get_ticks()
                    pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                    pygame.draw.rect(self.image, [42*(6-self.anim_frame),42*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]],self.width)
                    self.game_display_text(str(int(self.num)))
                    self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level):
            self.num *= random.choice(self.seed)

    def sync_check(self):
        if (pygame.time.get_ticks() > self.sync_lasttick + self.sync_len) and (self.num != 1):
            self.sync_switch ^= True
            self.sync_lasttick = pygame.time.get_ticks()
        elif (self.num == 1):
            self.sync_switch = True
    
    def update(self):
        
        self.sync_check()
        self.draw_box()    

class SubtracBox(pygame.sprite.Sprite):     #(self, pos, size, width = 0, level = 6)
    def __init__(self, pos, size, width = 0, level = 6, seed= None, colored = all_block, visible = False):
        super().__init__()
        
        self.visible = visible
        
        self.image = pygame.Surface(size)
        if trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
        
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = subtrac_color
        
        self.updating = True
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = (int(204/6)*self.anim_frame , int(153/6)*self.anim_frame , 0)
        self.pos = pos
        self.size = size
        self.width = width
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        
        
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        if self.num <= 1:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((self.anim_frame)/6*alpha_block)
                pygame.draw.rect(self.image, [int(155/6)*self.anim_frame , int(155/6)*self.anim_frame , 0], [0, 0, self.size[0], self.size[1]],self.width)
                self.anim_frame -= 1
                
            if self.anim_frame == 0: 
                self.kill()
        
        elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
            self.game_display_text(str(int(self.num-1)))
            self.updating = False
            
        elif self.pending_input != 0:
            self.anim_start = False
            self.num -= self.pending_input
            
            if self.num <= 0:
                self.num = 1
            
            self.pending_input = 0
            self.anim_lasttick = pygame.time.get_ticks()
            self.anim_frame = 6
            pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
            pygame.draw.rect(self.image, [int(155/6)*(6-self.anim_frame) , int(155/6)*(6-self.anim_frame) ,0], [0, 0, self.size[0], self.size[1]],self.width)
            self.game_display_text(str(int(self.num-1)))
            self.anim_frame -= 1
                
        if self.anim_start == True:
            
            if self.anim_frame < 1:
                self.anim_start = False 
            
            elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [int(155/6)*(6-self.anim_frame) , int(155/6)*(6-self.anim_frame) ,0], [0, 0, self.size[0], self.size[1]], self.width)
                self.game_display_text(str(int(self.num-1)))
                self.anim_frame -= 1
                
                     
        elif self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, [int(155/6)*(6-self.anim_frame) , int(155/6)*(6-self.anim_frame) ,0], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num-1)))
                self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(int(level*1.5)):
            self.num += random.choice(self.seed)

        
    def update(self):
        if self.visible:
            self.draw_box()

class MythicBox(pygame.sprite.Sprite):	     #(self, pos, size, width = 0, level = 6)
    def __init__(self, pos, size, width = 0, level = 6, seed = None, colored = all_block, visible= False):
        super().__init__()
        
        self.visible = visible
        
        self.image = pygame.Surface(size)
        if trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
        
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = mythic_color
        
        self.updating = True
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = violet
        self.pos = pos
        self.size = size
        self.width = width
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        
        
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        if self.num == 1:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((self.anim_frame)/6*alpha_block)
                pygame.draw.rect(self.image, [42*self.anim_frame,0,42*self.anim_frame], [0, 0, self.size[0], self.size[1]],self.width)
                self.anim_frame -= 1
                
            if self.anim_frame == 0: 
                self.kill()
        
        elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
            #self.game_display_text(str(int(self.num)))
            self.updating = False
            
        elif self.pending_input != 0:
            self.anim_start = False
            if (self.num % self.pending_input == 0):
                self.num /= self.pending_input
                self.pending_input = 0
                self.anim_lasttick = pygame.time.get_ticks()
                self.anim_frame = 6
                pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
                pygame.draw.rect(self.image, [42*(6-self.anim_frame),0,42*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                #self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
            else:
                self.pending_input = 0
                
        if self.anim_start == True:
            
            if self.anim_frame < 1:
                self.anim_start = False 
            
            elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [42*(6-self.anim_frame),0,42*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]], self.width)
                #self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
                     
        elif self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, [42*(6-self.anim_frame),0,42*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                #self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level*2):
            self.num *= random.choice(self.seed)

        
    def update(self):
        
        if self.visible:
            self.draw_box()

class CracBox(pygame.sprite.Sprite):  #(self, pos, size, width = 0, level = 6, sync_len = None, sync_ctr = None, switch = True)
    def __init__(self, pos, size, width = 0, level = 6, sync_len = None, sync_ctr = None, switch = True, seed = None, max = None, colored = all_block):
        super().__init__()
        
        self.visible = False
        
        self.image = pygame.Surface(size)
        if trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        self.sync_lasttick = pygame.time.get_ticks()
        
        if sync_len == None:
            self.sync_len = random.randrange(3000,10000)
        else:
            self.sync_len = sync_len
            
        self.sync_switch = switch
        
        if sync_ctr == None:
            self.sync_ctr_break = 3
        else:
            self.sync_ctr_break = sync_ctr
            
        if max == None:
            self.max = 2 ** 100
        else:
            self.max = max
        
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = crac_color
            
        self.sync_ctr = 0
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = blue
        self.pos = pos
        self.size = size
        self.width = width
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
          
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        if self.sync_switch == False:
            self.anim_start = False
            self.anim_frame = 0
            
            pygame.draw.rect(self.image, crac_color_2 if all_block == 1 else black, [0, 0, self.size[0], self.size[1]])
            pygame.draw.rect(self.image, [(255/6)*(6-self.anim_frame),0,0], [0, 0, self.size[0], self.size[1]],self.width)
            self.game_display_text(str(int(self.num)))
            if (self.pending_input != 0):
                if self.num < self.max:
                    self.num *= self.pending_input
                self.pending_input = 0
                self.sync_ctr += 1
            if (self.sync_ctr > self.sync_ctr_break):
                self.sync_switch = True
              
        elif self.num == 1:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((self.anim_frame)/6*alpha_block)
                pygame.draw.rect(self.image, [0,0,(255/6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.anim_frame -= 1
                
            if self.anim_frame == 0: 
                self.kill()
        
        elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
            self.game_display_text(str(int(self.num)))
            
            
        elif self.pending_input != 0:
            self.anim_start = False
            if (self.num % self.pending_input == 0):
                self.num /= self.pending_input
                self.pending_input = 0
                self.anim_lasttick = pygame.time.get_ticks()
                self.anim_frame = 6
                pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
                pygame.draw.rect(self.image, [0,0,(255/6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
            else:
                self.pending_input = 0
                
        elif self.anim_start == True:
            
            if self.anim_frame < 1:
                self.anim_start = False 
            
            elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [(255/6)*(6-self.anim_frame),0,0], [0, 0, self.size[0], self.size[1]], self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
                     
        elif self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, [0,0,(255/6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level):
            self.num *= random.choice(self.seed)

    def sync_check(self):
        if (pygame.time.get_ticks() > self.sync_lasttick + self.sync_len) and (self.num != 1):
            self.sync_switch ^= True
            self.sync_lasttick = pygame.time.get_ticks()
        elif (self.num == 1):
            self.sync_switch = True
    
    def update(self):
        
        if self.visible:
            self.sync_check()
            self.draw_box()    

class JacBox(pygame.sprite.Sprite):     #(self, pos, size, width = 0, level = 6, jac_num = None)
    def __init__(self, pos, size, width = 0, level = 6, jac_num = None, seed= None, colored = all_block):
        super().__init__()
        
        self.visible = False
        self.visc = False
        
        self.image = pygame.Surface(size)
        if jac_trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        
        if jac_num == None:
            self.jac_num_ver = 1
            self.jac_num = (2,3,4,5,6,7,8,9)
        else:
            self.jac_num_ver = 2
            if not(isinstance(jac_num, (list,tuple))):
                self.jac_num = (jac_num, jac_num)
            else: self.jac_num = jac_num
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
                
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = jac_color
        
        self.updating = True
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = green
        self.pos = pos
        self.size = size
        self.width = width
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def jactest(self):
        for num in self.jac_num:
            if self.num % num == 0:
                return True
        return False 
        
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        self.visc = True
        if self.num in (2,3,4,5,6,7,8,9) and self.jac_num_ver == 1:
            if (self.pending_input != 0) and (self.num % self.pending_input == 0):
                self.num /= self.pending_input
            self.pending_input = 0
            self.anim_frame = 0
            pygame.draw.rect(self.image, black, [0, 0, self.size[0], self.size[1]])
            self.visc = False
            #pygame.draw.rect(self.image, [0,42*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]],self.width)
            #self.game_display_text(str(int(self.num)))
            self.updating = False
        elif self.jactest() and self.jac_num_ver == 2:
            if (self.pending_input != 0) and (self.num % self.pending_input == 0):
                self.num /= self.pending_input
            self.pending_input = 0
            self.anim_frame = 0
            pygame.draw.rect(self.image, black, [0, 0, self.size[0], self.size[1]])
            #pygame.draw.rect(self.image, [0,42*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]],self.width)
            #self.game_display_text(str(int(self.num)))
            self.updating = False
            self.visc = False
        
        elif self.num == 1:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((self.anim_frame)/6*alpha_block)
                pygame.draw.rect(self.image, [0,42*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]],self.width)
                self.anim_frame += 1
                
            if self.anim_frame >= 5: 
                self.kill()
        
        elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
            self.game_display_text(str(int(self.num)))
            self.updating = False
            
        elif self.pending_input != 0:
            self.anim_start = False
            if (self.num % self.pending_input == 0):
                self.num /= self.pending_input
                self.pending_input = 0
                self.anim_lasttick = pygame.time.get_ticks()
                self.anim_frame = 6
                pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
                pygame.draw.rect(self.image, [0,42*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
            else:
                self.pending_input = 0
                
        if self.anim_start == True:
            
            if self.anim_frame < 1:
                self.anim_start = False 
            
            elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [0,42*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]], self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
                     
        elif self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, [0,42*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level):
            self.num *= random.choice(self.seed)

        
    def update(self):
        
        if self.visible: self.draw_box()
    
class TicBox(pygame.sprite.Sprite):	    #(self, pos, size, width = 0, level = 6, wait_tic = None, add_tic = None, switch = True)
    def __init__(self, pos, size, width = 0, level = 6, wait_tic = None, add_tic = None, switch = True, seed = None, max = None, colored = all_block):
        super().__init__()
        
        self.visible = False
        
        self.image = pygame.Surface(size)
        if trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        self.wait_lasttick = pygame.time.get_ticks()
        self.add_lasttick = pygame.time.get_ticks()
        
        if wait_tic == None:
            self.wait_tic = random.randrange(50,1500)
        else:
            self.wait_tic = wait_tic
            
        if add_tic == None:
            self.add_tic = random.randrange(50,500)
        else:
            self.add_tic = add_tic
            
        if max == None:
            self.max = 10000
        else:
            self.max = max
            
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = tic_color
                
        self.wait_switch = switch
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = (192,192,192)
        self.pos = pos
        self.size = size
        self.width = width
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
          
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        if self.wait_switch == False:
            self.anim_start = False
            self.anim_frame = 0
            pygame.draw.rect(self.image, tic_color_2 if all_block == 1 else black, [0, 0, self.size[0], self.size[1]])
            pygame.draw.rect(self.image, [0,62,62], [0, 0, self.size[0], self.size[1]],self.width)
            self.game_display_text(str(int(self.num)))
              
        elif self.num == 1:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((self.anim_frame)/6*alpha_block)
                pygame.draw.rect(self.image, [32*self.anim_frame,32*self.anim_frame,32*self.anim_frame], [0, 0, self.size[0], self.size[1]],self.width)
                self.anim_frame -= 1
                
            if self.anim_frame == 0: 
                self.kill()
        
        elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
            self.game_display_text(str(int(self.num)))
            
            
        elif self.pending_input != 0:
            self.anim_start = False
            if (self.num % self.pending_input == 0):
                self.num /= self.pending_input
                self.pending_input = 0
                self.anim_lasttick = pygame.time.get_ticks()
                self.anim_frame = 6
                pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
                pygame.draw.rect(self.image, [32*(6-self.anim_frame),32*(6-self.anim_frame),32*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
            else:
                self.pending_input = 0
                
        elif self.anim_start == True:
            
            if self.anim_frame < 1:
                self.anim_start = False 
            
            elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [32*(6-self.anim_frame),32*(6-self.anim_frame),32*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]], self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                     
        elif self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, [32*(6-self.anim_frame),32*(6-self.anim_frame),32*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level):
            self.num *= random.choice(self.seed)

    def sync_check(self):
        if (pygame.time.get_ticks() > self.wait_lasttick + self.wait_tic) and self.wait_switch == True and (self.num != 1):
            self.wait_switch = False
            self.add_lasttick = pygame.time.get_ticks()
            self.wait_lasttick = pygame.time.get_ticks()
            
        if self.pending_input != 0:
            self.wait_switch = True
            self.sync_lasttick = pygame.time.get_ticks()
            
        if self.wait_switch == False and (pygame.time.get_ticks() > self.add_lasttick + self.add_tic):
            if (self.num < self.max):
                self.num *= random.choice(self.seed)
            self.add_lasttick = pygame.time.get_ticks()
            
        elif (self.num == 1):
            self.wait_switch = True
    
    def update(self):
        
        if self.visible:
            self.sync_check()
            self.draw_box()        

class NicBox(pygame.sprite.Sprite):     #(self, pos, size, width = 0, level = 6)
    def __init__(self, pos, size, width = 0, level = 6, seed = None, colored = all_block):
        super().__init__()
        
        self.visible = False
        
        self.image = pygame.Surface(size)
        if trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
        
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = nic_color
        
        self.correct = None
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = [126,149,9]
        self.pos = pos
        self.size = size
        self.width = width
        
        self.updating = True
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        
        
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        if self.num == 1:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((self.anim_frame)/6*alpha_block)
                pygame.draw.rect(self.image, [(126//6)*self.anim_frame,(149//6)*self.anim_frame,(9//6)*self.anim_frame], [0, 0, self.size[0], self.size[1]],self.width)
                self.anim_frame -= 1
                
            if self.anim_frame == 0: 
                self.kill()
        
        elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
            self.game_display_text(str(int(self.num)))
            self.updating = False
            
            
        elif self.pending_input != 0:
            self.anim_start = False
            if (self.num % self.pending_input == 0):
                self.correct = True
                self.num /= self.pending_input
                self.pending_input = 0
                self.anim_lasttick = pygame.time.get_ticks()
                self.anim_frame = 6
                pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
                pygame.draw.rect(self.image, [(126//6)*(6-self.anim_frame),(149//6)*(6-self.anim_frame),(9//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
            else:
                self.correct = False
                self.num *= self.pending_input
                self.pending_input = 0
                self.anim_lasttick = pygame.time.get_ticks()
                self.anim_frame = 6
                pygame.draw.rect(self.image, blip(nic_color_2) if all_block == 1 else black, [0, 0, self.size[0], self.size[1]])
                pygame.draw.rect(self.image, [12*(6-self.anim_frame),0,12*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                self.pending_input = 0
                
        if self.anim_start == True:
            
            if self.anim_frame < 1:
                self.anim_start = False 
            
            elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [(126//6)*(6-self.anim_frame),(149//6)*(6-self.anim_frame),(9//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]], self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
                     
        elif self.anim_frame != 0:
            if self.correct:
                if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                    self.anim_lasttick = pygame.time.get_ticks()
                    pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                    pygame.draw.rect(self.image, [(126//6)*(6-self.anim_frame),(149//6)*(6-self.anim_frame),(9//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                    self.game_display_text(str(int(self.num)))
                    self.anim_frame -= 1
            if self.correct == False:
                if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                    self.anim_lasttick = pygame.time.get_ticks()
                    pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                    pygame.draw.rect(self.image, [12*(6-self.anim_frame),0,12*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                    self.game_display_text(str(int(self.num)))
                    self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level):
            self.num *= random.choice(self.seed)

        
    def update(self):
        
        if self.visible: self.draw_box()

class SniqBox(pygame.sprite.Sprite):        #(self, pos, size, width = 0, level = 6, wait_tic = None, mov_tic = None, switch = True)
    def __init__(self, pos, size, width = 0, level = 6, move_tic = None, switch = None, seed = None, colored = all_block):
        
        self.visible = False
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        if trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        #self.add_lasttick = pygame.time.get_ticks()
            
        if move_tic == None:
            self.move_tic = random.randint(1,3)
        else:
            self.move_tic = move_tic
        
        if switch == None:  
            self.move_x = random.choice((-1,1,0))
            self.move_y = random.choice((-1,1,0))
        else:
            self.move_x = random.choice((-1,1,0))
            self.move_y = random.choice((-1,1,0))
        
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = sniq_color
            
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = (93,240,255)
        self.pos = pos
        self.size = size
        self.width = width
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
          
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        if self.num == 1:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((self.anim_frame)/6*alpha_block)
                pygame.draw.rect(self.image, [(93//6)*self.anim_frame,(240//6)*self.anim_frame,(255//6)*self.anim_frame], [0, 0, self.size[0], self.size[1]],self.width)
                self.anim_frame -= 1
                
            if self.anim_frame == 0: 
                self.kill()
        
        elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
            self.game_display_text(str(int(self.num)))
            
            
        elif self.pending_input != 0:
            self.anim_start = False
            if (self.num % self.pending_input == 0):
                self.num /= self.pending_input
                self.pending_input = 0
                self.anim_lasttick = pygame.time.get_ticks()
                self.anim_frame = 6
                pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
                pygame.draw.rect(self.image, [(93//6)*(6-self.anim_frame),(240//6)*(6-self.anim_frame),(255//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
            else:
                self.pending_input = 0
                
        elif self.anim_start == True:
            
            if self.anim_frame < 1:
                self.anim_start = False 
            
            elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [(93//6)*(6-self.anim_frame),(240//6)*(6-self.anim_frame),(255//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]], self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                     
        elif self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, [(93//6)*(6-self.anim_frame),(240//6)*(6-self.anim_frame),(255//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level):
            self.num *= random.choice(self.seed)

    def sync_check(self):
        if (self.rect.x + self.size[0] > settings['screen_w']) or (self.rect.x < 0):
            self.move_x *= -1
        if (self.rect.y + self.size[1] > settings['screen_h']) or (self.rect.y < 0):
            self.move_y *= -1
        self.rect.x += self.move_x * self.move_tic
        self.rect.y += self.move_y * self.move_tic
    
    def update(self):
        
        if self.visible:
            self.sync_check()
            self.draw_box()        

class ShuqBox(pygame.sprite.Sprite):      #(self, pos, size, width = 0, level = 6)
    def __init__(self, pos, size, width = 0, level = 6, seed = None, colored = all_block):
        super().__init__()
        
        self.visible = False
        
        self.image = pygame.Surface(size)
        if trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        self.level = level
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
                
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = shuq_color
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = (192,48,114)
        self.pos = pos
        self.size = size
        self.width = width
        
        self.updating = True
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        
        
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        if self.num == 1:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((self.anim_frame)/6*alpha_block)
                pygame.draw.rect(self.image, ( (190//6)*self.anim_frame, (48//6)*self.anim_frame, (110//6)*self.anim_frame ), [0, 0, self.size[0], self.size[1]],self.width)
                self.anim_frame -= 1
                
            if self.anim_frame == 0: 
                self.kill()
        
        elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
            self.game_display_text(str(int(self.num)))
            self.updating = False
            
            
        elif self.pending_input != 0:
            self.anim_start = False
            if (self.num % self.pending_input == 0):
                self.num /= self.pending_input
                if self.num != 1:
                    self.level -= 1
                    self.generate_num(self.level)
                
                self.pending_input = 0
                self.anim_lasttick = pygame.time.get_ticks()
                self.anim_frame = 6
                pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
                pygame.draw.rect(self.image, ((192//6)*(6-self.anim_frame),(48//6)*(6-self.anim_frame),(114//6)*(6-self.anim_frame)), [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
            else:
                if self.num != 1:
                    self.generate_num(self.level)
                self.pending_input = 0
                
        if self.anim_start == True:
            
            if self.anim_frame < 1:
                self.anim_start = False 
            
            elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, ((192//6)*(6-self.anim_frame),(48//6)*(6-self.anim_frame),(114//6)*(6-self.anim_frame)), [0, 0, self.size[0], self.size[1]], self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
                     
        elif self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, ((192//6)*(6-self.anim_frame),(48//6)*(6-self.anim_frame),(114//6)*(6-self.anim_frame)), [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level):
            self.num *= random.choice(self.seed)

        
    def update(self):
        
        if self.visible:
            self.draw_box()

class MockBox(pygame.sprite.Sprite):  #(self, pos, size, width = 0, level = 6, sync_len = None, switch = 0 , seed = None, max = None)
    def __init__(self, pos, size, width = 0, level = 6, sync_len = None, switch = 0, seed = None, max = None, mode = 0, colored = all_block):
        super().__init__()
        
        self.visible = False
        
        self.image = pygame.Surface(size)
        if trans: self.image.set_colorkey(black)
        if alpha_low: self.image.set_alpha(alpha_block)
        
        self.sync_lasttick = pygame.time.get_ticks()
        
        if sync_len == None:
            self.sync_len = random.randrange(3000,10000)
        else:
            self.sync_len = sync_len
            
        self.sync_switch = switch
        
        if mode == 0:
            self.mode = 0
        elif mode == 1:
            self.mode = 1
        else:
            self.mode = 0
            
        if max == None:
            self.max = 2 ** 100
        else:
            self.max = max
        
        if colored == 0:
            self.bgcolor = black
        else:
            self.bgcolor = mock_color
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = blue
        self.pos = pos
        self.size = size
        self.width = width
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
          
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        if self.sync_switch == 1:
            self.anim_start = False
            if (self.pending_input != 0):
                self.anim_frame = 6
                if self.num < self.max:
                    self.num *= self.pending_input
                self.pending_input = 0
            if self.anim_frame > 0:
                self.anim_frame -= 1
            else:
                self.anim_frame = 0
            pygame.draw.rect(self.image, mock_color_2 if all_block == 1 else black, [0, 0, self.size[0], self.size[1]])
            pygame.draw.rect(self.image, [(255//6)*(6-self.anim_frame),0,0], [0, 0, self.size[0], self.size[1]],self.width)
            self.game_display_text(str(int(self.num)))
                
        elif self.sync_switch == 2 and self.num != 1:
            self.anim_start = False
            if (self.pending_input != 0):
                self.anim_frame = 6
                self.num -= self.pending_input
                if self.num <= 0:
                    self.num = 1
                self.pending_input = 0
            if self.anim_frame > 0:
                self.anim_frame -= 1
            else:
                self.anim_frame = 0
            pygame.draw.rect(self.image, mock_color_3 if all_block == 1 else black, [0, 0, self.size[0], self.size[1]])
            pygame.draw.rect(self.image, [(204//6)*(6-self.anim_frame),(153//6)*(6-self.anim_frame),0], [0, 0, self.size[0], self.size[1]],self.width)
            self.game_display_text(str(int(self.num)))
                
        elif self.sync_switch == 3 and self.num != 1:
            self.anim_start = False
            if (self.pending_input != 0):
                self.anim_frame = 6
                self.num += self.pending_input
                self.pending_input = 0
            if self.anim_frame > 0:
                self.anim_frame -= 1
            else:
                self.anim_frame = 0
            pygame.draw.rect(self.image, mock_color_3 if all_block == 1 else black, [0, 0, self.size[0], self.size[1]])
            pygame.draw.rect(self.image, [(150//6)*(6-self.anim_frame),(150//6)*(6-self.anim_frame),(150//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
            self.game_display_text(str(int(self.num)))
            
        elif self.sync_switch == 4 and self.num != 1:
            self.anim_start = False
            self.pending_input = 0
            pygame.draw.rect(self.image, black, [0, 0, self.size[0], self.size[1]])
            pygame.draw.rect(self.image, (0,0,0), [0, 0, self.size[0], self.size[1]],self.width)
            self.game_display_text(str(int(self.num)))
              
        elif self.num == 1:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((self.anim_frame)/6*alpha_block)
                pygame.draw.rect(self.image, [0,0,(255//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.anim_frame -= 1
                
            if self.anim_frame == 0: 
                self.kill()
        
        elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
            self.image.fill(self.bgcolor)
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)  
            self.game_display_text(str(int(self.num)))
            
            
        elif self.pending_input != 0:
            self.anim_start = False
            if (self.num % self.pending_input == 0):
                self.num /= self.pending_input
                self.pending_input = 0
                self.anim_lasttick = pygame.time.get_ticks()
                self.anim_frame = 6
                pygame.draw.rect(self.image, blip(self.bgcolor), [0, 0, self.size[0], self.size[1]])
                pygame.draw.rect(self.image, [0,0,(255//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
            else:
                self.pending_input = 0
                
        elif self.anim_start == True:
            
            if self.anim_frame < 1:
                self.anim_start = False 
            
            elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, [0,0,(255//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]], self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
                     
        elif self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, [0,0,(255//6)*(6-self.anim_frame)], [0, 0, self.size[0], self.size[1]],self.width)
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level):
            self.num *= random.choice(self.seed)

    def sync_check(self):
        if (pygame.time.get_ticks() > self.sync_lasttick + self.sync_len) and (self.num != 1):
            if self.mode == 0:
                self.sync_switch += 1
                self.sync_switch %= 4
            elif self.mode == 1:
                self.sync_switch = random.randint(0,5)
                self.sync_switch %= 4
            self.sync_lasttick = pygame.time.get_ticks()
            self.anim_frame = 0
        elif (self.num == 1):
            self.sync_switch = 0
    
    def update(self):
        
        if self.visible:
            self.sync_check()
            self.draw_box()    



class DrawBox(pygame.sprite.Sprite):
    def __init__(self, pos, size, width = 0, level = 6, seed = None):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        
        self.pending_input = 0
        self.anim_frame = 6
        self.anim_speed = fps
        self.anim_start = True
        
        if seed == None:
            self.seed = (2,3,4,5,6,7,8,9)
        else:
            if not(isinstance(seed, (list,tuple))):
                self.seed = (seed, seed)
            else:
                self.seed = seed
        
        self.anim_lasttick = pygame.time.get_ticks()
        
        self.color = blue
        self.pos = pos
        self.size = size
        self.width = width
        
        self.updating = True
        
        self.generate_num(level)
        self.draw_box()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        
        
    def game_display_text(self, text):
        self.text, self.textRect = textdisplay(text, font_color[1], font_typo[2])
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.text, self.textRect)
      
    def draw_box(self):
        if self.num == 1:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha((self.anim_frame)/6*alpha_block)
                self.image = pygame.transform.scale(player_anim['blockA'][self.anim_frame], (self.size[0],self.size[1])) 
                self.anim_frame -= 1
                
            if self.anim_frame == 0: 
                self.kill()
        
        elif self.pending_input == 0 and self.anim_frame == 0 and self.anim_start == False:
            self.image = pygame.transform.scale(player_anim['blockA'][self.anim_frame], (self.size[0],self.size[1])) 
            self.game_display_text(str(int(self.num)))
            self.updating = False
            
            
        elif self.pending_input != 0:
            self.anim_start = False
            if (self.num % self.pending_input == 0):
                self.num /= self.pending_input
                self.pending_input = 0
                self.anim_lasttick = pygame.time.get_ticks()
                self.anim_frame = 6
                self.image = pygame.transform.scale(player_anim['blockA'][self.anim_frame], (self.size[0],self.size[1])) 
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
            else:
                self.pending_input = 0
                
        if self.anim_start == True:
            
            if self.anim_frame < 1:
                self.anim_start = False 
            
            elif (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image = pygame.transform.scale(player_anim['blockA'][self.anim_frame], (self.size[0],self.size[1])) 
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                
                     
        elif self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image = pygame.transform.scale(player_anim['blockA'][self.anim_frame], (self.size[0],self.size[1])) 
                self.game_display_text(str(int(self.num)))
                self.anim_frame -= 1
                            
      
    def generate_num(self,level):
        self.num = 1
        if level < 0: level = 1
        for i in range(level):
            self.num *= random.choice(self.seed)

        
    def update(self):
        
        self.draw_box()
    

   
#####