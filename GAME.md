# Pac-Ghost About
Pac‑Ghost turns the classic maze into a battle‑royale: you’re the blue ghost competing nine colourful AI. Stationary PacMan materialise every few seconds; gobbling one boosts your level and speed, letting you hunt weaker ghosts while dodging stronger predators—collisions erase the low‑level or wipe out equals together. Stay clever, keep evolving, and be the lone phantom haunting the neon corridors when the rest have blinked out.
Pac-Ghost is a classic looking and feel PacMan like game, but with different mechanics.

# Pac-Ghost Machanics and Implementation
- Concept — Pac‑Ghost is a PyGame battle‑maze: 10 ghosts (1 blue player, 9 AI) fight to be last alive.
- Start — All ghosts spawn at Level 1 with same speed; colours: player blue, AI random non‑blue.
- Levelling — A Static PacMan spawn every 7 s (cap 4); touching one gives +1 level and little bit of improved speed.
- Speed Formula — speed = base_speed + (level‑1) * speed_bonus_per_level.
- Maze — Procedurally generated square (25–35 tiles), ≥ 60 % walkable, four edge‑centred warp tunnels that teleport top↔bottom, left↔right.
- Player Control — Arrow/WASD grid‑locked movement; sprites tween at 60 FPS.
- AI Logic — Every 0.2 s each ghost scans radius 12: prefers nearest PacMan; else hunts nearest lower‑level ghost; paths with A*.
- Collision Rules — Same tile, same frame: higher level survives; equal levels kill each other; death = 3 s blink then removal.
- Spectator Mode — On player death camera detaches; user can watch until the match ends.
- Victory — Match ends when one ghost remains; if it’s blue, player wins, otherwise AI wins.
- PacMan Timer — Continuous; if cap reached (x4), spawns are skipped but countdown keeps running.
- Audio & FX — Use PyGame sound/Howler for pickups and kills; death blink via alpha toggle; optional particle “poof”.

# Ghosts Look
Each ghost is a squat, domed sprite that also occupies roughly 28 × 28 px inside the 32‑pixel tile, its curved “head” tapering into a short body with four scalloped feet that billow as it drifts. The palette starts with a solid mid‑tone (royal‑blue for the player; red, pink, orange, cyan, green, yellow, purple or white for AI), then layers a soft 3‑pixel highlight down the left curve and a shadow line along the lower right, giving a candy‑shell sheen. Two oversized oval eyes—pure white with charcoal pupils—float near the crown; the pupils slide subtly in the travel direction every few frames, adding life without full animation. To suggest motion, the bottom fringe alternates between two frames: feet angled outward, then inward, creating a gentle “hover‑flap” at 8 fps. When a ghost dies, its fill colour toggles with transparency every 0.1 s for three seconds, then the sprite collapses into a faint, four‑pixel‑tall mist that fades out. Above the head, the level label (“Lv N”) sits in a pixel font, center‑aligned, its color auto‑contrasted—white over dark ghosts, navy over lighter ones—so the number is always readable amid the maze’s cobalt corridors.

# PacMan Look
Picture a perfectly round, glossy coin‑yellow puck that fills most of a single maze tile—about 28×28 px inside a 32 × 32 grid. Instead of the familiar wedge “mouth,” this PacMan keeps its jaws shut, so the circle is unbroken. A barely perceptible horizontal seam—two rows of slightly darker yellow pixels—marks where the mouth would open, hinting at latent hunger. A single black, almond‑shaped eye sits high on the right side, giving it just enough personality without animation. To make it pop against the dark‑blue maze walls, the sprite has a one‑pixel, warm‑orange rim light along its upper‑left edge and a two‑frame idle shimmer: every half‑second the highlight shifts by one pixel, suggesting a gentle glint rather than movement.

# The Maze
- Imagine the maze as a glowing, top‑down slice of neon circuitry—inky‑blue corridors carved out of solid midnight walls. Every match begins with a fresh labyrinth, so while its spirit recalls the classic Pac‑Man layout, its shape is never repeated.
- Tiles and scale: the board is a square grid between roughly 25 × 25 and 35 × 35 tiles. Walls are deep‑blue blocks with a faint inner bevel; floor tiles are a slightly lighter navy, helping pickups and ghosts pop.
- KEEP THE STYLE AND LOOKING FEEL LIKE THE ORIGINAL PACMAN GAME. 

# Assets Folder
- pacman.svg : PacMan asset svg
- death-effect.svg : Death effect svg
- ghost.svg : Players's blue color ghost svg
- ghost-colors.svg : Other ghosts svg