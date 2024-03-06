import pygame
import json

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,


}

CLOSEST_TILES_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass'}

class Tile:
    def __init__(self, type: str, variant: int, pos) -> None:
        self.type = type
        self.variant = variant
        self.pos = tuple((int(pos[0]), int(pos[1])))

        # Handling spelling mistakes for redundant strings
        self.tile_dict = {'type': self.type, 'variant': self.variant, 'pos': self.pos}
    
    # Make Tile class subscriptable
    def __getitem__(self, key):
        return self.tile_dict[key]
    
    def set_variant(self, new_variant):
        self.variant = new_variant
        self.tile_dict['variant'] = new_variant
    
    def __json__(self):
        return self.tile_dict

# Implementing JSON encoder for custom objects
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tile):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj)

class Tilemap:
    def __init__(self, game, tile_size=16) -> None:
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} # this will have physics and pos is in gird
        self.offgrid_tiles=[] # this will not have physics and pos is in pixels
        

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in CLOSEST_TILES_OFFSETS:
            # adding all the closest tiles to the base loc so we end up with 9 tiles around in that area
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1]) + '.0'
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def save(self, path):
        f = open(path, 'w')
        # Convert data to JSON 
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f, cls=CustomEncoder)
        f.close

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                # get tile position on x and y and multiply it by tile size to get pixel coordinates 
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1]) + '.0' 
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in PHYSICS_TILES) and (neighbors in AUTOTILE_MAP):
                try:
                    #Update JSON file
                    tile['variant'] = AUTOTILE_MAP[neighbors]
                except:
                    pass
                try:
                    # When there is no JSON file do this
                    tile.set_variant(AUTOTILE_MAP[neighbors])
                except:
                    pass
    
    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos']))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
        
        
