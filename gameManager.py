from enum import Enum
class UpgradeType(Enum):
    DREPY = 1
    KLIKY = 2
    JUMPING = 3
    ANGLICAKY = 4
    BRUSAKY = 5


upgrades: dict = {upgrade:1 for upgrade in UpgradeType}

def costToUpgrade(level:int):
    return 100*level**2

def levelMultiplier(level:int):
    return level

money = 150