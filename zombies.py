from random import random, randint
from datetime import datetime

class Zombie(object):
    def __init__(self, name, description, slowness, attack_rate, attack_level, defense_level):
        object.__init__(self)
        self.MOVING = 0
        self.CONTACT = 1
        self.name = name
        self.description = description
        self.time_reference = datetime.now()
        self.slowness = slowness
        self.attack_rate = attack_rate
        self.attack_level = attack_level
        self.defense_level = defense_level
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

    
class BoozoTheClown(Zombie):
    def __init__(self):
        Zombie.__init__(self, "Boozo", "The decayed clown",
                        5.0, 5.0, random()*3.0 + 1.0, 1.0)


class MikeThePoliceman(Zombie):
    def __init__(self):
        Zombie.__init__(
            self, "Mike", "The policeman witout jaw", 4.0, 4.0, 1.0, 2.0)


class BobTheFat(Zombie):
    def __init__(self):
        Zombie.__init__(
            self, "Bob", "The fat wet guy coming from sewer", 8.0, 4.0, 10.0, 2.0)

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
        Zombie.__init__(
            self, "Kristal", "The cheerleader with glue-like eyes and hanging arms", 4.0, 3.0, 1.0, 1.0)


class JulienTheGeek(Zombie):
    def __init__(self):
        Zombie.__init__(self, "Julien", "The creepy geek", 8.0, 1.0, 1.0, 1.0)


class CarlTheRunner(Zombie):
    def __init__(self):
        Zombie.__init__(
            self, "Carl", "The runner who wears a hoodie", 2.0, 5.0, 1.0, 1.0)
