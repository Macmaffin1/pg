import os

WIDTH = 1280
HEIGHT = 960
os.environ['SDL_VIDEO_CENTERED'] = '1'

import pygame
from pygame.locals import *

pygame.init()

BOUNDS = (0, 0, WIDTH, HEIGHT)
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('New Game')

clock = pygame.time.Clock()

textures = {
    'car': pygame.image.load('images/Cars/car_blue_1.png').convert_alpha(),
}

while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            exit()

    pygame.display.update()

    clock.tick(10)
