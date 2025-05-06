import pygame
import random
import numpy
import os
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, BLACK, BLUE, GHOST_COLORS, MAZE_BLACK,
    STATE_MENU, STATE_PLAYING, STATE_SPECTATING, STATE_GAME_OVER,
    PACMAN_SPAWN_TIME, MAX_PACMANS
)
from game.maze import Maze
from game.entities.ghost import Ghost
from game.entities.pacman import PacMan
from game.ai.ghost_ai import GhostAI
from game.ui.menu import Menu, GameOverMenu
from game.ui.hud import HUD, PacManTimer
from utils.helpers import get_random_color, calculate_offset, load_sound, create_placeholder_sound

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = STATE_MENU
        self.menu = Menu(screen)
        self.game_over_menu = None
        self.hud = HUD(screen)
        self.pacman_timer = PacManTimer(screen)
        
        # Game objects
        self.maze = None
        self.player = None
        self.ghosts = []
        self.ai_controllers = []
        self.pacmans = []
        
        # Game settings
        self.last_update_time = pygame.time.get_ticks()
        
        # Load sounds
        self.pickup_sound = load_sound('pickup.wav')
        self.elimination_sound = load_sound('elimination.wav')
        
        # Make sure we have sounds
        if not self.pickup_sound or not self.elimination_sound:
            print("Warning: Some sounds could not be loaded, using placeholders")
            # Create placeholder sounds if needed
            if not self.pickup_sound:
                self.pickup_sound = create_placeholder_sound()
            if not self.elimination_sound:
                self.elimination_sound = create_placeholder_sound()
    
    def handle_event(self, event):
        """Handle input events"""
        if self.state == STATE_MENU:
            option = self.menu.handle_event(event)
            if option == 'Start Game':
                self._start_new_game()
            elif option == 'Quit':
                pygame.quit()
                exit()
        
        elif self.state == STATE_GAME_OVER:
            option = self.game_over_menu.handle_event(event)
            if option == 'Play Again':
                self._start_new_game()
            elif option == 'Quit':
                pygame.quit()
                exit()
        
        elif self.state == STATE_PLAYING:
            if event.type == pygame.KEYDOWN:
                # Player movement
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.player.move(0, -1, self.maze)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.player.move(0, 1, self.maze)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.player.move(-1, 0, self.maze)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.player.move(1, 0, self.maze)
    
    def update(self):
        """Update game state"""
        # Calculate delta time
        current_time = pygame.time.get_ticks()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time
        
        if self.state == STATE_MENU:
            self.menu.update(dt)
        
        elif self.state == STATE_GAME_OVER:
            self.game_over_menu.update(dt)
        
        elif self.state in (STATE_PLAYING, STATE_SPECTATING):
            # Update PacMan timer
            if self.pacman_timer.update(dt):
                # Spawn new PacMan if we haven't reached the cap
                if self.pacman_timer.increment_count():
                    self._spawn_pacman()
            
            # Update entities
            for ghost in self.ghosts:
                ghost.update(dt)
            
            # Clean up inactive PacMans
            self.pacmans = [p for p in self.pacmans if p.active]
            
            for pacman in self.pacmans:
                pacman.update(dt)
            
            # Update AI
            for ai in self.ai_controllers:
                ai.update(self.pacmans, self.ghosts)
            
            # Check collisions
            self._check_collisions()
            
            # Check game over condition
            alive_ghosts = [g for g in self.ghosts if g.alive and not g.dying]
            if len(alive_ghosts) <= 1:
                # Game over
                player_won = self.player.alive and not self.player.dying
                self.game_over_menu = GameOverMenu(self.screen, player_won)
                self.state = STATE_GAME_OVER
            
            # Check if player died
            elif self.state == STATE_PLAYING and (not self.player.alive or self.player.dying):
                # Switch to spectator mode
                self.state = STATE_SPECTATING
    
    def render(self):
        """Render the game"""
        # Clear screen
        self.screen.fill(MAZE_BLACK)  # Use classic Pac-Man black background
        
        if self.state == STATE_MENU:
            self.menu.render()
        
        elif self.state == STATE_GAME_OVER:
            self.game_over_menu.render()
        
        elif self.state in (STATE_PLAYING, STATE_SPECTATING):
            # Calculate offset to center maze
            offset_x, offset_y = calculate_offset(
                self.maze.size, TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
            )
            
            # Render maze
            self.maze.render(self.screen, offset_x, offset_y)
            
            # Render PacMans
            for pacman in self.pacmans:
                pacman.render(self.screen, offset_x, offset_y)
            
            # Render ghosts
            for ghost in self.ghosts:
                ghost.render(self.screen, offset_x, offset_y)
            
            # Render HUD
            player_level = self.player.level if self.player.alive else 0
            alive_ghosts = len([g for g in self.ghosts if g.alive and not g.dying])
            self.hud.render(player_level, alive_ghosts, self.state == STATE_SPECTATING)
            self.pacman_timer.render()
    
    def _start_new_game(self):
        """Initialize a new game"""
        # Create maze
        self.maze = Maze()
        
        # Create player ghost
        player_pos = self.maze.get_random_walkable_position()
        self.player = Ghost(player_pos[0], player_pos[1], BLUE, is_player=True)
        self.ghosts = [self.player]
        
        # Create AI ghosts
        for _ in range(9):
            # Find position not occupied by another ghost
            while True:
                pos = self.maze.get_random_walkable_position()
                if not any(g.grid_x == pos[0] and g.grid_y == pos[1] for g in self.ghosts):
                    break
            
            # Create ghost with random color (not blue)
            ghost = Ghost(pos[0], pos[1], get_random_color(exclude_color=BLUE))
            self.ghosts.append(ghost)
            
            # Create AI controller for this ghost
            ai = GhostAI(ghost, self.maze)
            self.ai_controllers.append(ai)
        
        # Reset PacMans
        self.pacmans = []
        self.pacman_timer = PacManTimer(self.screen)
        
        # Set game state
        self.state = STATE_PLAYING
    
    def _spawn_pacman(self):
        """Spawn a new PacMan at a random position"""
        # Find position not occupied by another entity
        while True:
            pos = self.maze.get_random_walkable_position()
            if not any(g.grid_x == pos[0] and g.grid_y == pos[1] for g in self.ghosts) and \
               not any(p.grid_x == pos[0] and p.grid_y == pos[1] for p in self.pacmans):
                break
        
        # Create PacMan
        pacman = PacMan(pos[0], pos[1])
        self.pacmans.append(pacman)
    
    def _check_collisions(self):
        """Check for collisions between entities"""
        # Check ghost-pacman collisions
        for ghost in self.ghosts:
            if not ghost.alive or ghost.dying:
                continue
                
            for pacman in self.pacmans[:]:  # Create a copy of the list to safely remove items
                if not pacman.active:
                    continue
                    
                if ghost.collides_with(pacman):
                    # Ghost eats PacMan
                    pacman.collect()
                    ghost.level_up()
                    self.pacman_timer.decrement_count()
                    
                    # Play sound
                    try:
                        if self.pickup_sound:
                            self.pickup_sound.play()
                    except Exception as e:
                        print(f"Error playing pickup sound: {e}")
        
        # Check ghost-ghost collisions
        for i, ghost1 in enumerate(self.ghosts):
            if not ghost1.alive or ghost1.dying:
                continue
                
            for ghost2 in self.ghosts[i+1:]:
                if not ghost2.alive or ghost2.dying:
                    continue
                    
                if ghost1.collides_with(ghost2):
                    # Higher level ghost eliminates lower level
                    if ghost1.level > ghost2.level:
                        ghost2.start_death()
                        try:
                            if self.elimination_sound:
                                self.elimination_sound.play()
                        except Exception as e:
                            print(f"Error playing elimination sound: {e}")
                    elif ghost2.level > ghost1.level:
                        ghost1.start_death()
                        try:
                            if self.elimination_sound:
                                self.elimination_sound.play()
                        except Exception as e:
                            print(f"Error playing elimination sound: {e}")
                    else:
                        # Equal levels, both die
                        ghost1.start_death()
                        ghost2.start_death()
                        try:
                            if self.elimination_sound:
                                self.elimination_sound.play()
                        except Exception as e:
                            print(f"Error playing elimination sound: {e}")
