import pygame
import random
import math
from settings import TILE_SIZE
from game.collision import is_blocked

class NPC:
    def __init__(self, x, y, textures):
        self.pos = pygame.Vector2(x, y)
        self.jump_timer = 0
        self.jump_height = 0
        self.max_jump_height = 20
        self.jumping = False
        self.facing_right = True
        
        # Textures
        self.texture_left = textures['npc_left']
        self.texture_right = textures['npc_right']
        
        # Collision rect
        self.rect = pygame.Rect(self.pos.x * TILE_SIZE, self.pos.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        
    def update(self, dt, player, map_data):
        # Random jumping - less frequent for better performance
        if not self.jumping and random.random() < 0.01:
            self.jumping = True
            self.jump_timer = 0
            
        if self.jumping:
            self.jump_timer += dt
            self.jump_height = int(self.max_jump_height * math.sin(self.jump_timer * math.pi))
            if self.jump_timer >= 1.0:
                self.jumping = False
                self.jump_height = 0
        
        # Move toward player (less frequently for performance)
        direction = pygame.Vector2(player.pos.x - self.pos.x, player.pos.y - self.pos.y)
        if direction.length() > 0:
            direction = direction.normalize()
            
            # Update facing direction based on movement
            if direction.x > 0:
                self.facing_right = True
            elif direction.x < 0:
                self.facing_right = False
                
            # Create a potential new position
            new_pos = self.pos + direction * dt * 1.5  # Slower than player
            
            # Only move if not blocked
            if not is_blocked(map_data, new_pos.x, new_pos.y):
                self.pos = new_pos
        
        # Update rect position
        self.rect.x = self.pos.x * TILE_SIZE
        self.rect.y = self.pos.y * TILE_SIZE
            
    def draw(self, screen, camera_offset):
        screen_x = self.pos.x * TILE_SIZE - camera_offset.x
        screen_y = self.pos.y * TILE_SIZE - camera_offset.y - self.jump_height
        
        # Use the correct texture based on facing direction
        texture = self.texture_right if self.facing_right else self.texture_left
        screen.blit(texture, (screen_x, screen_y))

def create_npcs(map_data, count=5, textures=None):
    """Create NPCs at random safe locations on the map"""
    npcs_list = []
    safe_tiles = []
    
    # Pre-compute safe tiles for NPCs once
    for y in range(1, len(map_data) - 1):
        for x in range(1, len(map_data[0]) - 1):
            from settings import COLLIDABLE_TILES
            if map_data[y][x] not in COLLIDABLE_TILES and map_data[y][x] != 0:  # Not collidable and not a spawn point
                safe_tiles.append((x, y))
    
    # Randomly place NPCs on safe tiles
    while len(npcs_list) < count and safe_tiles:
        if not safe_tiles:
            break
            
        idx = random.randint(0, len(safe_tiles) - 1)
        x, y = safe_tiles[idx]
        npcs_list.append(NPC(x, y, textures))
        safe_tiles.pop(idx)  # Remove used position
    
    return npcs_list