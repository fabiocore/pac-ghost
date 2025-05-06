#!/usr/bin/env python3
import pygame
import sys
from game.game import Game
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE

def main():
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption(TITLE)
    
    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # Create game instance
    game = Game(screen)
    
    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Render game
        game.render()
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
