import sys
import pygame

from scripts.utils import load_image
from scripts.entities import PhysicsEntity

class Game:
    def __init__(self) -> None:
        pygame.init()

        WIDTH, HEIGHT = 640, 480

        pygame.display.set_caption('Penguin Invasion')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH/3, HEIGHT/3))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'player': load_image('entities/player.png')
        }

        self.player = PhysicsEntity(self, 'player', (50, 50), (17, 16))
        self.rect = pygame.Rect(100, 50, 17, 16)

    def run(self):
        while True:
            self.display.fill((150,200,255))

            pygame.draw.rect(self.display, (255, 0, 0), self.rect)

            if self.player.rect().colliderect(self.rect):
                pygame.draw.rect(self.display, (0, 255, 0), self.rect)

            self.player.update((self.movement[1] - self.movement[0], 0))
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
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
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