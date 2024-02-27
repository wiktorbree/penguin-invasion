import pygame

class PhysicsEntity:
    def __init__(self, game, entity_type, pos, size) -> None:
        self.game = game
        self.type = entity_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

    def rect(self):
        # create a rect for entity
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        
    def update(self, movement=(0, 0)):
        # frame_movement returns a tuple of x and y movement that is happening in one frame
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # update the position of entity
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
    
    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)
        