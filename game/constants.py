# Game window settings
TITLE = "Pac-Ghost"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
NAVY_BLUE = (0, 0, 100)
MAZE_BLUE = (33, 33, 255)  # Classic Pac-Man maze blue
MAZE_BLACK = (0, 0, 0)     # Classic Pac-Man background black
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

# Ghost colors (excluding blue which is for player)
GHOST_COLORS = [RED, PINK, ORANGE, CYAN, GREEN, YELLOW, PURPLE, WHITE]

# Game settings
MIN_MAZE_SIZE = 25
MAX_MAZE_SIZE = 35
TILE_SIZE = 32
WALKABLE_PERCENTAGE = 0.6

# Game mechanics
BASE_SPEED = 1.5  # Reduced base speed
SPEED_BONUS_PER_LEVEL = 0.1  # Reduced speed bonus per level
PACMAN_SPAWN_TIME = 7000  # milliseconds
MAX_PACMANS = 4
AI_DECISION_TIME = 200  # milliseconds
AI_VISION_RADIUS = 8  # tiles (reduced from 12)
DEATH_BLINK_TIME = 3000  # milliseconds
DEATH_BLINK_INTERVAL = 100  # milliseconds

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_SPECTATING = 2
STATE_GAME_OVER = 3
