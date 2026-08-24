import pygame
import time

class Button:
    def __init__(self,rect:pygame.Rect, onClick) -> None:
        self.rect = rect
        self.onClick = onClick

    def render(self,win:pygame.Surface):
        pygame.draw.rect(win, "gray", self.rect)

    def consumeEvent(self,event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x,y):
                self.onClick()


def yayy():
    print("yay")

pygame.init()
win = pygame.display.set_mode((1440,960))
font = pygame.font.Font("LobsterTwo-Regular.ttf",100)
running = True
rect = pygame.Rect(((50,50),(150,40)))
tlacitka:list[Button] = []

tlacitko = Button(rect,yayy)
tlacitka.append(tlacitko)
peniazteky = 0

while running:
    time.sleep(1/60)
    win.fill("black")
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running= False
        for t in tlacitka:
            t.consumeEvent(e)


    peniazteky_surf = font.render(str(peniazteky),True,'orange')
    win.blit(peniazteky_surf,rect.topright)
    

    pygame.display.flip()

