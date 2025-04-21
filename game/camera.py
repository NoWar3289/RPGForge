import pygame
from settings import TILE_SIZE

class Camera:
    def __init__(self):
        self.position = pygame.Vector2(0, 0)
    
    def update(self, target_pos):
        """Update camera position to follow target"""
        self.position.x = target_pos.x * TILE_SIZE - pygame.display.get_surface().get_width() / 2
        self.position.y = target_pos.y * TILE_SIZE - pygame.display.get_surface().get_height() / 2