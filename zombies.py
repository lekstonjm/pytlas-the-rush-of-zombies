from random import random, randint
from datetime import datetime
from .scheduler import RandomScheduler

class ZombieSpawner(object):
    def __init__(self):
        self.wanderer = RandomScheduler(30,40)
        self.pack = RandomScheduler(60,120)
        self.zombies_limit = 2
        self.wanderer.plan(True)
        self.pack.plan()
        self.pack_size = 5
        self.zombie_factory = ZombieFactory()
    
    def update(self, message_handler, game):
        if len(game.zombies_pack.zombies) >= self.zombies_limit:
            return
        if self.pack.check():
            self.spawn_pack(message_handler, game, self.pack_size)
            self.pack.plan()
            self.wanderer.plan()
        elif self.wanderer.check():
            self.spawn_wanderer(message_handler, game)
            self.wanderer.plan()
    
    def spawn_wanderer(self,message_handler, game):
        zombie = self.zombie_factory.spawn_zombie()
        game.zombies_pack.add(zombie)
        message_handler.on_zombie_spawn(zombie.name)
        #game.agent.answer('{0} {1} {2}'.format(zombie.spawn_message, zombie.name, zombie.description))
    
    def spawn_pack(self, message_handler, game, pack_size):
        for _index in range(pack_size):
            self.spawn_wanderer(message_handler, game)


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
        self.time_reference = datetime.now()
        self.slowness = 0
        self.attack_rate = 0
        self.attack_level = 0
        self.defense_level = 0
        self.state = self.MOVING
        self.dead_again = False

    def update(self, message_handler, game):
        if self.dead_again:
            return
        delay = (datetime.now() - self.time_reference).total_seconds()
        if (self.state == self.MOVING):
            if (delay > self.slowness):
                message_handler.on_zombie_contact(self.name)
                self.state = self.CONTACT
                self.time_reference = datetime.now()
        elif (self.state == self.CONTACT):
            if (delay > self.attack_rate):
                message_handler.on_zombie_bite(self.name)
                #agent.answer('{0} is biting you'.format(self.name))
                game.player.damage(message_handler, self.attack_level)
                self.time_reference = datetime.now()

    def damage(self, message_handler, amount):
        message_handler.on_zombie_damage(self.name, amount)
        if self.defense_level <= amount:
            message_handler.on_zombie_dead_again(self.name)
            self.dead_again = True

    
class BoozoTheClown(Zombie):
    def __init__(self):
        Zombie.__init__(self)
        self.name = "boozo"
        self.slowness = 5.0
        self.attack_rate = 5.0
        self.attack_level = randint(1,3)
        self.defense_level = 1.0


class MikeThePoliceman(Zombie):
    def __init__(self):
        Zombie.__init__(self)
        self.name = "mike"
        self.slowness = 4.0
        self.attack_rate = 4.0
        self.attack_level = 1.0
        self.defense_level = 2.0


class BobTheFat(Zombie):
    def __init__(self):
        Zombie.__init__(self)
        self.name = "bob"
        self.slowness = 8.0
        self.attack_rate = 4.0
        self.attack_level = 8.0
        self.defense_level = 2.0

    def update(self, message_handler, game):
        delay = (datetime.now() - self.time_reference).total_seconds()
        if (self.state == self.MOVING):
            if (delay > self.slowness):
                message_handler.on_zombie_explode(self.name)
                game.player.damage(message_handler, self.attack_level)
                self.dead_again = True


class KristalTheCheerleders(Zombie):
    def __init__(self):
        Zombie.__init__(self)
        self.name = "kristal"
        self.slowness = 4.0
        self.attack_rate = 3.0
        self.attack_level = 1.0
        self.defense_level = 1.0

class JulienTheGeek(Zombie):
    def __init__(self):
        Zombie.__init__(self)
        self.name = "julien"
        self.slowness = 8.0
        self.attack_rate = 1.0
        self.attack_level = 1.0
        self.defense_level = 1.0

class CarlTheRunner(Zombie):
    def __init__(self):
        Zombie.__init__(self)
        self.name = "carl"
        self.slowness = 2.0
        self.attack_rate = 5.0
        self.attack_level = 1.0
        self.defense_level = 1.0