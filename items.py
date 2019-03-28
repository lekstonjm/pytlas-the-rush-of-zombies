from .loot import Loot

class Item(Loot):
    def __init__(self):
        Loot.__init__(self)
    def use(self, game, agent):
        pass
    
    def pickedup_by(self, player):
        player.item = self
    

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
