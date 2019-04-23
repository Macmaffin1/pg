import pygame
from pygame.locals import *

# https://itch.io/tags

pygame.init()

WIDTH = 128 * 6
HEIGHT = 480
BOUNDS = (0, 0, WIDTH, HEIGHT)
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('New Game')

clock = pygame.time.Clock()

# tileset = pygame.image.load('data/spritesheet_tiles.png').convert()
# textures = {
#     'test': tileset.subsurface((0, 0, 128, 128)),
#     'bg_left': tileset.subsurface((0, 0, 128, 128)),
# }

textures = {
    'grass_left': pygame.image.load('images/Tiles/Grass/land_grass03.png').convert(),
    'grass_right': pygame.image.load('images/Tiles/Grass/land_grass05.png').convert(),
    'road_left': pygame.image.load('images/Tiles/Asphalt road/road_asphalt21.png').convert(),
    'road_center': pygame.image.load('images/Tiles/Asphalt road/road_asphalt22.png').convert(),
    'road_right': pygame.image.load('images/Tiles/Asphalt road/road_asphalt23.png').convert(),
    'car': pygame.image.load('images/Cars/car_blue_1.png').convert_alpha(),
}

car_x = (WIDTH - textures['car'].get_width()) // 2
car_y = HEIGHT - textures['car'].get_height()
speed_x = 3.5
speed_y = 2.5

offset = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            exit()

    # mouse = pygame.mouse.get_pos()
    # # pygame.draw.rect(display, (255, 0, 0), (mouse[0], mouse[1], 30, 30))
    # display.fill((255, 0, 0), (mouse[0], mouse[1], 30, 30))

    keys = pygame.key.get_pressed()
    x = 0
    if keys[K_LEFT]:
        x -= 1
    if keys[K_RIGHT]:
        x += 1

    car_x += x * speed_x
    car_x = max(car_x, 128+30)
    car_x = min(car_x, WIDTH - 128 - 30 - textures['car'].get_width())

    for y in range(-5, 10):
        display.blit(textures['grass_left'], (128 * 0, 128 * y + offset))
        display.blit(textures['road_left'], (128 * 1, 128 * y + offset))
        display.blit(textures['road_center'], (128 * 2, 128 * y + offset))
        display.blit(textures['road_center'], (128 * 3, 128 * y + offset))
        display.blit(textures['road_right'], (128 * 4, 128 * y + offset))
        display.blit(textures['grass_right'], (128 * 5, 128 * y + offset))

    display.blit(textures['car'], (car_x, car_y))

    offset += speed_y

    pygame.display.update()

    clock.tick(60)
