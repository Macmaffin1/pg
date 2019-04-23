import pygame
from pygame.locals import *
from helpers import *

SCREENRECT = Rect(0, 0, 640, 480)
SCORE = 0


class Player(pygame.sprite.Sprite):
    speed = 1
    life = 4
    images = []
    pos = [0, 0, 0, 0]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.pos = [self.rect[0], self.rect[1], self.rect[2], self.rect[3]]

    def move(self, x, y):
        self.pos[0] += x * self.speed
        self.pos[1] += y * self.speed
        self.rect[0] = self.pos[0]
        self.rect[1] = self.pos[1]
        # self.rect.move_ip(x * self.speed, y * self.speed)


def start():
    pygame.init()

    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    img = load_image('intro_ball.gif')
    Player.images = [img, pygame.transform.flip(img, 1, 0)]

    pygame.display.set_caption('Pygame Aliens')
    pygame.mouse.set_visible(0)

    # create the background, tile the bgd image
    bgdtile = load_image('background.gif')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    all_groups = pygame.sprite.RenderUpdates()
    Player.containers = all_groups

    player = Player()

    clock = pygame.time.Clock()

    while player.alive() and player.life:
        # get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return

        keystate = pygame.key.get_pressed()

        x, y = 0, 0
        if keystate[K_LEFT]:
            x = -1
        elif keystate[K_RIGHT]:
            x = 1
        if keystate[K_UP]:
            y = -1
        elif keystate[K_DOWN]:
            y = 1

        if keystate[K_KP_PLUS]:
            player.speed += 0.1
        elif keystate[K_KP_MINUS]:
            player.speed = max(1, player.speed - 0.1)

        player.move(x, y)

        # print(player.pos, player.speed)
        # print(player.rect)
        # print(dir(player.rect))


        # clear/erase the last drawn sprites
        all_groups.clear(screen, background)

        # update all the sprites
        all_groups.update()

        # mouse = pygame.mouse.get_pos()
        # # background.set_at(mouse, (255, 0, 0, 255))
        # background.fill((255, 0, 0, 255), (mouse[0], mouse[1], 50, 50))
        # print(background.get_at(mouse), mouse)

        # draw the scene
        dirty = all_groups.draw(screen)
        pygame.display.update(dirty)

        # mouse = pygame.mouse.get_pos()
        # # background.set_at(mouse, (255, 0, 0, 255))
        # screen.fill((255, 0, 0, 255), (mouse[0], mouse[1], 50, 50))
        # print(background.get_at(mouse), mouse)

        # pygame.display.flip()

        # cap the framerate
        # clock.tick(40)
        clock.tick(40)

    print('dead')
    pygame.time.wait(500)
    pygame.quit()


if __name__ == '__main__':
    start()
