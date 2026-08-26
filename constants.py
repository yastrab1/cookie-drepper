import pygame
from screeninfo import get_monitors

from gameManager import UpgradeType

pygame.font.init()
small_font = pygame.font.Font("LobsterTwo-Regular.ttf", 18)
medium_font = pygame.font.Font("LobsterTwo-Regular.ttf", 24)
large_font = pygame.font.Font("LobsterTwo-Regular.ttf", 32)
huge_font = pygame.font.Font("LobsterTwo-Regular.ttf", 100)

keybind_to_upgrade = {"k": UpgradeType.KLIKY, "j": UpgradeType.JUMPING, "a": UpgradeType.ANGLICAKY,
                      "b": UpgradeType.BRUSAKY, 'd': UpgradeType.DREPY}

#TODO settle on real constants
exercise_multipliers = {
    UpgradeType.KLIKY: 1.1,
    UpgradeType.JUMPING: 1.2,
    UpgradeType.ANGLICAKY: 1.3,
    UpgradeType.BRUSAKY: 1.4,
    UpgradeType.DREPY: 1.5
}
button_rect = pygame.Rect(((0, 0), (300, 100)))



drepy_rect, kliky_rect, jumping_rect, anglicaky_rect, brusaky_rect = [button_rect.copy() for _ in range(5)]


def getSreenSize():
    monitors = get_monitors()
    primary = list(filter(lambda m: m.is_primary, monitors))[0]
    return primary.width, primary.height

screen_width, screen_height = getSreenSize()

drepy_rect.center = (screen_width//4, 6*screen_height//8)
kliky_rect.center = (2*screen_width//4, 6*screen_height//8)
jumping_rect.center = (3*screen_width//4, 6*screen_height//8)
anglicaky_rect.center = (screen_width//3, 7*screen_height//8)
brusaky_rect.center = (2*screen_width//3, 7*screen_height//8)

upgrade_button_positions = {
    UpgradeType.KLIKY: kliky_rect,
    UpgradeType.JUMPING: jumping_rect,
    UpgradeType.ANGLICAKY: anglicaky_rect,
    UpgradeType.BRUSAKY: brusaky_rect,
    UpgradeType.DREPY: drepy_rect
}
input_rect = pygame.Rect((0,0),(screen_width//2,100))
input_rect.center=(screen_width//2, screen_height//10)

