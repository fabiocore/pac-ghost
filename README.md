# Pac-Ghost

A battle-royale style maze game inspired by Pac-Man, built with PyGame and Amazon Q.

This concept was created for the [Amazon Q Developer "Quack The Code" Challenge (dev.to)](https://dev.to/challenges/aws-amazon-q-v2025-04-30).

## Game Description

Pac-Ghost turns the classic maze into a battle-royale: you're the blue ghost competing against nine colorful AI ghosts. Stationary PacMan characters materialize every few seconds; gobbling one boosts your level and speed, letting you hunt weaker ghosts while dodging stronger predators. Collisions erase the lower-level ghost or wipe out equals together. Stay clever, keep evolving, and be the lone phantom haunting the neon corridors when the rest have blinked out.

## Features

- **Battle Royale Gameplay**: 10 ghosts (1 player, 9 AI) compete to be the last one standing
- **Procedurally Generated Mazes**: Every game has a unique maze layout
- **Level Progression**: Consume PacMan characters to level up and increase speed
- **Intelligent AI**: AI ghosts use A* pathfinding to hunt PacMan or weaker ghosts
- **Classic Arcade Style**: Retro graphics and sound inspired by the original Pac-Man

## Controls

- **Arrow Keys** or **WASD**: Move your ghost
- **Enter**: Select menu options

## Installation

1. Ensure you have Python 3.x installed
2. Install PyGame:
   ```
   pip install pygame
   ```
3. Clone this repository:
   ```
   git clone git@github.com:fabiocore/pac-ghost.git
   ```
4. Run the game:
   ```
   cd pac-ghost
   python main.py
   ```

## Game Mechanics

- All ghosts start at Level 1 with the same speed
- A stationary PacMan spawns every 7 seconds (maximum 4 on screen at once)
- Touching a PacMan increases your level and speed
- When ghosts collide, the higher level ghost survives
- If equal level ghosts collide, both are eliminated
- The last ghost standing wins

## Project Structure

```
pac-ghost/
├── main.py              # Entry point
├── game/                # Game logic
│   ├── constants.py     # Game constants
│   ├── game.py          # Main game class
│   ├── maze.py          # Maze generation
│   ├── entities/        # Game entities
│   ├── ai/              # AI logic
│   └── ui/              # User interface
├── assets/              # Game assets
│   ├── images/          # Sprites
│   └── sounds/          # Sound effects
└── utils/               # Utility functions
```

## Credits

- Game concept and implementation: [Fabio Ferreira]
- Inspired by the classic Pac-Man game by Namco
