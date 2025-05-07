import settings
import json
from utils.sound_manager import play_sound, GameSounds


def load_collision_data():
    """Load collision data from mapdata.json and update settings"""
    try:
        with open("./mapdata.json", 'r') as f:
            map_data = json.load(f)
            
            # Build collision map from tile data
            collision_data = {}
            collidable_list = []
            
            for tile_id, tile_info in map_data.get("tiles", {}).items():
                is_collidable = tile_info.get("collidable", False)
                int_id = int(tile_id)
                collision_data[int_id] = is_collidable
                
                # If tile is collidable, add to the list
                if is_collidable:
                    collidable_list.append(int_id)
            
            # Update the global setting
            settings.COLLIDABLE_TILES = collidable_list
            
            return collision_data
            
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading collision data: {e}")
        # Return empty collision data if file not found
        return {}

# Initialize collision data on module import
collision_data = load_collision_data()

def is_blocked(map_data, world_x, world_y):
    """Check if a position in the world is blocked (collidable)"""
    # Convert world coordinates to map coordinates
    map_x = int(world_x)
    map_y = int(world_y)
    
    # Check if coordinates are within map boundaries
    if 0 <= map_y < settings.MAP_HEIGHT and 0 <= map_x < settings.MAP_WIDTH:
        tile_id = map_data[map_y][map_x]
        
        # Check if the tile is collidable based on JSON data
        return collision_data.get(tile_id, False)
    else:
        # Out of map boundaries is considered blocked
        return True

def process_npc_collisions(player, npcs_list):
    """Process collisions between the player and NPCs"""
    npcs_to_remove = []
    
    for npc in npcs_list:
        if player.jumping and player.rect.colliderect(npc.rect):
            npcs_to_remove.append(npc)
            settings.POINTS += 1
            play_sound(GameSounds.NPC_HIT, settings.SFX_VOLUME)
            play_sound(GameSounds.POINT_COLLECT, settings.SFX_VOLUME * 0.7)
    
    # Remove the NPCs that were jumped on
    for npc in npcs_to_remove:
        npcs_list.remove(npc)