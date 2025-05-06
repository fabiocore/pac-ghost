import heapq
import math

class AStar:
    def __init__(self, maze):
        self.maze = maze
    
    def find_path(self, start, end):
        """
        Find a path from start to end using A* algorithm
        
        Args:
            start: Tuple (x, y) of starting position
            end: Tuple (x, y) of ending position
            
        Returns:
            List of tuples representing the path from start to end,
            or an empty list if no path is found
        """
        # Check if start or end are not walkable
        if not self.maze.is_walkable(start[0], start[1]) or not self.maze.is_walkable(end[0], end[1]):
            return []
            
        # If start and end are the same, return just that position
        if start == end:
            return [start]
            
        # Initialize open and closed sets
        open_set = []
        closed_set = set()
        
        # Start node
        start_node = (0, 0, start, None)  # (f_score, g_score, position, parent)
        heapq.heappush(open_set, start_node)
        
        # Keep track of nodes and their scores
        g_scores = {start: 0}
        f_scores = {start: self._heuristic(start, end)}
        
        # Keep track of parents for path reconstruction
        parents = {}
        
        # Limit search to prevent infinite loops
        max_iterations = self.maze.size * self.maze.size
        iterations = 0
        
        while open_set and iterations < max_iterations:
            iterations += 1
            
            # Get node with lowest f_score
            _, g_score, current, parent = heapq.heappop(open_set)
            
            # If we reached the end, reconstruct and return the path
            if current == end:
                path = self._reconstruct_path(parents, current)
                return path
            
            # Add current to closed set
            closed_set.add(current)
            
            # Check neighbors
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # Skip if neighbor is in closed set
                if neighbor in closed_set:
                    continue
                
                # Skip if neighbor is not walkable
                if not self.maze.is_walkable(neighbor[0], neighbor[1]):
                    continue
                
                # Calculate tentative g_score
                tentative_g_score = g_score + 1
                
                # If neighbor is not in open set or has a better g_score
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update scores
                    parents[neighbor] = current
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = tentative_g_score + self._heuristic(neighbor, end)
                    
                    # Add to open set if not already there
                    if neighbor not in [n[2] for n in open_set]:
                        heapq.heappush(open_set, (f_scores[neighbor], g_scores[neighbor], neighbor, current))
        
        # No path found
        return []
    
    def _heuristic(self, a, b):
        """Calculate Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def _reconstruct_path(self, parents, current):
        """Reconstruct path from parents dictionary"""
        path = [current]
        while current in parents:
            current = parents[current]
            path.append(current)
        
        # Reverse to get path from start to end
        path.reverse()
        return path
