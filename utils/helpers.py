import pygame
import random
import os
import numpy

def load_sound(filename):
    """Load a sound file and return a pygame Sound object"""
    if not pygame.mixer or not pygame.mixer.get_init():
        return None
        
    try:
        # Try to load the sound file
        filepath = os.path.join('assets', 'sounds', filename)
        if os.path.exists(filepath):
            try:
                sound = pygame.mixer.Sound(filepath)
                return sound
            except Exception as e:
                print(f"Error loading sound file: {filename}, error: {e}")
                # Create a placeholder sound
                return create_placeholder_sound()
        else:
            print(f"Sound file not found: {filepath}, creating placeholder")
            return create_placeholder_sound()
    except Exception as e:
        print(f"Could not load sound file: {filename}, error: {e}")
        return create_placeholder_sound()

def create_placeholder_sound():
    """Create a placeholder silent sound"""
    try:
        import numpy
        # Create a very short silent sound (0.1 seconds)
        sample_rate = 22050
        buffer = numpy.zeros((int(sample_rate * 0.1), 2), dtype=numpy.int16)
        sound = pygame.mixer.Sound(buffer=buffer)
        return sound
    except Exception as e:
        print(f"Could not create placeholder sound: {e}")
        try:
            # Try an alternative method
            sound = pygame.mixer.Sound(buffer=bytes([0] * 44100))
            return sound
        except:
            print("All methods to create placeholder sound failed")
            return None

def create_placeholder_image(width, height, color, name):
    """Create a placeholder image for development"""
    surface = pygame.Surface((width, height))
    surface.fill(color)
    
    # Save to assets folder
    os.makedirs(os.path.join('assets', 'images'), exist_ok=True)
    pygame.image.save(surface, os.path.join('assets', 'images', f"{name}.png"))
    
    return surface

def get_random_color(exclude_color=None):
    """Get a random color, optionally excluding a specific color"""
    colors = [
        (255, 0, 0),      # Red
        (255, 192, 203),  # Pink
        (255, 165, 0),    # Orange
        (0, 255, 255),    # Cyan
        (0, 255, 0),      # Green
        (255, 255, 0),    # Yellow
        (128, 0, 128),    # Purple
        (255, 255, 255),  # White
    ]
    
    if exclude_color:
        colors = [c for c in colors if c != exclude_color]
    
    return random.choice(colors)

def calculate_offset(maze_size, tile_size, screen_width, screen_height):
    """Calculate offset to center the maze on screen"""
    maze_pixel_size = maze_size * tile_size
    offset_x = (screen_width - maze_pixel_size) // 2
    offset_y = (screen_height - maze_pixel_size) // 2
    return offset_x, offset_y
