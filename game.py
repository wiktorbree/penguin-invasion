import sys
import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self) -> None:
        pygame.init()

        WIDTH, HEIGHT = 640, 480

        pygame.display.set_caption('Penguin Invasion')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH/2, HEIGHT/2))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'large_decor': load_images('tiles/large_decor'),
            'grass': load_images('tiles/grass'),
            'clouds': load_images('clouds'),
            'back_trees': load_image('trees.png'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=20),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player': load_image('entities/player.png'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=45),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=4),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (11, 16))
        self.rect = pygame.Rect(100, 50, 17, 16)

        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.rect_pos.x = spawner['pos'][0]
                self.player.rect_pos.y = spawner['pos'][1]
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (11, 16)))


    def run(self):
        while True:
            self.display.fill((118,206,217))

            self.clouds.update()
            self.clouds.render(self.display)

            self.display.blit(self.assets['back_trees'], (0, 120))
            self.display.blit(self.assets['back_trees'], (256, 120))
            self.display.blit(self.assets['back_trees'], (0, 80))
            self.display.blit(self.assets['back_trees'], (256, 80))

            self.tilemap.render(self.display)

            pygame.draw.rect(self.display, (255, 0, 0), self.rect)

            if self.player.rect_pos.colliderect(self.rect):
                pygame.draw.rect(self.display, (0, 255, 0), self.rect)
                print('Collided')

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap)
                enemy.render(self.display)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
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

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
Game().run()