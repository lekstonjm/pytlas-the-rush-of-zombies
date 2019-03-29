import random
from .items import *
from .weapons import *

class ItemFactory(object):
    def create_item(self):
        index = random.randint(1,5)
        if index == 1:
            return Grenade()
        else:
            return Bandage()

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


class LootFactory(object):
    def __init__(self):
        self.weapon_factory = WeaponFactory()
        self.item_factory = ItemFactory()
    
    def create_loot(self):
        number = random.randint(1,3)
        if number <= 2:
            return self.item_factory.create_item()
        else: 
            return self.weapon_factory.create_weapon()
