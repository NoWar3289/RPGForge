import pygame
from settings import TILE_SIZE

# Texture cache to avoid loading the same texture multiple times
texture_cache = {}

def get_texture(path, size=TILE_SIZE, use_alpha=False):
    """Load and cache textures for efficient reuse"""
    cache_key = f"{path}_{size}_{use_alpha}"
    if cache_key not in texture_cache:
        if use_alpha:
            img = pygame.image.load(path).convert_alpha()
            texture_cache[cache_key] = pygame.transform.scale(img, (size, size))
        else:
            img = pygame.image.load(path).convert()
            texture_cache[cache_key] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    return texture_cache[cache_key]

# Load all game textures
def load_textures():
    # Tile textures
    textures = {
        'grass': get_texture("./textures/tiles/grass.png"),
        'water': get_texture("./textures/tiles/water.png"),
        'stone': get_texture("./textures/tiles/stone.png"),
        'bridge': get_texture("./textures/tiles/bridge.png"),
        'tree': get_texture("./textures/tiles/tree.png"),
        'grass_alt': get_texture("./textures/tiles/grass001.png"),
        'bedrock': get_texture("./textures/tiles/bedrock.png"),
        
        # Player textures
        'player_default': get_texture("./textures/player/default.png", TILE_SIZE, True),
        'player_up': get_texture("./textures/player/up.png", TILE_SIZE, True),
        'player_down': get_texture("./textures/player/down.png", TILE_SIZE, True),
        'player_right': get_texture("./textures/player/right.png", TILE_SIZE, True),
        'player_left': get_texture("./textures/player/left.png", TILE_SIZE, True),
        'player_jump': get_texture("./textures/player/default.png", 128, True),
        
        # NPC textures
        'npc': get_texture("./textures/player/npc.png", 16, True),
        'npc_left': get_texture("./textures/player/npc_left.png", 16, True),
        'npc_right': get_texture("./textures/player/npc_right.png", 16, True),
    }
    
    # Create tile mapping
    tile_mapping = {
        0: textures['bridge'],      # spawn
        1: textures['grass'],       # grass
        2: textures['stone'],       # stone
        3: textures['water'],       # water (collidable)
        4: textures['tree'],        # tree (collidable)
        5: textures['grass_alt'],   # more grass
        9: textures['grass_alt'],   # more grass
        10: textures['bedrock']     # bedrock border (collidable)
    }
    
    textures['tile_mapping'] = tile_mapping
    
    return textures