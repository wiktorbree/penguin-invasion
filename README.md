
# Penguin Invasion

Penguin Invasion is a Python game made using PyGame-CE library. It's my second game I'm making using pygame.

## About Penguin Invasion

```python
game_not_done = True

while game_not_done:
	about_section = 'EMPTY'
	working = True
```

## Updates
*In the form of a concise list*
**Version: 0.0.5**
- Added editor to make and edit levels
- Made some minor changes in tilemap script
- Now map in game is from JSON file :)

**Version: 0.0.4**
- Added animations to the Player
- Added background and moving clouds
- Made separate class for Player that inherits from PhysicsEntity

**Version: 0.0.3**
- Added tilemap script that handles making tiles
- Added collisions for entities and tiles
- Added ability to jump
- Refined getting rect from entity (using FRect now)

**Version: 0.0.2**
- Made entities script for handling entities logic such as player (and enemies in the future)
- Made utils script that handles utility stuff such as getting images
- Made assets variable that contains a dictionary with all assets that will be used in the game

**Version: 0.0.1**
- Made basic setup for pygame games
- Basic collision test
