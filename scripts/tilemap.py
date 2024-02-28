import pygame

CLOSEST_TILES_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass'}

class Tile:
    def __init__(self, type: str, variant: int, pos) -> None:
        self.type = type
        self.variant = variant
        self.pos = tuple(pos)

        # Handling spelling mistakes for redundant strings
        self.tile_dict = {'type': self.type, 'variant': self.variant, 'pos': self.pos}

class Tilemap:
    def __init__(self, game, tile_size=16) -> None:
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} # this will have physics and pos is in gird
        self.offgrid_tiles=[] # this will not have physics and pos is in pixels

        for i in range(8):
            self.tilemap[str(3 + i) + ';10'] = Tile('grass', 1, (3 + i, 10)).tile_dict
            self.tilemap['10;' + str(5 + i)] = Tile('grass', 1, (10, 5 + i)).tile_dict

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in CLOSEST_TILES_OFFSETS:

            # adding all the closest tiles to the base location so we end up with 9 tiles around in that area
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                # get tile position on x and y and multiply it by tile size to get pixel coordinates 
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos']))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
        
        
