import pygame
import math
from settings import TILE_SIZE, WALK_SPEED, SPRINT_SPEED, SPRINT_COOLDOWN
from game.collision import is_blocked

class Player:
    def __init__(self, pos, textures, game_map):
        self.pos = pos
        self.textures = textures
        self.game_map = game_map
        self.image = textures['player_default']
        
        # Jump properties
        self.jump_height = 0
        self.jumping = False
        self.jump_time = 0
        self.max_jump_height = 30
        
        # Sprint properties
        self.sprinting = False
        self.sprint_energy = 100.0
        self.sprint_cooldown = 0.0
        self.energy_regen_rate = 15.0
        self.energy_use_rate = 20.0
        self.key_press = False
        
        # Collision rect
        self.rect = pygame.Rect(self.pos.x * TILE_SIZE, self.pos.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        
    def update(self, dt, keys, map_data):
        # Reset player position if R is pressed
        if keys[pygame.K_r]:
            self.pos = self.game_map.find_spawn_location()
            self.jumping = False
            self.jump_height = 0
            return
    
        move_dir = pygame.Vector2(0, 0)
        new_image = self.textures['player_default']
        
        # Handle sprint energy and cooldown
        if self.sprint_cooldown > 0:
            self.sprint_cooldown -= dt
            self.sprinting = False
        elif self.sprint_energy < 100.0 and not self.sprinting:
            self.sprint_energy += self.energy_regen_rate * dt
            if self.sprint_energy > 100.0:
                self.sprint_energy = 100.0
        
        # Determine sprinting state and speed
        movement_speed = WALK_SPEED
        if self.key_press and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            if self.sprint_energy > 0 and self.sprint_cooldown <= 0:
                self.sprinting = True
                movement_speed = SPRINT_SPEED
                self.sprint_energy -= self.energy_use_rate * dt
                if self.sprint_energy <= 0:
                    self.sprint_energy = 0
                    self.sprinting = False
                    self.sprint_cooldown = SPRINT_COOLDOWN
        else:
            self.sprinting = False
            
        # Get key input
        self.key_press = False
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_dir.y -= 1
            new_image = self.textures['player_up']
            self.key_press = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_dir.y += 1
            new_image = self.textures['player_down']
            self.key_press = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_dir.x -= 1
            new_image = self.textures['player_left']
            self.key_press = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_dir.x += 1
            new_image = self.textures['player_right']
            self.key_press = True
            
        # Handle jumping
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.jump_time = 0
            self.key_press = True
            
        if self.jumping:
            self.jump_time += dt
            self.jump_height = int(self.max_jump_height * math.sin(self.jump_time * math.pi))
            new_image = self.textures['player_jump']
            
            if self.jump_time >= 1.0:
                self.jumping = False
                self.jump_height = 0
        
        # Movement with collision detection
        if move_dir.length() > 0:
            move_dir = move_dir.normalize()
            
            # Try to move in x and y directions separately to allow sliding along obstacles
            target_x = self.pos + pygame.Vector2(move_dir.x * dt * movement_speed, 0)
            if not is_blocked(map_data, target_x.x, target_x.y):
                self.pos.x = target_x.x
                
            target_y = self.pos + pygame.Vector2(0, move_dir.y * dt * movement_speed)
            if not is_blocked(map_data, target_y.x, target_y.y):
                self.pos.y = target_y.y
                
            self.image = new_image
        
        # Update collision rect
        self.rect.x = self.pos.x * TILE_SIZE
        self.rect.y = self.pos.y * TILE_SIZE
            
    def draw(self, screen):
        screen_x = screen.get_width() / 2 - self.image.get_width() / 2
        screen_y = screen.get_height() / 2 - self.image.get_height() / 2 - self.jump_height
        screen.blit(self.image, (screen_x, screen_y))
    
    def get_current_block(self):
        """Get information about the block the player is currently on"""
        # Get the block coordinates the player is currently on
        block_x = int(self.pos.x)
        block_y = int(self.pos.y)
        
        # Check if the coordinates are within the map boundaries
        if 0 <= block_y < len(self.game_map.data) and 0 <= block_x < len(self.game_map.data[0]):
            tile_id = self.game_map.data[block_y][block_x]
            tile_name = self.game_map.get_tile_name(tile_id)
            
            return {
                "block_x": block_x,
                "block_y": block_y,
                "tile_name": tile_name
            }
        return None