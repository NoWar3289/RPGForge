import pygame
import settings

def draw_ui(screen, player):
    """Draw the user interface elements"""
    # Draw sprint bar
    bar_width = 200
    bar_height = 20
    bar_x = 15
    bar_y = screen.get_height() - bar_height - 15
    
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    
    energy_width = int((player.sprint_energy / 100.0) * bar_width)
    
    if player.sprint_cooldown > 0:
        energy_color = (255, 0, 0)
    elif player.sprinting:
        energy_color = (255, 255, 0)
    else:
        energy_color = (0, 255, 0)
        
    pygame.draw.rect(screen, energy_color, (bar_x, bar_y, energy_width, bar_height))
    pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
    
    label = settings.font.render("Sprint Energy: ", True, (255, 255, 255))
    screen.blit(label, (bar_x, bar_y - 25))
    
    if player.sprint_cooldown > 0:
        cooldown_text = settings.font.render(f"Cooldown: {player.sprint_cooldown:.1f}s", True, (255, 200, 200))
        screen.blit(cooldown_text, (bar_x + bar_width + 10, bar_y))
    
    # Draw points counter
    points_text = settings.font.render(f"Points: {settings.points}", True, (255, 255, 255))
    screen.blit(points_text, (15, bar_y - 50))

def draw_debug_info(screen, player, show_ui, npcs):
    """Draw debug information when UI is enabled"""
    if not show_ui:
        return
        
    # === fps info
    fps_text = settings.font.render(f"FPS: {int(settings.clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (15, 15))

    # === position info
    pos_text = settings.font.render(f"Pos: ({player.pos.x:.0f}, {player.pos.y:.0f})", True, (255, 255, 255))
    screen.blit(pos_text, (15, 35))

    # === block and tile info
    current_block = player.get_current_block()
    if current_block:
        block_text = settings.font.render(f"Block: {current_block['tile_name']} ({current_block['block_x']}, {current_block['block_y']})", True, (255, 255, 255))
        screen.blit(block_text, (15, 55))
        
    # === status info
    status_list = []
    if player.jumping:
        status_list.append("Jumping")
    if player.sprinting:
        status_list.append("Sprinting")
    status_text = settings.font.render(f"Status: {', '.join(status_list)}", True, (255, 255, 255))
    screen.blit(status_text, (15, 75))
    
    draw_minimap(screen, player, npcs)

def draw_minimap(screen, player, npcs):
    """Draw the minimap in the corner of the screen"""
    mini_map_size = 100
    mini_map_surface = pygame.Surface((mini_map_size, mini_map_size))
    mini_map_surface.fill("#d97757")
    pygame.draw.rect(screen, (200, 200, 200), (screen.get_width() - mini_map_size - 23, 16.8, 106, 107))
    
    # Draw player on minimap
    player_mini_x = (player.pos.x / settings.MAP_WIDTH) * mini_map_size
    player_mini_y = (player.pos.y / settings.MAP_HEIGHT) * mini_map_size
    pygame.draw.circle(mini_map_surface, ("#e83b3b"), (player_mini_x, player_mini_y), 3)

    # Draw only nearby NPCs on minimap 
    for npc in npcs:
        # Only draw NPCs that are relatively close to player
        dx = abs(npc.pos.x - player.pos.x)
        dy = abs(npc.pos.y - player.pos.y)
        if dx < 20 and dy < 20:
            npc_mini_x = (npc.pos.x / settings.MAP_WIDTH) * mini_map_size
            npc_mini_y = (npc.pos.y / settings.MAP_HEIGHT) * mini_map_size
            pygame.draw.circle(mini_map_surface, ("#03ff00"), (npc_mini_x, npc_mini_y), 2)
    
    screen.blit(mini_map_surface, (screen.get_width() - mini_map_size - 20, 20))