import pygame
import time

pygame.init()
win = pygame.display.set_mode((1920,1200))
font = pygame.font.Font("LobsterTwo-Regular.ttf",100)
running = True
rect = pygame.Rect(((50,50),(150,40)))
peniazteky = 0

while running:
    time.sleep(1/60)
    win.fill("black")
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running= False
        if e.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            if rect.collidepoint(x,y):
                peniazteky += 1

    peniazteky_surf = font.render(str(peniazteky),True,'orange')
    win.blit(peniazteky_surf,rect.topright)
    pygame.draw.rect(win, "gray", rect)

    pygame.display.flip()