import abc
from abc import abstractmethod

import pygame
import time

import animations
import constants
import gameManager
from animations import AnimationManager
from constants import large_font, medium_font, keybind_to_upgrade, exercise_multipliers


class UIComponent(abc.ABC):

    @abstractmethod
    def render(self, win: pygame.Surface):
        pass

    @abstractmethod
    def consumeEvent(self, event: pygame.event.Event):
        pass


class UpgradeButton(UIComponent):
    def __init__(self, rect: pygame.Rect, upgradeType: gameManager.UpgradeType) -> None:
        self.rect = rect
        self.upgradeType = upgradeType

    def render(self, win: pygame.Surface):
        pygame.draw.rect(win, "gray", self.rect)
        label_surf = large_font.render(self.upgradeType.name, True, "black")
        cost_surf = medium_font.render(str(gameManager.costToUpgrade(gameManager.upgrades[self.upgradeType])), True,
                                       "gold")
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

        gameManager.setMoney(gameManager.money - cost)
        gameManager.upgrades[self.upgradeType] += 1


class InputBox(UIComponent):
    def __init__(self, rect: pygame.Rect,manager:AnimationManager) -> None:
        self.rect = rect
        self.currentlyTyping = 0
        self.animation_manager = manager

    def render(self, win: pygame.Surface):
        pygame.draw.rect(win, "darkgray", self.rect)
        currently_typing_surf = large_font.render(str(self.currentlyTyping), True, "black")
        currently_typing_rect = currently_typing_surf.get_rect(center=self.rect.center)
        currently_typing_rect.center = self.rect.center
        win.blit(currently_typing_surf, currently_typing_rect)

    def consumeEvent(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            name = pygame.key.name(event.key)
            if name.isdecimal():
                self.currentlyTyping *= 10
                self.currentlyTyping += int(name)
            if name == "backspace":
                self.currentlyTyping = int(self.currentlyTyping / 10)
            if name in keybind_to_upgrade.keys():
                upgrade_type = keybind_to_upgrade[name]
                upgrade_level = gameManager.upgrades[upgrade_type]
                money_gain = (exercise_multipliers[upgrade_type] * self.currentlyTyping
                              * gameManager.levelMultiplier(upgrade_level))
                self.animation_manager.uranium_pellet_animations(int(money_gain))
                gameManager.setMoney(money_gain + gameManager.money)
                self.currentlyTyping = 0


pygame.init()

win = pygame.display.set_mode((constants.screen_width, constants.screen_height),pygame.FULLSCREEN)

running = True

components: list[UIComponent] = []

animation = AnimationManager()

for upgrade_type in gameManager.UpgradeType:
    components.append(UpgradeButton(constants.upgrade_button_positions[upgrade_type], upgrade_type))
input = InputBox(constants.input_rect,animation)
components.append(input)
while running:
    time.sleep(1 / 60)
    win.fill("white")
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        for t in components:
            t.consumeEvent(e)

    money = constants.huge_font.render(f"{int(gameManager.display_money)}", True, "black")
    money_rect = money.get_rect(center=(constants.screen_width // 2, constants.screen_height//2))
    win.blit(money, money_rect)
    for t in components:
        t.render(win)
    animation.render(win)

    pygame.display.flip()
