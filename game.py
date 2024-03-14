import sys
import pygame
import random
import math
import os

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle

class Game:
    def __init__(self) -> None:
        pygame.init()

        WIDTH, HEIGHT = 1024, 768

        pygame.display.set_caption('Penguin Invasion')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH/2, HEIGHT/2), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((WIDTH/2, HEIGHT/2))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'large_decor': load_images('tiles/large_decor'),
            'grass': load_images('tiles/grass'),
            'clouds': load_images('clouds'),
            'back_trees': load_image('trees.png'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=30),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=8),
            'player': load_image('entities/player.png'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=45),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=4),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (11, 16))
        self.rect = pygame.Rect(50, 50, 17, 16)

        self.tilemap = Tilemap(self, tile_size=16)
        
        self.level = 0
        self.load_level(self.level)

        self.screenshake = 0

    def load_level(self, lvl_id):
        self.tilemap.load('data/maps/' + str(lvl_id) + '.json')

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.rect_pos.x = spawner['pos'][0]
                self.player.rect_pos.y = spawner['pos'][1]
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (11, 16)))
        
        self.dead = 0
        self.particles = []
        self.collided = 0
        self.transition = -30
        self.level_ended = False
        self.wait_time = 0


    def run(self):
        while True:
            self.display.fill((0, 0, 0, 0))
            self.display_2.fill((118,206,217))

            self.clouds.update()
            self.clouds.render(self.display_2)

            self.display_2.blit(self.assets['back_trees'], (0, 260))
            self.display_2.blit(self.assets['back_trees'], (256, 260))
            self.display_2.blit(self.assets['back_trees'], (0, 220))
            self.display_2.blit(self.assets['back_trees'], (256, 220))

            self.screenshake = max(0, self.screenshake - 1)

            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 50:
                    self.load_level(self.level)

            self.tilemap.render(self.display)

            pygame.draw.rect(self.display, (255, 0, 0), self.rect)

            if self.player.rect_pos.colliderect(self.tilemap.end_tile()):
                pygame.draw.rect(self.display, (0, 255, 0), self.rect)
                self.level_ended = True

            if self.level_ended:
                self.wait_time += 1
            
            if self.wait_time > 40:
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)

            if self.transition < 0:
                self.transition += 1

            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display)
                if kill:
                    self.particles.remove(particle)

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap)
                enemy.render(self.display)

                # if player collide with enemy, player die
                if self.player.rect_pos.colliderect(enemy.rect_pos):
                    self.collided += 1

            if self.collided == 1:
                self.dead += 1
                self.screenshake = max(25, self.screenshake)
                for num in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 3
                    self.particles.append(Particle(self, 'particle', self.player.rect_pos.center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.collided += 1

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and not self.level_ended:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.jump()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 10)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            self.display_2.blit(self.display, (0, 0))

            screenshake_offset = (random.random() * self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)
            pygame.display.update()
            self.clock.tick(60)
Game().run()