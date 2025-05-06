import pygame
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, MAZE_BLUE

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
    
    def render(self, player_level, ghosts_alive, spectator_mode=False):
        """Render the HUD with game information"""
        # Player level
        if not spectator_mode:
            level_text = self.font.render(f"Your Level: {player_level}", True, MAZE_BLUE)
            self.screen.blit(level_text, (20, 20))
        else:
            spectator_text = self.font.render("Spectator Mode", True, MAZE_BLUE)
            self.screen.blit(spectator_text, (20, 20))
        
        # Ghosts remaining
        ghosts_text = self.font.render(f"Ghosts: {ghosts_alive}", True, WHITE)
        self.screen.blit(ghosts_text, (SCREEN_WIDTH - 150, 20))
        
        # Controls reminder
        if not spectator_mode:
            controls_text = self.small_font.render("Controls: Arrow Keys or WASD", True, WHITE)
            self.screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))


class PacManTimer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 18)
        self.spawn_time = 7000  # ms
        self.max_pacmans = 4
        self.timer = 0
        self.pacman_count = 0
    
    def update(self, dt):
        """Update the PacMan spawn timer"""
        self.timer += dt
        
        # Reset timer when it reaches spawn time
        if self.timer >= self.spawn_time:
            self.timer = 0
            return True
        
        return False
    
    def increment_count(self):
        """Increment the PacMan count"""
        if self.pacman_count < self.max_pacmans:
            self.pacman_count += 1
            return True
        return False
    
    def decrement_count(self):
        """Decrement the PacMan count"""
        if self.pacman_count > 0:
            self.pacman_count -= 1
            return True
        return False
    
    def render(self):
        """Render the PacMan timer"""
        # Calculate progress
        progress = min(self.timer / self.spawn_time, 1.0)
        
        # Draw timer bar
        bar_width = 150
        bar_height = 15
        x = SCREEN_WIDTH - bar_width - 20
        y = 50
        
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, bar_width, bar_height))
        
        # Progress
        progress_width = int(bar_width * progress)
        pygame.draw.rect(self.screen, (255, 255, 0), (x, y, progress_width, bar_height))
        
        # Border
        pygame.draw.rect(self.screen, WHITE, (x, y, bar_width, bar_height), 1)
        
        # Text
        timer_text = self.font.render(f"PacMan: {self.pacman_count}/{self.max_pacmans}", True, WHITE)
        self.screen.blit(timer_text, (x, y - 20))
