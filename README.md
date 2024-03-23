
# Penguin Invasion

Penguin Invasion is a Python game made using PyGame-CE library. It's my second game I'm making using pygame.

## About Penguin Invasion

Penguin Invasion is a 2D platformer where you play as a chicken trying to avoid blind penguins that have invaded the Grassland, your home. Despite their blindness, these penguins possess a dangerous power: touching them causes an explosion! So, be cautious and navigate carefully. Your mission is to reach the Arctic to save the Frozen Shark, the only creature capable of defeating the penguins. You are the last hope for the animals of the Grassland!

**Game:**
![Image of the game](screenshots/1.png)
**Menu:**
![Image of the game](screenshots/0.png)
**Simple Level Editor:**
![Image of the game](screenshots/2.png)

It's my second Pygame game and the first one that's using OOP. This game is based on tutorials from Clear Code, Coding with Russ, DaFluffyPotato, and others. It's still a work in progress, but it's finally playable. I will gradually update it and hopefully make it a playable, fun, short game.


## Updates
*In the form of a concise list*

**Version: 1.1**
- Added pause menu
- Added options button for later use
- Some other minor changes


**Version: 1.0**
- Added menu
- Added sounds
- Added pausing
- Fixed minor bugs
- The game is kinda done :)

**Version: 0.9**
- Added level ending object (the sign)
- Added transitions after death and when player complete the level
- Fixed grass texture
- Added outline to almost everything (thru code)

**Version: 0.8**
- Added death for the player
- Added particles (blood when players die) and script that handles them
- Added screenshake
- Added new map loading function, so now there can be multiple levels
- Fixed levitating player when running


**Version: 0.7**
- Added class for enemies
- Made spawners for enemies and player
- Made function to extract those spawners from tilemap
- Enemies for now just go in one direction and walk off the edge
- **Quick fix** - *Enemies now won't walk off the edge and also won't walk into a wall*


**Version: 0.6**
- Added ability to double jump, before the Player could jump infinitely
- Did some minor changes
- Fixed little bugs

**Version: 0.5**
- Added editor to make and edit levels
- Made some minor changes in tilemap script
- Now map in game is from JSON file :)

**Version: 0.4**
- Added animations to the Player
- Added background and moving clouds
- Made separate class for Player that inherits from PhysicsEntity

**Version: 0.3**
- Added tilemap script that handles making tiles
- Added collisions for entities and tiles
- Added ability to jump
- Refined getting rect from entity (using FRect now)

**Version: 0.2**
- Made entities script for handling entities logic such as player (and enemies in the future)
- Made utils script that handles utility stuff such as getting images
- Made assets variable that contains a dictionary with all assets that will be used in the game

**Version: 0.1**
- Made basic setup for pygame games
- Basic collision test
