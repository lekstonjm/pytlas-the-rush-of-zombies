from random import random, randint
from datetime import datetime

class ZombieFactory(object):
    def spawn_zombie(self):
        index = randint(1,6)
        if index == 1:
            return BoozoTheClown()
        elif index == 2:
            return MikeThePoliceman()
        elif index == 3:
            return BobTheFat()
        elif index == 4:
            return KristalTheCheerleders()
        elif index == 5:
            return JulienTheGeek()
        elif index == 6:
            return CarlTheRunner()

class Zombie(object):
    def __init__(self):
        object.__init__(self)
        self.MOVING = 0
        self.CONTACT = 1
        self.name = ""
        self.description = ""
        self.spawn_message = "gggrrrr"
        self.dead_again_message = "rrrggg"
        self.time_reference = datetime.now()
        self.slowness = 0
        self.attack_rate = 0
        self.attack_level = 0
        self.defense_level = 0
        self.state = self.MOVING
        self.dead_again = False

    def update(self, player, agent):
        if self.dead_again:
            return
        delay = (datetime.now() - self.time_reference).total_seconds()
        if (self.state == self.MOVING):
            if (delay > self.slowness):
                agent.answer('Warning! {0} is on you'.format(self.name))
                self.state = self.CONTACT
                self.time_reference = datetime.now()
        elif (self.state == self.CONTACT):
            if (delay > self.attack_rate):
                agent.answer('{0} is biting you'.format(self.name))
                player.damage(self.attack_level, agent)
                self.time_reference = datetime.now()

    def damage(self, amount):
        if self.defense_level < amount:
            self.dead_again = True

    
class BoozoTheClown(Zombie):
    def __init__(self):
        Zombie.__init__(self)
        self.name = "Boozo"
        self.description = "The decayed clown"
        self.slowness = 5.0
        self.attack_rate = 5.0
        self.attack_level = random()*3.0 + 1.0
        self.defense_level = 1.0


class MikeThePoliceman(Zombie):
    def __init__(self):
        Zombie.__init__()
        self.name = "Mike"
        self.description = "The policeman witout jaw"
        self.slowness = 4.0
        self.attack_rate = 4.0
        self.attack_level = 1.0
        self.defense_level = 2.0


class BobTheFat(Zombie):
    def __init__(self):
        Zombie.__init__()
        self.name = "Bob"
        self.description = "The fat wet guy coming from sewer"
        self.slowness = 8.0
        self.attack_rate = 4.0
        self.attack_level = 10.0
        self.defense_level = 2.0

    def update(self, player, agent):
        delay = (datetime.now() - self.time_reference).total_seconds()
        if (self.state == self.MOVING):
            if (delay > self.slowness):
                agent.answer(
                    '{0} explodes throwing decayed flesh and bones around him'.format(self.name))
                player.damage(self.attack_level, agent)
                self.dead_again = True


class KristalTheCheerleders(Zombie):
    def __init__(self):
        Zombie.__init__()
        self.name = "Kristal"
        self.description = "The cheerleader with glue-like eyes and hanging arms"
        self.slowness = 4.0
        self.attack_rate = 3.0
        self.attack_level = 1.0
        self.defense_level = 1.0

class JulienTheGeek(Zombie):
    def __init__(self):
        Zombie.__init__()
        self.name = "Julien"
        self.description = "The creepy geek"
        self.slowness = 8.0
        self.attack_rate = 1.0
        self.attack_level = 1.0
        self.defense_level = 1.0

class CarlTheRunner(Zombie):
    def __init__(self):
        Zombie.__init__()
        self.name = "Carl"
        self.description = "The runner who wears a hoodie"
        self.slowness = 2.0
        self.attack_rate = 5.0
        self.attack_level = 1.0
        self.defense_level = 1.0