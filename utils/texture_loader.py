import pygame
import json
import os
from settings import TILE_SIZE

# Texture cache to avoid loading the same texture multiple times
texture_cache = {}

def create_fallback_texture(size=TILE_SIZE):
    """Create a fallback texture (purple checkered pattern) for missing textures"""
    fallback = pygame.Surface((size, size))
    fallback.fill((255, 255, 255))  # Magenta
    for i in range(0, size, 8):
        for j in range(0, size, 8):
            if (i + j) % 16 == 0:
                pygame.draw.rect(fallback, (0, 0, 0), (i, j, 8, 8))
    return fallback

def get_texture(path, size=TILE_SIZE, use_alpha=False):
    """Load and cache textures for efficient reuse"""
    cache_key = f"{path}_{size}_{use_alpha}"
    if cache_key not in texture_cache:
        try:
            if os.path.exists(path):
                if use_alpha:
                    img = pygame.image.load(path).convert_alpha()
                    texture_cache[cache_key] = pygame.transform.scale(img, (size, size))
                else:
                    img = pygame.image.load(path).convert()
                    texture_cache[cache_key] = pygame.transform.scale(img, (size, size))
            else:
                print(f"Texture file not found: {path}")
                texture_cache[cache_key] = create_fallback_texture(size)
        except pygame.error as e:
            print(f"Error loading texture {path}: {e}")
            texture_cache[cache_key] = create_fallback_texture(size)
    return texture_cache[cache_key]

def load_textures():
    """Load all game textures based on mapdata.json"""
    textures = {}
    
    # Create a default fallback texture for missing textures
    fallback_texture = create_fallback_texture()
    textures['fallback'] = fallback_texture
    
    # Load tile metadata from JSON
    try:
        with open("./mapdata.json", 'r') as f:
            map_data = json.load(f)
            tile_data = map_data.get("tiles", {})
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error loading mapdata.json: {e}")
        tile_data = {}  # Use empty dict if file not found or invalid
    
    # Load tile textures based on JSON data
    for tile_id, tile_info in tile_data.items():
        texture_file = tile_info.get("texture")
        tile_name = tile_info.get("name")
        
        if texture_file and tile_name:
            texture_path = f"./textures/tiles/{texture_file}"
            textures[tile_name] = get_texture(texture_path)
            
            # Add to numeric lookup as well (as integers)
            try:
                int_id = int(tile_id)
                textures[int_id] = textures[tile_name]
            except ValueError:
                print(f"Invalid tile ID (not an integer): {tile_id}")
    
    # Create tile mapping dictionary for easy lookup
    tile_mapping = {}
    for tile_id, tile_info in tile_data.items():
        try:
            int_id = int(tile_id)
            tile_name = tile_info.get("name")
            if tile_name in textures:
                tile_mapping[int_id] = textures[tile_name]
        except ValueError:
            continue
    
    # Player textures
    textures['player_default'] = get_texture("./textures/player/default.png", TILE_SIZE, True)
    textures['player_up'] = get_texture("./textures/player/up.png", TILE_SIZE, True)
    textures['player_down'] = get_texture("./textures/player/down.png", TILE_SIZE, True)
    textures['player_right'] = get_texture("./textures/player/right.png", TILE_SIZE, True)
    textures['player_left'] = get_texture("./textures/player/left.png", TILE_SIZE, True)
    textures['player_jump'] = get_texture("./textures/player/default.png", 128, True)
    
    # NPC textures
    textures['npc'] = get_texture("./textures/player/npc.png", 16, True)
    textures['npc_left'] = get_texture("./textures/player/npc_left.png", 16, True)
    textures['npc_right'] = get_texture("./textures/player/npc_right.png", 16, True)
    
    # Store the complete tile mapping with fallback for missing textures
    for i in range(50):  # Support up to 50 tile IDs
        if i not in tile_mapping:
            tile_mapping[i] = fallback_texture
    
    textures['tile_mapping'] = tile_mapping
    
    # Store collision information
    collision_map = {}
    for tile_id, tile_info in tile_data.items():
        try:
            int_id = int(tile_id)
            collision_map[int_id] = tile_info.get("collidable", False)
        except ValueError:
            continue
    
    textures['collision_map'] = collision_map
    
    return textures