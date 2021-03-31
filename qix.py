from pygame.constants import K_x
import pygame.display;
import time;
import pygame.color;
import pygame.locals;
import pygame.event;
import sys

pygame.display.init()
fps = 30
fpsclock=pygame.time.Clock()
mysurface = pygame.display.set_mode(size=(800, 600), flags=0, depth=0, display=0, vsync=0)
pygame.display.update()

x = 10
y = 10
incr = 10
neato = pygame.Rect(x,y,10,10)
pygame.draw.rect(mysurface, pygame.Color(0,255,255),neato)

running = True
while running:
    fpsclock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    keys = pygame.key.get_pressed()
    neato.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * incr
    neato.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * incr

    mysurface.fill(0)
    pygame.draw.rect(mysurface, pygame.Color(0,255,255),neato)
    pygame.display.flip()
