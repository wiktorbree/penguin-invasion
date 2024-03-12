import sys
import pygame

from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap, Tile

SCALE = 2.0

class Editor:
    def __init__(self) -> None:
        pygame.init()

        WIDTH, HEIGHT = 640, 480

        pygame.display.set_caption('LEVEL EDITOR - Penguin Invasion')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH/2, HEIGHT/2))

        self.clock = pygame.time.Clock()

        self.assets = {
            'decor': load_images('tiles/decor'),
            'large_decor': load_images('tiles/large_decor'),
            'grass': load_images('tiles/grass'),
            'spawners': load_images('tiles/spawners'),
        }

        self.tilemap = Tilemap(self, tile_size=16)

        self.tile_list = list(self.assets)
        self.tile_group = 0 # grass, decor, etc.
        self.tile_variant = 0
        
        self.left_click = False
        self.right_click = False
        self.shift = False

        self.ongrid = True

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

    def run(self):
        while True:
            self.display.fill((118,206,217))
            self.tilemap.render(self.display)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(150)

            # Mouse control
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / SCALE, mpos[1] / SCALE)
            tile_pos = (int(mpos[0] // self.tilemap.tile_size), int(mpos[1] // self.tilemap.tile_size))
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size, tile_pos[1] * self.tilemap.tile_size))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.left_click and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = Tile(self.tile_list[self.tile_group], self.tile_variant, tile_pos)
            if self.right_click:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_rect = pygame.Rect(tile['pos'][0], tile['pos'][1], tile_img.get_width(), tile_img.get_height())
                    if tile_rect.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.left_click = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append(Tile(self.tile_list[self.tile_group], self.tile_variant, mpos))
                    if event.button == 3:
                        self.right_click = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.left_click = False
                    if event.button == 3:
                        self.right_click = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
Editor().run()