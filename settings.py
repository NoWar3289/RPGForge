import pygame

# Game constants
TILE_SIZE = 64
WALK_SPEED = 10
SPRINT_SPEED = 25
SPRINT_COOLDOWN = 3.0

# Map dimensions (will be updated when map is loaded)
MAP_WIDTH = 0
MAP_HEIGHT = 0

# Global game state
POINTS = 0
REQUIRED_POINTS = 5

# Sound effects
SOUND_ENABLED = True
MUSIC_VOLUME = 0.3
SFX_VOLUME = 0.5

# Initialize pygame and create basic objects
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Anna Hustle")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)