import random
import pygame
from game.constants import TILE_SIZE, MIN_MAZE_SIZE, MAX_MAZE_SIZE, WALKABLE_PERCENTAGE, MAZE_BLUE, MAZE_BLACK

class Maze:
    def __init__(self):
        # Determine maze size (random between min and max)
        self.size = random.randint(MIN_MAZE_SIZE, MAX_MAZE_SIZE)
        
        # Initialize maze grid (0 = wall, 1 = path)
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        # Generate the maze
        self._generate_maze()
        
        # Create warp tunnels
        self._create_warp_tunnels()
        
        # Create surface for rendering
        self.surface = pygame.Surface((self.size * TILE_SIZE, self.size * TILE_SIZE))
        self._render_maze_surface()
    
    def _generate_maze(self):
        """Generate a procedural maze with at least 60% walkable area"""
        # Start with a completely walled maze
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        # Use a modified recursive backtracking algorithm
        # Start from the center
        start_x, start_y = self.size // 2, self.size // 2
        self.grid[start_y][start_x] = 1  # Mark as path
        
        # Use stack for backtracking
        stack = [(start_x, start_y)]
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]  # Up, Right, Down, Left
        
        while stack:
            current_x, current_y = stack[-1]
            
            # Find unvisited neighbors
            unvisited = []
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[ny][nx] == 0:
                    unvisited.append((nx, ny, dx // 2, dy // 2))
            
            if unvisited:
                # Choose random unvisited neighbor
                next_x, next_y, wall_x, wall_y = random.choice(unvisited)
                
                # Remove wall between current and next
                self.grid[current_y + wall_y][current_x + wall_x] = 1
                
                # Mark next cell as path
                self.grid[next_y][next_x] = 1
                
                # Push next cell to stack
                stack.append((next_x, next_y))
            else:
                # Backtrack
                stack.pop()
        
        # Ensure we have at least 60% walkable area
        walkable_count = sum(row.count(1) for row in self.grid)
        total_cells = self.size * self.size
        
        # If we don't have enough walkable area, add more paths
        while walkable_count / total_cells < WALKABLE_PERCENTAGE:
            # Find a wall adjacent to a path
            x, y = random.randint(1, self.size - 2), random.randint(1, self.size - 2)
            if self.grid[y][x] == 0:  # If it's a wall
                # Check if it's adjacent to a path
                adjacent_paths = 0
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[ny][nx] == 1:
                        adjacent_paths += 1
                
                if adjacent_paths > 0:
                    self.grid[y][x] = 1  # Convert to path
                    walkable_count += 1
    
    def _create_warp_tunnels(self):
        """Create warp tunnels at the center of each edge"""
        # Top and bottom tunnels
        mid_x = self.size // 2
        self.grid[0][mid_x] = 2  # Top tunnel
        self.grid[self.size - 1][mid_x] = 2  # Bottom tunnel
        
        # Left and right tunnels
        mid_y = self.size // 2
        self.grid[mid_y][0] = 2  # Left tunnel
        self.grid[mid_y][self.size - 1] = 2  # Right tunnel
    
    def _render_maze_surface(self):
        """Pre-render the maze surface for efficient drawing"""
        self.surface.fill(MAZE_BLACK)  # Fill with classic Pac-Man black background
        
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] > 0:  # Path or tunnel
                    # Draw path tile (black for classic Pac-Man look)
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.surface, MAZE_BLACK, rect)
                else:
                    # Draw wall (blue for classic Pac-Man look)
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.surface, MAZE_BLUE, rect)
                    
                    # Add subtle inner bevel for walls
                    inner_rect = rect.inflate(-2, -2)
                    pygame.draw.rect(self.surface, MAZE_BLUE, inner_rect)
                
                # Add visual indicator for tunnels
                if self.grid[y][x] == 2:
                    tunnel_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.surface, (50, 50, 150), tunnel_rect, 2)
    
    def is_walkable(self, x, y):
        """Check if a position is walkable"""
        # Handle out of bounds
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False
            
        # Check if it's a path or tunnel
        return self.grid[y][x] > 0
    
    def get_warp_destination(self, x, y):
        """Get destination coordinates when entering a warp tunnel"""
        mid_x = self.size // 2
        mid_y = self.size // 2
        
        # Top tunnel
        if y == 0 and x == mid_x:
            return x, self.size - 1
        
        # Bottom tunnel
        if y == self.size - 1 and x == mid_x:
            return x, 0
        
        # Left tunnel
        if x == 0 and y == mid_y:
            return self.size - 1, y
        
        # Right tunnel
        if x == self.size - 1 and y == mid_y:
            return 0, y
        
        # Not a tunnel
        return x, y
    
    def get_random_walkable_position(self):
        """Get a random walkable position in the maze"""
        walkable_positions = []
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] == 1:  # Only regular paths, not tunnels
                    walkable_positions.append((x, y))
        
        return random.choice(walkable_positions) if walkable_positions else (self.size // 2, self.size // 2)
    
    def render(self, screen, offset_x=0, offset_y=0):
        """Render the maze to the screen"""
        screen.blit(self.surface, (offset_x, offset_y))
