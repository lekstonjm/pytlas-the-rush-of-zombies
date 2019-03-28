import random
from .weapons import *

class WeaponFactory(object):
    def create_weapon(self):
        index = random.randint(1,8)
        if index == 1:
            return Knife()
        elif index == 2:
            return BaseballBat()
        elif index == 3:
            return Katana()
        elif index == 4:
            return Crossbow()
        elif index == 5:
            return Revolver()
        elif index == 6:
            return Pistol()
        elif index == 7:
            return Shootgun()