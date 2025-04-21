import pygame

# Game constants
TILE_SIZE = 64
WALK_SPEED = 10
SPRINT_SPEED = 25
SPRINT_COOLDOWN = 3.0

# Map dimensions (will be updated when map is loaded)
MAP_WIDTH = 0
MAP_HEIGHT = 0

# Collidable tiles
# COLLIDABLE_TILES = [3, 4, 10]  # Water, trees, and bedrock
COLLIDABLE_TILES = [9, 4, 10]  # Water, trees, and bedrock

# Global game state
points = 0

# Initialize pygame and create basic objects
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Anna Hustle")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)