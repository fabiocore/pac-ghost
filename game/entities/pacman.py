import pygame
import math
import os
from game.constants import TILE_SIZE, YELLOW

class PacMan:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.active = True
        
        # For animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 500  # ms between frames
        
        # Try to load SVG pacman image
        self.svg_loaded = False
        try:
            # Check if the SVG file exists
            if os.path.exists(os.path.join('assets', 'pacman.svg')):
                # We'll use our own rendering since PyGame doesn't directly support SVG
                self.svg_loaded = True
        except:
            print("Could not load pacman SVG, using fallback rendering")
        
        # Create PacMan surface
        self.surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.render_pacman()
    
    def render_pacman(self):
        """Render the PacMan sprite"""
        self.surface.fill((0, 0, 0, 0))  # Clear with transparency
        
        # PacMan dimensions
        radius = 14  # 28px diameter
        
        # Center in tile
        center_x = TILE_SIZE // 2
        center_y = TILE_SIZE // 2
        
        # Draw PacMan body
        pygame.draw.circle(self.surface, YELLOW, (center_x, center_y), radius)
        
        # Add rim light on upper-left edge - using a polygon instead of arc for compatibility
        rim_color = (255, 200, 100)  # Warm orange
        rim_points = []
        for angle in range(135, 315, 10):  # 3/4 pi to 7/4 pi in degrees
            rad = math.radians(angle)
            rim_x = center_x + int((radius) * math.cos(rad))
            rim_y = center_y + int((radius) * math.sin(rad))
            rim_points.append((rim_x, rim_y))
        
        if len(rim_points) >= 2:
            pygame.draw.lines(self.surface, rim_color, False, rim_points, 1)
        
        # Add horizontal seam for mouth
        seam_color = (220, 220, 0)  # Slightly darker yellow
        pygame.draw.line(self.surface, seam_color, 
                        (center_x - radius + 2, center_y), 
                        (center_x + radius - 2, center_y), 2)
        
        # Draw eye
        eye_radius = 3
        eye_x = center_x + radius // 2
        eye_y = center_y - radius // 2
        pygame.draw.ellipse(self.surface, (0, 0, 0), 
                          [eye_x - eye_radius, eye_y - eye_radius, 
                           eye_radius * 2, eye_radius * 1.5])
        
        # Add shimmer based on animation frame
        if self.animation_frame == 1:
            shimmer_pos = (center_x - radius // 2, center_y - radius // 2)
            shimmer_radius = 3
            pygame.draw.circle(self.surface, (255, 255, 200), shimmer_pos, shimmer_radius)
    
    def update(self, dt):
        """Update PacMan animation"""
        if not self.active:
            return
            
        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = 1 - self.animation_frame  # Toggle between 0 and 1
            self.render_pacman()
    
    def collect(self):
        """Mark PacMan as collected"""
        self.active = False
    
    def render(self, screen, offset_x=0, offset_y=0):
        """Render PacMan to the screen"""
        if not self.active:
            return
            
        screen.blit(self.surface, (self.pixel_x + offset_x, self.pixel_y + offset_y))
