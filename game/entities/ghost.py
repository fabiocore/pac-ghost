import pygame
import math
import time
import os
from game.constants import TILE_SIZE, BASE_SPEED, SPEED_BONUS_PER_LEVEL, BLUE, WHITE, DEATH_BLINK_TIME, DEATH_BLINK_INTERVAL

class Ghost:
    def __init__(self, x, y, color, is_player=False):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.color = color
        self.is_player = is_player
        self.level = 1
        self.speed = self._calculate_speed()
        self.direction = (0, 0)  # Current movement direction
        self.alive = True
        self.dying = False
        self.death_time = 0
        self.blink_state = False
        self.last_blink = 0
        
        # For animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 125  # ms between frames
        
        # Try to load SVG ghost image
        self.svg_loaded = False
        try:
            # Check if the SVG file exists
            if os.path.exists(os.path.join('assets', 'ghost.svg')):
                # We'll use our own rendering since PyGame doesn't directly support SVG
                self.svg_loaded = True
        except:
            print("Could not load ghost SVG, using fallback rendering")
        
        # Create ghost surface
        self.surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.render_ghost()
    
    def _calculate_speed(self):
        """Calculate ghost speed based on level"""
        return BASE_SPEED + (self.level - 1) * SPEED_BONUS_PER_LEVEL
    
    def render_ghost(self):
        """Render the ghost sprite"""
        self.surface.fill((0, 0, 0, 0))  # Clear with transparency
        
        # If dying and in blink off state, return transparent
        if self.dying and not self.blink_state:
            return
        
        # Ghost body dimensions
        width = 28
        height = 28
        
        # Center in tile
        x_offset = (TILE_SIZE - width) // 2
        y_offset = (TILE_SIZE - height) // 2
        
        # Draw ghost body
        body_rect = pygame.Rect(x_offset, y_offset, width, height - 8)
        pygame.draw.rect(self.surface, self.color, body_rect, border_radius=width//2)
        
        # Draw scalloped bottom
        feet_height = 8
        feet_width = width // 4
        
        # Animation: alternate between two frames for the feet
        if self.animation_frame == 0:
            feet_offsets = [0, 2, 0, 2]  # Feet positions for frame 1
        else:
            feet_offsets = [2, 0, 2, 0]  # Feet positions for frame 2
            
        for i in range(4):
            foot_x = x_offset + i * feet_width
            foot_y = y_offset + height - feet_height - feet_offsets[i]
            foot_rect = pygame.Rect(foot_x, foot_y, feet_width, feet_height)
            pygame.draw.rect(self.surface, self.color, foot_rect)
            
            # Draw arc for bottom of feet - using a filled polygon instead of arc for compatibility
            arc_points = []
            for angle in range(0, 180, 10):
                rad = math.radians(angle)
                arc_x = foot_x + feet_width // 2 + int((feet_width // 2) * math.cos(rad))
                arc_y = foot_y + feet_height + int((feet_width // 2) * math.sin(rad))
                arc_points.append((arc_x, arc_y))
            
            if arc_points:
                # Add the corners to create a filled shape
                arc_points.insert(0, (foot_x, foot_y + feet_height))
                arc_points.append((foot_x + feet_width, foot_y + feet_height))
                pygame.draw.polygon(self.surface, self.color, arc_points)
        
        # Add highlight on left side
        highlight_color = self._lighten_color(self.color)
        pygame.draw.line(self.surface, highlight_color, 
                        (x_offset + 3, y_offset + 3), 
                        (x_offset + 3, y_offset + height - 10), 3)
        
        # Add shadow on right side
        shadow_color = self._darken_color(self.color)
        pygame.draw.line(self.surface, shadow_color, 
                        (x_offset + width - 3, y_offset + 3), 
                        (x_offset + width - 3, y_offset + height - 10), 2)
        
        # Draw eyes
        eye_radius = 6
        left_eye_x = x_offset + width // 3
        right_eye_x = x_offset + 2 * width // 3
        eye_y = y_offset + height // 3
        
        # White part of eyes
        pygame.draw.circle(self.surface, WHITE, (left_eye_x, eye_y), eye_radius)
        pygame.draw.circle(self.surface, WHITE, (right_eye_x, eye_y), eye_radius)
        
        # Pupils (shift slightly in movement direction)
        pupil_radius = 3
        pupil_offset_x = 0
        pupil_offset_y = 0
        
        if self.direction[0] > 0:
            pupil_offset_x = 2
        elif self.direction[0] < 0:
            pupil_offset_x = -2
        
        if self.direction[1] > 0:
            pupil_offset_y = 2
        elif self.direction[1] < 0:
            pupil_offset_y = -2
        
        pygame.draw.circle(self.surface, (20, 20, 20), 
                          (left_eye_x + pupil_offset_x, eye_y + pupil_offset_y), 
                          pupil_radius)
        pygame.draw.circle(self.surface, (20, 20, 20), 
                          (right_eye_x + pupil_offset_x, eye_y + pupil_offset_y), 
                          pupil_radius)
        
        # Draw level number in the center of the ghost
        font = pygame.font.SysFont('Arial', 16, bold=True)
        level_text = font.render(f"{self.level}", True, (0, 0, 0))  # Black text
        text_rect = level_text.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
        self.surface.blit(level_text, text_rect)
    
    def _lighten_color(self, color):
        """Create a lighter version of the color for highlights"""
        r, g, b = color
        return min(r + 50, 255), min(g + 50, 255), min(b + 50, 255)
    
    def _darken_color(self, color):
        """Create a darker version of the color for shadows"""
        r, g, b = color
        return max(r - 50, 0), max(g - 50, 0), max(b - 50, 0)
    
    def level_up(self):
        """Increase ghost level and speed"""
        self.level += 1
        self.speed = self._calculate_speed()
    
    def move(self, dx, dy, maze):
        """Set movement direction for the ghost"""
        # Only allow movement if we've reached our target position
        if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
            # Ensure we're only moving one tile at a time
            dx = max(-1, min(1, dx))
            dy = max(-1, min(1, dy))
            
            # Ensure we're only moving in one direction at a time
            if dx != 0 and dy != 0:
                dy = 0  # Prioritize horizontal movement
            
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy
            
            # Double-check if the new position is walkable
            if not maze.is_walkable(new_x, new_y):
                return False
                
            # Set new direction and position
            self.direction = (dx, dy)
            self.grid_x = new_x
            self.grid_y = new_y
            
            # Check for warp tunnels
            self.grid_x, self.grid_y = maze.get_warp_destination(self.grid_x, self.grid_y)
            
            # Set new target position
            self.target_x = self.grid_x * TILE_SIZE
            self.target_y = self.grid_y * TILE_SIZE
            return True
        return False  # Return False if we haven't reached the target position
    
    def update(self, dt):
        """Update ghost position and animation"""
        if not self.alive:
            return
            
        # Handle death animation
        if self.dying:
            current_time = pygame.time.get_ticks()
            
            # Check if death animation is complete
            if current_time - self.death_time >= DEATH_BLINK_TIME:
                self.alive = False
                return
                
            # Update blink state
            if current_time - self.last_blink >= DEATH_BLINK_INTERVAL:
                self.blink_state = not self.blink_state
                self.last_blink = current_time
                self.render_ghost()
            return
        
        # Move towards target position
        if self.pixel_x != self.target_x or self.pixel_y != self.target_y:
            # Calculate movement distance (ensure it's not too large)
            move_distance = min(self.speed * dt, TILE_SIZE / 2)
            
            # Move in x direction
            if self.pixel_x < self.target_x:
                self.pixel_x = min(self.pixel_x + move_distance, self.target_x)
            elif self.pixel_x > self.target_x:
                self.pixel_x = max(self.pixel_x - move_distance, self.target_x)
                
            # Move in y direction
            if self.pixel_y < self.target_y:
                self.pixel_y = min(self.pixel_y + move_distance, self.target_y)
            elif self.pixel_y > self.target_y:
                self.pixel_y = max(self.pixel_y - move_distance, self.target_y)
        
        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = 1 - self.animation_frame  # Toggle between 0 and 1
            self.render_ghost()
    
    def start_death(self):
        """Start death animation"""
        self.dying = True
        self.death_time = pygame.time.get_ticks()
        self.last_blink = self.death_time
        self.blink_state = False
    
    def collides_with(self, other):
        """Check if this ghost collides with another entity"""
        # Only check collision if both are at the same grid position
        return self.grid_x == other.grid_x and self.grid_y == other.grid_y
    
    def render(self, screen, offset_x=0, offset_y=0):
        """Render the ghost to the screen"""
        if not self.alive:
            return
            
        screen.blit(self.surface, (self.pixel_x + offset_x, self.pixel_y + offset_y))
