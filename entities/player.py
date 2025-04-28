import pygame
import math
import settings
from settings import TILE_SIZE, WALK_SPEED, SPRINT_SPEED, SPRINT_COOLDOWN, POINTS, REQUIRED_POINTS, screen
from game.collision import is_blocked
from utils.sound_manager import play_sound, GameSounds
import random

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

        # teleport
        self.teleport_countdown = 0
        self.teleporting = False
        self.teleport_direction = None


        
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

                # Add sound with slight delay for better experience
                if random.random() < 0.2:  # Only play sprint sound occasionally
                    play_sound(GameSounds.PLAYER_SPRINT, settings.SFX_VOLUME * 0.7)

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
            play_sound(GameSounds.PLAYER_JUMP, settings.SFX_VOLUME)
            
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

            # Add footstep sounds with timing based on speed
            self.footstep_timer = getattr(self, 'footstep_timer', 0) + dt
            step_interval = 0.4 if not self.sprinting else 0.2
            if self.footstep_timer >= step_interval:
                play_sound(GameSounds.PLAYER_WALK, settings.SFX_VOLUME * 0.4)
                self.footstep_timer = 0
        
        # Update collision rect
        self.rect.x = self.pos.x * TILE_SIZE
        self.rect.y = self.pos.y * TILE_SIZE

        # Add this to your Player.update method, just before the return statement:
        # Handle teleport countdown
       # Handle teleport countdown
        if self.teleporting:
            # print(f"Teleporting countdown: {self.teleport_countdown:.2f}s to {self.teleport_direction}")
            self.teleport_countdown -= dt
            if self.teleport_countdown <= 0:
                direction = self.teleport_direction
                print(f"Teleport complete! Direction: {direction}")
                self.teleporting = False
                self.teleport_countdown = 0
                self.teleport_direction = None
                return direction
        
        return None  # Make sure to return None if not teleporting
            
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
    
    # In player.py, update the check_teleportation method
    def check_teleportation(self, map_data):
        """Check if player is on a teleport tile and has enough points"""
        from settings import POINTS
        
        # If already teleporting, don't start another countdown
        if self.teleporting:
            return
                
        block_x = int(self.pos.x)
        block_y = int(self.pos.y)
        
        # Calculate required points based on current map
        map_number = self.game_map.map_number
        required_points = (map_number + 1) * 5  # 5 points for map 0, 10 for map 1, etc.
        
        # Check if coordinates are within map boundaries
        if 0 <= block_y < len(map_data) and 0 <= block_x < len(map_data[0]):
            tile_id = map_data[block_y][block_x]
            
            if tile_id == 11 and POINTS >= required_points:  # Next map teleport
                self.teleporting = True
                self.teleport_countdown = 0.9  # Reduced from 1.0 to 0.5 seconds
                self.teleport_direction = "next"
                play_sound(GameSounds.PLAYER_TELEPORT, settings.SFX_VOLUME)
            elif tile_id == 12:  # Previous map teleport
                self.teleporting = True
                self.teleport_countdown = 0.9  # Reduced from 1.0 to 0.5 seconds
                self.teleport_direction = "previous"
                play_sound(GameSounds.PLAYER_TELEPORT, settings.SFX_VOLUME)