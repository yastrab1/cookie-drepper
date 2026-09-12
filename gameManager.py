from enum import Enum
class UpgradeType(Enum):
    DREPY = 1
    KLIKY = 2
    JUMPING = 3
    ANGLICAKY = 4
    BRUSAKY = 5


upgrades: dict = {upgrade:1 for upgrade in UpgradeType}
unlockedUpgrades = [UpgradeType.DREPY]


def costToUpgrade(level:int):
    return 1000*level**2

def levelMultiplier(level:int):
    return 10*level

money = 0
golden = False
goldenStart = -1

