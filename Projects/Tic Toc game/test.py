
import pygame

pygame.init()
# colour

white = (255,255,255)
black = (0,0,0)
pink = (255,180,203)
blue = (173,216,230)
green = (144,238,144)
grey = (220,220,220)

#display

size = (600,600)
ds = pygame.display.set_mode(size)
ds.fill(grey)
pygame.display.set_caption('Tic Toc Game : ')
pygame.display.update()

pygame.draw.aalines(ds,black,[(81,81),(81,290)],[(181,81),(181,290)],100)
pygame.display.update()

pygame.time.delay(2000)
