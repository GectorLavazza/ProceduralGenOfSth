import noise

from settings import *
from load_image import load_image

class Map:
    def __init__(self, screen: pygame.surface.Surface, seed, center):
        self.scale = 10.0
        self.octaves = 5
        self.persistence = 0.55
        self.lacunarity = 5

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.seed = seed

        self.array = self.get_array()
        self.tiles = self.get_tiles(self.array)

        self.default_surface = self.get_surface(self.tiles, self.array)
        self.surface = self.get_surface(self.tiles, self.array)

        self.rect = self.surface.get_rect()
        self.rect.center = center
        self.pos = self.rect.topleft

        self.center = center

        self.speed = 3
        self.edge_threshold = screen_width // 5

        self.dx = 0
        self.dy = 0
        self.dynamic_speed_x = 0
        self.dynamic_speed_y = 0
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt):
        self.screen.blit(self.surface, self.pos)
        self.check_mouse_edges()
        self.move(dt)

    def check_mouse_edges(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.dx = 0
        self.dy = 0

        if mouse_x < self.edge_threshold:
            self.dx = 1

            distance_to_edge = self.edge_threshold - mouse_x
            self.dynamic_speed_x = distance_to_edge / self.edge_threshold

        elif mouse_x > screen_width - self.edge_threshold:
            self.dx = -1

            distance_to_edge = mouse_x - (
                        screen_width - self.edge_threshold)
            self.dynamic_speed_x = distance_to_edge / self.edge_threshold

        if mouse_y < self.edge_threshold:
            self.dy = 1

            distance_to_edge = self.edge_threshold - mouse_y
            self.dynamic_speed_y = distance_to_edge / self.edge_threshold

        elif mouse_y > screen_height - self.edge_threshold:
            self.dy = -1

            distance_to_edge = mouse_y - (
                        screen_height - self.edge_threshold)

            self.dynamic_speed_y = distance_to_edge / self.edge_threshold

    def move(self, dt):
        input_direction = pygame.Vector2(self.dx, self.dy)
        if input_direction.length() > 0:
            input_direction = input_direction.normalize()

        speed_multiplier_x = max(0,
                                 min(1, self.dynamic_speed_x))
        speed_multiplier_y = max(0,
                                 min(1, self.dynamic_speed_y))

        self.velocity.x = input_direction.x * self.speed * speed_multiplier_x * dt
        self.velocity.y = input_direction.y * self.speed * speed_multiplier_y * dt

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        self.rect.x = max(self.screen_rect.width - self.rect.width,
                          min(self.rect.x, 0))
        self.rect.y = max(self.screen_rect.height - self.rect.height,
                          min(self.rect.y, 0))

        self.pos = self.rect.topleft

    def get_array(self):
        array = []
        for y in range(MAP_HEIGHT):
            row = []
            for x in range(MAP_WIDTH):

                noise_value = noise.pnoise2(
                    (x + self.seed) / self.scale, (y + self.seed) / self.scale,
                    octaves=self.octaves,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity,
                    repeatx=1024, repeaty=1024
                ) + 0.5

                if noise_value < 0:
                    noise_value = 0
                elif noise_value > 1:
                    noise_value = 1

                row.append(noise_value)

            array.append(row)

        return array

    def get_tiles(self, array):
        tiles = []

        for y in range(MAP_HEIGHT):
            row = []

            for x in range(MAP_WIDTH):
                noise_value = array[y][x]

                if noise_value < 0.3:
                    tile = '1'
                elif noise_value < 0.5:
                    tile = '2'
                elif noise_value < 0.7:
                    tile = '3'
                else:
                    tile = '4'

                row.append(tile)

            tiles.append(row)

        return tiles

    def get_surface(self, tiles, array):
        w, h = TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT
        surface = pygame.surface.Surface((w, h)).convert_alpha()

        for y in range(h // TILE_SIZE):
            for x in range(w // TILE_SIZE):

                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    tile = tiles[y][x]

                    surface.blit(load_image(tile), (x * TILE_SIZE, y * TILE_SIZE))

        return surface

    def get_corners(self, rect: pygame.Rect):
        corners = [rect.topleft, rect.topright,
                   rect.bottomleft, rect.bottomright]

        return corners

    def get_sides(self, rect: pygame.Rect):
        top = [(rect.topleft[0] + i, rect.topleft[1]) for i in
               range(rect.top // 2 + 1)]
        bottom = [(rect.bottomleft[0] + i, rect.bottomleft[1]) for i in
                  range(rect.top // 2 + 1)]
        right = [(rect.topright[0], rect.topright[1] + i) for i in
                 range(rect.left // 2 + 1)]
        left = [(rect.topleft[0], rect.topleft[1] + i) for i in
                range(rect.left // 2 + 1)]

        res = top + bottom + right + left

        return res
