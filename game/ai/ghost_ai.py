import random
import pygame
from game.ai.pathfinding import AStar
from game.constants import AI_DECISION_TIME, AI_VISION_RADIUS

class GhostAI:
    def __init__(self, ghost, maze):
        self.ghost = ghost
        self.maze = maze
        self.pathfinder = AStar(maze)
        self.current_path = []
        self.target = None
        self.last_decision_time = 0
        self.decision_interval = AI_DECISION_TIME  # ms between AI decisions
        self.last_random_move_time = 0
        self.random_move_interval = 1000  # ms between random moves
    
    def update(self, pacmans, ghosts):
        """Update AI decision making"""
        current_time = pygame.time.get_ticks()
        
        # Only make decisions at certain intervals
        if current_time - self.last_decision_time < self.decision_interval:
            self._follow_path()
            return
            
        self.last_decision_time = current_time
        
        # Current position
        current_pos = (self.ghost.grid_x, self.ghost.grid_y)
        
        # Find targets within vision radius
        visible_pacmans = []
        visible_ghosts = []
        
        # Check for visible PacMans
        for pacman in pacmans:
            if not pacman.active:
                continue
                
            pacman_pos = (pacman.grid_x, pacman.grid_y)
            distance = self._calculate_distance(current_pos, pacman_pos)
            
            if distance <= AI_VISION_RADIUS:
                # Check if there's a clear path to the PacMan (no walls in between)
                path = self.pathfinder.find_path(current_pos, pacman_pos)
                if path and len(path) > 0:
                    visible_pacmans.append((pacman, distance))
        
        # Check for visible ghosts
        for other_ghost in ghosts:
            if other_ghost is self.ghost or not other_ghost.alive or other_ghost.dying:
                continue
                
            ghost_pos = (other_ghost.grid_x, other_ghost.grid_y)
            distance = self._calculate_distance(current_pos, ghost_pos)
            
            if distance <= AI_VISION_RADIUS:
                # Only target ghosts with lower level
                if other_ghost.level < self.ghost.level:
                    # Check if there's a clear path to the ghost (no walls in between)
                    path = self.pathfinder.find_path(current_pos, ghost_pos)
                    if path and len(path) > 0:
                        visible_ghosts.append((other_ghost, distance))
        
        # Prioritize targets
        target_entity = None
        
        # First priority: nearest PacMan
        if visible_pacmans:
            visible_pacmans.sort(key=lambda x: x[1])  # Sort by distance
            target_entity = visible_pacmans[0][0]
        
        # Second priority: nearest weaker ghost
        elif visible_ghosts:
            visible_ghosts.sort(key=lambda x: x[1])  # Sort by distance
            target_entity = visible_ghosts[0][0]
        
        # If we have a target, set path to it
        if target_entity:
            target_pos = (target_entity.grid_x, target_entity.grid_y)
            self.target = target_entity
            self.current_path = self.pathfinder.find_path(current_pos, target_pos)
            
            # Remove the first position (current position)
            if self.current_path and len(self.current_path) > 0 and self.current_path[0] == current_pos:
                self.current_path.pop(0)
        else:
            # No target in sight, move randomly but less frequently
            if current_time - self.last_random_move_time >= self.random_move_interval:
                self._random_movement()
                self.last_random_move_time = current_time
        
        # Follow the path
        self._follow_path()
    
    def _has_line_of_sight(self, start, end):
        """Check if there's a clear line of sight between two positions"""
        # Use A* pathfinding to check if there's a valid path
        path = self.pathfinder.find_path(start, end)
        
        # If there's no path, there's no line of sight
        if not path:
            return False
            
        # Check if the path is direct (Manhattan distance equals path length)
        manhattan_distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
        
        # Path length includes start and end points, so we need to subtract 1
        path_length = len(path) - 1
        
        # Only consider it line of sight if the path is direct or nearly direct
        # (allowing for one extra step for diagonal movement)
        return path_length <= manhattan_distance + 1
    
    def _follow_path(self):
        """Follow the current path"""
        if not self.current_path or len(self.current_path) == 0:
            return
            
        # Get next position in path
        next_pos = self.current_path[0]
        
        # Verify next position is adjacent and walkable
        dx = next_pos[0] - self.ghost.grid_x
        dy = next_pos[1] - self.ghost.grid_y
        
        # Ensure we're only moving in one direction at a time
        if dx != 0 and dy != 0:
            # Prioritize x movement
            dy = 0
            dx = 1 if dx > 0 else -1
        else:
            # Normalize to single step
            dx = 1 if dx > 0 else (-1 if dx < 0 else 0)
            dy = 1 if dy > 0 else (-1 if dy < 0 else 0)
        
        # Verify the move is valid
        new_x = self.ghost.grid_x + dx
        new_y = self.ghost.grid_y + dy
        
        if not self.maze.is_walkable(new_x, new_y):
            # Invalid move, recalculate path
            self.current_path = []
            return
        
        # Try to move
        if self.ghost.move(dx, dy, self.maze):
            # Successfully moved, remove this position from path
            self.current_path.pop(0)
        else:
            # Move failed, clear path to force recalculation
            self.current_path = []
    
    def _random_movement(self):
        """Choose a random direction to move"""
        current_pos = (self.ghost.grid_x, self.ghost.grid_y)
        
        # Get possible directions
        possible_moves = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy
            
            if self.maze.is_walkable(new_x, new_y):
                possible_moves.append((dx, dy))
        
        # If we have possible moves, choose one randomly
        if possible_moves:
            # Prefer not to reverse direction if possible
            forward_moves = [m for m in possible_moves if m != (-self.ghost.direction[0], -self.ghost.direction[1])]
            
            if forward_moves and random.random() < 0.8:  # 80% chance to not reverse
                dx, dy = random.choice(forward_moves)
            else:
                dx, dy = random.choice(possible_moves)
            
            # Set path to this direction
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy
            self.current_path = [(new_x, new_y)]
    
    def _calculate_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
