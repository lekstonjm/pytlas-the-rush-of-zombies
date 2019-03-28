from random import randint

class ItemFactory(object):
    def create_item(self):
        index = randint(1,5)
        if index == 1:
            return Grenade()
        else:
            return Bandage()

class Item(object):
    def __init__(self):
        object.__init__(self)
        self.name = ""
    def use(self, game, agent):
        pass
    

class Grenade(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "Grenade"
        self.attack_level = 10
        self.use_message = "BOOM"    

    def use(self, game, agent):
        agent.answer(self.use_message)
        for zombie in game.zombies:
            zombie.damage(self.attack_level)
            self.attack_level = self.attack_level - zombie.defense_level
                
class Bandage(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "Bandage"
        self.healing_level = 2
        self.use_message = "Frot! Frot!"    
    def use(self, game, agent):
        agent.answer(self.use_message)
        game.player.heal(self.healing_level)
