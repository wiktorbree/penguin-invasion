import sys
import pygame

class Game:
    def __init__(self) -> None:
        pygame.init()

        WIDTH, HEIGHT = 640, 480

        pygame.display.set_caption('CODE-33')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH/3, HEIGHT/3))

        self.clock = pygame.time.Clock()

        self.img = pygame.image.load('data/images/entities/player.png')
        self.img.set_colorkey((0, 0, 0))

        self.img_pos = [70, 70]
        self.movement = [False, False]

        self.rect = pygame.Rect(100, 70, 16, 16)

    def run(self):
        while True:
            self.display.fill((150,200,255))

            pygame.draw.rect(self.display, (255, 0, 0), self.rect)
            self.img_pos[0] += (self.movement[1] - self.movement[0]) * 5
            
            
            img_rect = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())

            if img_rect.colliderect(self.rect):
                pygame.draw.rect(self.display, (0,100,255), self.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.display.blit(self.img, self.img_pos)
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
Game().run()