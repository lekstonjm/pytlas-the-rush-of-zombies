
from .weapons import Fist

class Player(object):
    def __init__(self, life):
        object.__init__(self)
        self.life = life
        self.is_dead = False
        self.weapon = None
        self.fist = Fist()
        self.item = None

    def damage(self, message_handler, amount):
        if self.is_dead:
            return
        self.life = self.life - amount
        message_handler.on_player_damage(amount, self.life)
        if self.life < 0:
            self.is_dead = True
            message_handler.on_player_death()

    def heal(self, message_handler, amount):
        if self.is_dead:
            return message_handler.render_too_late()
        self.life = self.life + amount
        message_handler.on_heal(amount, self.life)

    def pickup(self, message_handler, game, loot_name):
        loot = game.floor.pickup_first(loot_name)
        if loot == None:
            return message_handler.on_pickup_failed(loot_name)
            #return req.agent.answer(req._("You don't see any {0} on the floor").format(item_name))
        message_handler.on_pickup(loot.name)
        loot.pickedup_by(message_handler, self) 
        #return req.agent.answer(req._("You just picked up {0}").format(loot.name))

    def use (self, message_handler, game, item_name):
        if self.item == None or self.item.name != item_name:
            return message_handler.on_item_not_available(item_name)
        self.item.use(message_handler, self, game)

    def hit(self, message_handler, game, zombie_name):
        weapon = self.fist
        if self.weapon:
            weapon = self.weapon
        weapon.use(message_handler, game, zombie_name)
    