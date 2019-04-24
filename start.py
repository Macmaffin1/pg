import os

WIDTH = 1280
HEIGHT = 960
os.environ['SDL_VIDEO_CENTERED'] = '1'

import pygame
import random
from pygame.locals import *

# https://itch.io/tags

pygame.init()

BOUNDS = (0, 0, WIDTH, HEIGHT)
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('New Game')

clock = pygame.time.Clock()

textures = {
    'grass_left': pygame.image.load('images/Tiles/Grass/land_grass03.png').convert(),
    'grass_right': pygame.image.load('images/Tiles/Grass/land_grass05.png').convert(),
    'road_left': pygame.image.load('images/Tiles/Asphalt road/road_asphalt21.png').convert(),
    'road_center': pygame.image.load('images/Tiles/Asphalt road/road_asphalt22.png').convert(),
    'road_right': pygame.image.load('images/Tiles/Asphalt road/road_asphalt23.png').convert(),
    'car': pygame.image.load('images/Cars/car_blue_1.png').convert_alpha(),
    'tree_small': pygame.image.load('images/Objects/tree_small.png').convert_alpha(),
    'rock1': pygame.image.load('images/Objects/rock1.png').convert_alpha(),
    'rock2': pygame.image.load('images/Objects/rock2.png').convert_alpha(),
    'rock3': pygame.image.load('images/Objects/rock3.png').convert_alpha(),
}

car_x = (WIDTH - textures['car'].get_width()) // 2
car_y = HEIGHT - textures['car'].get_height()
car_width = textures['car'].get_width()
car_height = textures['car'].get_height()
speed_x = 4.5
speed_y = 2.5
speed_y_delta_up = speed_y / 20
speed_y_delta_down = speed_y / 10
max_amount_rocks = 20

trees = []
rocks = []
rock_keys = ['rock1', 'rock2', 'rock3']

offset = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
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
    if keys[K_UP]:
        speed_y += speed_y_delta_up
    if keys[K_DOWN]:
        speed_y = max(1, speed_y - speed_y_delta_down)

    car_x += x * speed_x
    car_x = max(car_x, 128 + 30)
    car_x = min(car_x, WIDTH - 128 - 30 - textures['car'].get_width())

    # камни
    if random.random() < 0.01 and len(rocks) < max_amount_rocks:
        scale = random.randint(60, 100) / 100
        key = random.choice(rock_keys)
        bounds = textures[key].get_size()
        rocks.append({
            'x': random.randint(128, WIDTH - 128 - bounds[0]),
            'y': -bounds[1],
            'image': key,
            'width': int(bounds[0] * scale),
            'height': int(bounds[1] * scale),
        })

    # деревья
    if random.random() < 0.01:
        scale = random.randint(60, 100) / 100
        bounds = textures['tree_small'].get_size()
        trees.append({
            'x': random.randint(-30, 30) if random.random() > 0.5 else WIDTH - bounds[0] + random.randint(-30, 30),
            'y': -bounds[1],
            'image': 'tree_small',
            'width': int(bounds[0] * scale),
            'height': int(bounds[1] * scale),
        })

    # дорога
    for y in range(-5, 10):
        left = 128
        right = WIDTH - 128
        parts = WIDTH // 128
        display.blit(textures['grass_left'], (128 * 0, 128 * y + offset))
        display.blit(textures['road_left'], (128 * 1, 128 * y + offset))

        for i in range(2, parts - 2):
            display.blit(textures['road_center'], (128 * i, 128 * y + offset))

        display.blit(textures['road_right'], (WIDTH - 128 * 2, 128 * y + offset))
        display.blit(textures['grass_right'], (WIDTH - 128, 128 * y + offset))

    display.blit(textures['car'], (car_x, car_y))

    # двигаем деревья
    to_remove_trees = []
    for tree in trees:
        if tree['y'] > HEIGHT:
            to_remove_trees.append(tree)
            continue

        tree['y'] += speed_y
        # display.blit(textures[tree['image']], (tree['x'], tree['y']))
        display.blit(
            pygame.transform.scale(textures[tree['image']], (tree['width'], tree['height'])),
            (tree['x'], tree['y'])
        )

    # удаляем деревья за экраном
    for tree in to_remove_trees:
        trees.remove(tree)

    # камни
    to_remove_rocks = []
    for rock in rocks:
        if rock['y'] > HEIGHT:
            to_remove_rocks.append(rock)
            continue

        rock['y'] += speed_y

        display.blit(
            pygame.transform.scale(textures[rock['image']], (rock['width'], rock['height'])),
            (rock['x'], rock['y'])
        )

        # проверим столкновения с камнями
        if Rect((rock['x'], rock['y'], rock['width'], rock['height'])).colliderect(
                (car_x, car_y, car_width, car_height)):
            print('dead')

    # удаляем камни за экраном
    for rock in to_remove_rocks:
        rocks.remove(rock)

    offset += speed_y
    pygame.display.update()

    if offset > 128:
        offset -= 128

    clock.tick(100)
