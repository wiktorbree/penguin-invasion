import pygame

class PhysicsEntity:
    def __init__(self, game, entity_type, pos, size) -> None:
        self.game = game
        self.type = entity_type
        self.rect_pos = pygame.FRect(pos[0], pos[1], size[0], size[1])
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-5, -5)
        self.flip = False
        self.set_action('idle')

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy_anim()

    def update(self, tilemap, movement=(0, 0)):

        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        # frame_movement returns a tuple of x and y movement that is happening in one frame
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # update the x position of entity
        self.rect_pos[0] += frame_movement[0]

        for rect in tilemap.physics_rects_around(self.rect_pos):
            if self.rect_pos.colliderect(rect):
                # snap entity position to left/right side of tile position
                if frame_movement[0] > 0:
                    self.rect_pos.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    self.rect_pos.left = rect.right
                    self.collisions['left'] = True

        # update the y position of entity
        self.rect_pos[1] += frame_movement[1]

        for rect in tilemap.physics_rects_around(self.rect_pos):
            if self.rect_pos.colliderect(rect):
                # snap entity position to top/bottom side of tile position
                if frame_movement[1] > 0:
                    self.rect_pos.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    self.rect_pos.top = rect.bottom
                    self.collisions['up'] = True

        if movement[0] > 0:
            self.flip = True
        if movement[0] < 0:
            self.flip = False

        # adding gravity to the entity, min ensure that the y in velocity does not exceed 5
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()
    
    def render(self, surf):
        #surf.blit(self.game.assets['player'], self.rect_pos)
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.rect_pos[0] + self.anim_offset[0], self.rect_pos[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size) -> None:
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
    
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
        
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')