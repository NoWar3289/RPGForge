import settings

def is_blocked(map_data, world_x, world_y):
    """Check if a position in the world is blocked (collidable)"""
    # Convert world coordinates to map coordinates
    map_x = int(world_x)
    map_y = int(world_y)
    
    # Check if coordinates are within map boundaries
    if 0 <= map_y < settings.MAP_HEIGHT and 0 <= map_x < settings.MAP_WIDTH:
        # Check if the tile is collidable
        return map_data[map_y][map_x] in settings.COLLIDABLE_TILES
    else:
        # Out of map boundaries is considered blocked
        return True

def process_npc_collisions(player, npcs_list):
    """Process collisions between the player and NPCs"""
    npcs_to_remove = []
    
    for npc in npcs_list:
        if player.jumping and player.rect.colliderect(npc.rect):
            npcs_to_remove.append(npc)
            settings.points += 1
    
    # Remove the NPCs that were jumped on
    for npc in npcs_to_remove:
        npcs_list.remove(npc)