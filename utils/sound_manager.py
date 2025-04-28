import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Sound cache to avoid loading the same sound multiple times
sound_cache = {}

def load_sound(path, volume=0.5):
    """Load and cache a sound for efficient reuse"""
    if path not in sound_cache:
        try:
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(volume)
                sound_cache[path] = sound
            else:
                print(f"Sound file not found: {path}")
                return None
        except pygame.error as e:
            print(f"Error loading sound {path}: {e}")
            return None
    return sound_cache[path]

def play_sound(sound_name, volume=None):
    """Play a sound by name"""
    sound = load_sound(f"./sounds/{sound_name}.mp3", volume or 0.5)
    if sound:
        sound.play()

def play_bgm(music_name, volume=0.3, loops=-1):
    """Play background music, loops by default"""
    music_path = f"./sounds/music/{music_name}.mp3"
    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
        except pygame.error as e:
            print(f"Error playing music {music_path}: {e}")
    else:
        print(f"Music file not found: {music_path}")

def stop_bgm():
    """Stop the currently playing background music"""
    pygame.mixer.music.stop()

def set_bgm_volume(volume):
    """Set the volume of the background music (0.0 to 1.0)"""
    pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))


# Sound effect categories for easier management
class GameSounds:
    # Player sounds
    PLAYER_JUMP = "player_jump"
    PLAYER_WALK = "player_walk" 
    PLAYER_SPRINT = "player_sprint"
    PLAYER_TELEPORT = "player_teleport"
    
    # NPC sounds
    NPC_HIT = "npc_hit"
    NPC_JUMP = "npc_jump"
    
    # Game sounds
    POINT_COLLECT = "point_collect"
    LEVEL_COMPLETE = "level_complete"
    GAME_START = "game_start"
    
    # Music tracks
    MAIN_THEME = "main_theme"
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"