import pygame.display;
import time;
import pygame.color;
import pygame.locals;
import pygame.event;

pygame.display.init()
mysurface = pygame.display.set_mode(size=(110, 110), flags=0, depth=0, display=0, vsync=0)
pygame.draw.rect(mysurface, pygame.Color(0,255,255), pygame.Rect(20,20,20,20))
pygame.display.update()

while True:
    pygame.event.wait()
    pygame.event.pump()
    if pygame.key.get_pressed()[pygame.locals.K_ESCAPE]:
        break