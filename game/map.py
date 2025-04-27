import pygame
import json
import settings
from settings import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT

class Map:
    def __init__(self, file_path="./maps/map000.txt"):
        self.data = self.load_map(file_path)
        self.add_border_to_map()
        self.tile_info = self.load_tile_info()

        self.map_number = self.extract_map_number(file_path)
        self.data = self.load_map(file_path)
        self.add_border_to_map()
        self.tile_info = self.load_tile_info()
    def load_tile_info(self):
        """Load tile information from mapdata.json"""
        try:
            with open("./mapdata.json", 'r') as f:
                map_data = json.load(f)
                return map_data.get("tiles", {})
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading mapdata.json: {e}")
            return {}
        
    def load_map(self, file_path):
        """Load map data from a file of any dimensions"""
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                
                # First determine the maximum width
                max_width = 0
                for line in lines:
                    # Split by any whitespace (space, tab) and count elements
                    nums = line.split()
                    max_width = max(max_width, len(nums))
                
                # Now create the map data with consistent width
                map_data = []
                for line in lines:
                    nums = [int(num) for num in line.split()]
                    # Pad with grass (1) if the row is shorter than max_width
                    while len(nums) < max_width:
                        nums.append(1)  # Use grass (1) as default filler
                    map_data.append(nums)
            
            # Update global map dimensions
            settings.MAP_HEIGHT = len(map_data)
            settings.MAP_WIDTH = max_width
            
            return map_data
            
        except FileNotFoundError:
            print(f"Map file not found: {file_path}")
            # Return a small default map if file not found
            default_map = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]  # Simple 3x3 map with spawn in center
            settings.MAP_HEIGHT = len(default_map)
            settings.MAP_WIDTH = len(default_map[0])
            return default_map
        except Exception as e:
            print(f"Error loading map: {e}")
            # Return a minimal map in case of other errors
            default_map = [[1, 0, 1], [1, 1, 1]]
            settings.MAP_HEIGHT = len(default_map)
            settings.MAP_WIDTH = len(default_map[0])
            return default_map
    
    def add_border_to_map(self):
        """Add a border of bedrock around the map"""
        bordered_map = []
        bordered_map.append([9] * (settings.MAP_WIDTH + 2))  # Top border
        for row in self.data:
            bordered_map.append([9] + row + [9])   # Side borders
        bordered_map.append([9] * (settings.MAP_WIDTH + 2))  # Bottom border
        
        # Update global map dimensions
        settings.MAP_WIDTH = len(bordered_map[0])
        settings.MAP_HEIGHT = len(bordered_map)
        self.data = bordered_map
    
    def find_spawn_location(self):
        """Find the spawn point (tile 0) in the map"""
        for y in range(settings.MAP_HEIGHT):
            for x in range(settings.MAP_WIDTH):
                if self.data[y][x] == 0:  # 0 is the spawn tile
                    return pygame.Vector2(x, y)
        
        # Fallback to position 1,1 if no spawn point found
        return pygame.Vector2(1, 1)
    
    def get_tile_name(self, tile_id):
        """Get the name of a tile based on its ID using the JSON data"""
        tile_str_id = str(tile_id)
        if tile_str_id in self.tile_info:
            return self.tile_info[tile_str_id].get("name", "Unknown")
        return "Unknown"
    
    def is_tile_collidable(self, tile_id):
        """Check if a tile is collidable based on JSON data"""
        tile_str_id = str(tile_id)
        if tile_str_id in self.tile_info:
            return self.tile_info[tile_str_id].get("collidable", False)
        return False  # Default to non-collidable
    
    def draw(self, screen, textures, camera_pos):
        """Draw visible parts of the map efficiently"""
        # Calculate the visible area
        screen_width, screen_height = screen.get_width(), screen.get_height()
        
        # Get fallback texture
        fallback_texture = textures.get('fallback') or textures.get(1) or next(iter(textures.values()))
        
        # Determine which tiles are visible based on camera position
        start_x = max(0, int(camera_pos.x // TILE_SIZE) - 1)
        start_y = max(0, int(camera_pos.y // TILE_SIZE) - 1)
        end_x = min(settings.MAP_WIDTH, start_x + (screen_width // TILE_SIZE) + 3)
        end_y = min(settings.MAP_HEIGHT, start_y + (screen_height // TILE_SIZE) + 3)
        
        # Draw only visible tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                # Calculate screen position
                screen_x = x * TILE_SIZE - camera_pos.x
                screen_y = y * TILE_SIZE - camera_pos.y
                
                # Only draw if within visible screen area
                if (-TILE_SIZE <= screen_x <= screen_width and 
                    -TILE_SIZE <= screen_y <= screen_height):
                    # Draw the tile
                    tile_id = self.data[y][x]
                    texture = textures['tile_mapping'].get(tile_id)
                    
                    # If texture is None, use fallback
                    if texture is None:
                        texture = fallback_texture
                        
                    screen.blit(texture, (screen_x, screen_y))


    def extract_map_number(self, file_path):
        """Extract map number from file path"""
        # Default to 0 if no number in filename
        import re
        match = re.search(r'map(\d+)\.txt', file_path)
        if match:
            return int(match.group(1))
        return 0
    
    def get_next_map_path(self):
        """Get the path to the next map"""
        next_number = self.map_number + 1
        return f"./maps/map{next_number:03d}.txt"

    def get_previous_map_path(self):
        """Get the path to the previous map"""
        prev_number = max(0, self.map_number - 1)
        return f"./maps/map{prev_number:03d}.txt"