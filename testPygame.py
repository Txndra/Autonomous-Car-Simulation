import pygame
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode([640,600])

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    window.fill([0,0,255])
    pygame.draw.rect(window, (255,10,10), Rect((100,300), (20,30)))

    pygame.display.update()


