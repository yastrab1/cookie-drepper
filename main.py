import pygame
import time
from screeninfo import get_monitors

import gameManager
from constants import large_font, medium_font


class UpgradeButton:
    def __init__(self, rect: pygame.Rect, upgradeType: gameManager.UpgradeType) -> None:
        self.rect = rect
        self.upgradeType = upgradeType

    def render(self, win: pygame.Surface):
        pygame.draw.rect(win, "gray", self.rect)
        label_surf = large_font.render(self.upgradeType.name, True, "black")
        cost_surf = medium_font.render(str(gameManager.costToUpgrade(gameManager.upgrades[self.upgradeType])), True, "gold")
        label_rect = label_surf.get_rect(center=self.rect.center)
        cost_rect = cost_surf.get_rect(center=label_rect.center)
        label_rect.midtop = self.rect.midtop
        cost_rect.center = self.rect.center
        win.blit(label_surf, label_rect)
        win.blit(cost_surf, cost_rect)

    def consumeEvent(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                self.onClick()

    def onClick(self):
        upgradeLevel = gameManager.upgrades[self.upgradeType]
        cost = gameManager.costToUpgrade(upgradeLevel)
        if gameManager.money < cost:
            return

        gameManager.money -= cost
        gameManager.upgrades[self.upgradeType] += 1




def getSreenSize():
    monitors = get_monitors()
    primary = list(filter(lambda m: m.is_primary, monitors))[0]
    return primary.width, primary.height


pygame.init()
win = pygame.display.set_mode(getSreenSize())

running = True
rect = pygame.Rect(((50, 50), (300, 80)))
tlacitka: list[UpgradeButton] = []

tlacitko = UpgradeButton(rect, gameManager.UpgradeType.DREPY)
tlacitka.append(tlacitko)

while running:
    time.sleep(1 / 60)
    win.fill("white")
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        for t in tlacitka:
            t.consumeEvent(e)

    for t in tlacitka:
        t.render(win)

    pygame.display.flip()
