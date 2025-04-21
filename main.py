import pygame
import settings
from utils.texture_loader import load_textures
from game.map import Map
from game.camera import Camera
from game.ui import draw_ui, draw_debug_info
from game.collision import process_npc_collisions
from entities.player import Player
from entities.npc import create_npcs, NPC

def main():
    # Initialize game
    running = True
    show_ui = False
    dt = 0
    
    # Load textures
    textures = load_textures()
    
    # Load map
    game_map = Map("./maps/map.txt")
    
    # Create player at spawn location
    player_pos = game_map.find_spawn_location()
    player = Player(player_pos, textures, game_map)
    
    # Create camera
    camera = Camera()
    
    # Create initial NPCs
    npcs = create_npcs(game_map.data, 5, textures)
    
    # Game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    show_ui = not show_ui
                if event.key == pygame.K_ESCAPE:
                    running = False
    
        settings.screen.fill("#625465")
        keys = pygame.key.get_pressed()
    
        # Update player
        player.update(dt, keys, game_map.data)
        
        # Update camera
        camera.update(player.pos)
        
        # Only update NPCs that are close to the player for performance
        for npc in npcs:
            # Calculate distance to player
            dx = abs(npc.pos.x - player.pos.x)
            dy = abs(npc.pos.y - player.pos.y)
            if dx < 20 and dy < 20:  # Only update NPCs within range
                npc.update(dt, player, game_map.data)
    
        # Process collisions
        process_npc_collisions(player, npcs)
    
        # Respawn NPCs if needed
        if len(npcs) < 5:
            npcs.extend(create_npcs(game_map.data, 5 - len(npcs), textures))
    
        # Draw world
        game_map.draw(settings.screen, textures, camera.position)
        
        # Draw NPCs (only those on screen)
        screen_width, screen_height = settings.screen.get_width(), settings.screen.get_height()
        for npc in npcs:
            screen_x = npc.pos.x * settings.TILE_SIZE - camera.position.x
            screen_y = npc.pos.y * settings.TILE_SIZE - camera.position.y
            
            # Only draw if within visible screen area (with buffer)
            if (-settings.TILE_SIZE <= screen_x <= screen_width and 
                -settings.TILE_SIZE <= screen_y <= screen_height):
                npc.draw(settings.screen, camera.position)
    
        # Draw player (always in center of screen)
        player.draw(settings.screen)
        
        # Draw UI
        draw_ui(settings.screen, player)
        draw_debug_info(settings.screen, player, show_ui, npcs)
    
        pygame.display.flip()
        dt = min(settings.clock.tick(60) / 1000, 0.1)  # Cap dt to prevent physics issues
    
    pygame.quit()

if __name__ == "__main__":
    main()