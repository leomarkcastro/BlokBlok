import pygame
import os

pygame.mixer.init()

#Import music function

game_folder = os.path.dirname(__file__)   

MUSIC_ENDED = pygame.USEREVENT
pygame.mixer.music.set_endevent(MUSIC_ENDED)

#Sound and Music Switches

play_sound = True
play_music = True


# Music

music_folder = os.path.join(game_folder, 'music')   # 'img' refers to the folder in the current game dir
bg_folder = os.path.join(music_folder, 'bg')
beep_folder = os.path.join(music_folder, 'Beep')
lounge_folder = os.path.join(music_folder, 'lounge')


music_array = {
    'main_menu': os.path.join(bg_folder, "Gymnopédie No.1 - Erik Satie 8bit Jazz Version.mp3"),
    'main_menu_2': os.path.join(bg_folder, "main_menu_2.mp3"),
    'endless': os.path.join(bg_folder, "endless.mp3"),
    'select_level': os.path.join(bg_folder, "select_level.mp3"),
    'get_ready': os.path.join(bg_folder, "get_ready_2.mp3"),
    'win': os.path.join(bg_folder, "win.mp3"),
    'lose': os.path.join(bg_folder, "game_over.mp3"),
    'groove': os.path.join(bg_folder, "groove.mp3"),
    'tutorial': os.path.join(bg_folder, "tutorial.mp3"),
    
    'club_music': os.path.join(bg_folder, "club_music.mp3"),
    'club_boss': os.path.join(bg_folder, "club_boss.mp3"),
    
    'under_music': os.path.join(bg_folder, "ug_music.mp3"),
    'under_boss': os.path.join(bg_folder, "under_boss.mp3"),
    
    'crib_music': os.path.join(bg_folder, "elite_music_2.mp3"),
    'crib_black': os.path.join(bg_folder, "elite_blackout.mp3"),
    'crib_boss': os.path.join(bg_folder, "elite_boss.mp3"),
}

def load_music(path):
    songs = []
    if isinstance(path, (list,tuple)):
        for each in path:
            for filename in os.listdir(each):
                if filename.endswith('.mp3'):
                    songs.append(os.path.join(path, filename))
    else:
        for filename in os.listdir(path):
            if filename.endswith('.mp3'):
                songs.append(os.path.join(path, filename))
    return songs

lounge_array = load_music(lounge_folder)


beep_array = {
    'beep04' : pygame.mixer.Sound(os.path.join(beep_folder, "Pickup_coin4.wav")) ,#Number press
    'beep08' : pygame.mixer.Sound(os.path.join(beep_folder, "Pickup_coin8.wav")) ,#Number press
    'beep18' : pygame.mixer.Sound(os.path.join(beep_folder, "Pickup_coin18.wav")) ,#Menu Select
    'beep20': pygame.mixer.Sound(os.path.join(beep_folder, "Pickup_coin20.wav")) ,#Dialogue
    
    'pow02' : pygame.mixer.Sound(os.path.join(beep_folder, "Powerup2.wav")) ,#Quit
    'pow05' : pygame.mixer.Sound(os.path.join(beep_folder, "Powerup5.wav")) ,#Destroyed
    'pow11' : pygame.mixer.Sound(os.path.join(beep_folder, "Powerup11.wav")) ,#Pause
    'pow18' : pygame.mixer.Sound(os.path.join(beep_folder, "Powerup18.wav")) ,#Win
    
    'blip02': pygame.mixer.Sound(os.path.join(beep_folder, "Blip_Select2.wav")) ,#Wall hit
    'blip06': pygame.mixer.Sound(os.path.join(beep_folder, "Blip_Select6.wav")) ,#Wall hit
    'blip19': pygame.mixer.Sound(os.path.join(beep_folder, "Blip_Select19.wav")) ,#Timer less than 10

    'pew': pygame.mixer.Sound(os.path.join(beep_folder, "pew.wav")) ,#Pew pew
    'ahoo': pygame.mixer.Sound(os.path.join(beep_folder, "ahoo.wav")) ,#Pew pew

    }




#Pygame Music Functions


def playmusic(music,repeat = 0,start_at = 0.0): 
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(repeat,start_at)
    
def stopmusic():
    pygame.mixer.music.stop()