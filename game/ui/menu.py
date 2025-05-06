import pygame
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, BLACK, MAZE_BLACK, MAZE_BLUE

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 32)
        self.font_small = pygame.font.SysFont('Arial', 24)
        
        # Menu options
        self.options = ['Start Game', 'Quit']
        self.selected = 0
        
        # For blinking text
        self.blink_timer = 0
        self.blink_interval = 500  # ms
        self.show_prompt = True
    
    def handle_event(self, event):
        """Handle menu input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None
    
    def update(self, dt):
        """Update menu animations"""
        # Update blink timer
        self.blink_timer += dt
        if self.blink_timer >= self.blink_interval:
            self.blink_timer = 0
            self.show_prompt = not self.show_prompt
    
    def render(self):
        """Render the menu"""
        # Clear screen
        self.screen.fill(MAZE_BLACK)  # Classic Pac-Man black background
        
        # Draw title
        title = self.font_large.render('PAC-GHOST', True, MAZE_BLUE)  # Classic Pac-Man blue
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)
        
        # Draw subtitle
        subtitle = self.font_small.render('Battle Royale Edition', True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 50))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = MAZE_BLUE if i == self.selected else WHITE  # Classic Pac-Man blue for selected
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            self.screen.blit(text, text_rect)
        
        # Draw prompt
        if self.show_prompt:
            prompt = self.font_small.render('Press ENTER to select', True, WHITE)
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
            self.screen.blit(prompt, prompt_rect)


class GameOverMenu:
    def __init__(self, screen, player_won):
        self.screen = screen
        self.player_won = player_won
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 32)
        self.font_small = pygame.font.SysFont('Arial', 24)
        
        # Menu options
        self.options = ['Play Again', 'Quit']
        self.selected = 0
        
        # For blinking text
        self.blink_timer = 0
        self.blink_interval = 500  # ms
        self.show_prompt = True
    
    def handle_event(self, event):
        """Handle menu input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None
    
    def update(self, dt):
        """Update menu animations"""
        # Update blink timer
        self.blink_timer += dt
        if self.blink_timer >= self.blink_interval:
            self.blink_timer = 0
            self.show_prompt = not self.show_prompt
    
    def render(self):
        """Render the game over menu"""
        # Clear screen
        self.screen.fill(MAZE_BLACK)  # Classic Pac-Man black background
        
        # Draw title
        if self.player_won:
            title = self.font_large.render('YOU WIN!', True, MAZE_BLUE)  # Classic Pac-Man blue
        else:
            title = self.font_large.render('GAME OVER', True, (255, 0, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = MAZE_BLUE if i == self.selected else WHITE  # Classic Pac-Man blue for selected
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            self.screen.blit(text, text_rect)
        
        # Draw prompt
        if self.show_prompt:
            prompt = self.font_small.render('Press ENTER to select', True, WHITE)
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
            self.screen.blit(prompt, prompt_rect)
