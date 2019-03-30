from .loot import Loot

class Item(Loot):
    def __init__(self):
        Loot.__init__(self)

    def use(self, message_handler, player, game, target_name = None):
        message_handler.on_use(self.name)
        player.item = None

    def pickedup_by(self, message_handler, player):
        if player.item != None:
            message_handler.on_drop(player.item.name)
        player.item = self

class Grenade(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "grenade"
        self.attack_level = 10

    def use(self, message_handler,player, game, target_name = None):
        Item.use(self, message_handler, player, game, target_name)
        for zombie in game.zombies:
            zombie.damage(message_handler, self.attack_level)
            self.attack_level = self.attack_level - zombie.defense_level
                
class Bandage(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "bandage"
        self.healing_level = 2

    def use(self, message_handler, player, game, target_name = None):
        Item.use(self, message_handler, player, game, target_name)
        player.heal(message_handler, self.healing_level)
