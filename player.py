
from .weapons import Fist

class Player(object):
    def __init__(self, life):
        object.__init__(self)
        self.life = life
        self.is_dead = False
        self.weapon = None
        self.fist = Fist()
        self.item = None

    def damage(self, amount, agent):
        if self.is_dead:
            return
        self.life = self.life - amount
        agent.answer(
            'You receive {0} damage. You have {1} life left'.format(amount, self.life))
        if self.life < 0:
            self.is_dead = True
            agent.answer('You are dead ... or worse ... undead')

    def heal(self, amount, agent):
        if self.is_dead:
            return
        agent.answer(
            'You receive {0} healing. You have {1} life left'.format(amount, self.life))
        self.life = self.life + amount

    def take(self, loot, req):
        loot.pickedup_by(self)
        return req.agent.answer(req._("You just picked up {0}").format(loot.name))
