import threading
import time
import random
from datetime import datetime
from .zombies import ZombieFactory
from .weapons import WeaponFactory

class Player(object):
  def __init__(self, life):
    object.__init__(self)
    self.life = life
    self.is_dead = False
    self.weapon = None

  def damage(self, amount,agent):
    if self.is_dead: return
    self.life = self.life - amount
    agent.answer('You receive {0} damage. You have {1} life left'.format(amount, self.life))
    if self.life < 0:
      self.is_dead = True
      agent.answer('You are dead ... or worse ... undead')
    
  def heal(self, amount, agent):
    if self.is_dead : return
    agent.answer('You receive {0} healing. You have {1} life left'.format(amount, self.life))
    self.life = self.life + amount
  
class ZombiePack(object):
    def __init__(self):
        self.zombies = []

    def add(self, zombie):
        self.zombies.append(zombie)

    def get_first(self, zombie_name):
        for zombie in self.zombies:
            if zombie.name == zombie_name:
                return zombie

    def update(self, game):
        burried = []
        for zombie in self.zombies:
            if zombie.dead_again:
                burried.append(zombie)
            else:
                zombie.update(game.player, game.agent)
        for zombie in burried:
            self.zombies.remove(zombie)

class Scheduler(object):
    def __init__(self, period_min, period_max):
        self.reference = datetime.now()
        self.period = [period_min, period_max]
        self.delay = 0
    def plan(self):
        self.reference = datetime.now()
        self.delay = (random.random() * (self.period[1] - self.period[0]) + self.period[0])
    def check(self):
        delay = (datetime.now() -self.reference).total_seconds()
        if delay > self.delay:
            return True
        else:
            return False    

class ZombieSpawner(object):
    def __init__(self):
        self.wanderer = Scheduler(5,10)
        self.pack = Scheduler(20,30)
        self.wanderer.plan()
        self.pack.plan()
        self.pack_size = 5.0
    
    def update(self, game):
        if self.pack.check():
            self.spawn_pack(game, self.pack_size)
            self.pack.plan()
            self.wanderer.plan()
        if self.wanderer.check():
            self.spawn_wanderer(game)
            self.wanderer.plan()
    
    def spawn_wanderer(self, game):
        zombie = game.zombie_factory.spawn_zombie()
        game.zombies_pack.add(zombie)
        game.agent.answer('{0} {1} {2}'.format(zombie.spawn_message, zombie.name, zombie.description))
    
    def spawn_pack(self, game, pack_size):
        for _index in range(pack_size):
            self.spawn_wanderer(game)

class Game(threading.Thread):
    def __init__(self, agent):
        threading.Thread.__init__(self)
        self.agent = agent
        self.loop = True
        self.zombie_factory = ZombieFactory()
        self.weapon_factory = WeaponFactory()
        self.zombies_pack = ZombiePack()
        self.zombies_spawner = ZombieSpawner()
        self.player = Player(20)

    def stop(self):
        self.loop = False

    def run(self):
        while(self.loop):
            if not self.player.is_dead:
                self.zombies_pack.update(self)
                self.zombies_spawner.update(self)
            time.sleep(1.0)


