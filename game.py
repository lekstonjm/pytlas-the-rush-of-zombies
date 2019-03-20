import threading
import time
import random
from datetime import datetime
from .zombies import ZombieFactory
from .weapons import Pistol

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


class Game(threading.Thread):
    def __init__(self, agent):
        threading.Thread.__init__(self)
        self.agent = agent
        self.loop = True
        self.zombie_factory = ZombieFactory()
        self.zombies_pack = ZombiePack()
        self.plan_zombie_spawn()
        self.player = Player(20)

    def stop(self):
        self.loop = False

    def run(self):
        while(self.loop):
            if not self.player.is_dead:
                self.zombies_pack.update(self)
                self.spawn_zombie()
            time.sleep(1.0)

    def spawn_zombie(self):
        if self.check_zombie_spawn():
            zombie = self.zombie_factory.spawn_zombie()
            self.zombies_pack.add(zombie)
            self.agent.answer('grrrrr! Mike the chocked wet zombie is coming')
            self.plan_zombie_spawn()

    def plan_zombie_spawn(self):
        self.zombie_spawn_date_reference = datetime.now()
        self.zombie_spawn_delay = (random.random() * 10.0 + 1)

    def check_zombie_spawn(self):
        current_delay = (datetime.now() -
                         self.zombie_spawn_date_reference).total_seconds()
        if current_delay > self.zombie_spawn_delay:
            return True
        else:
            return False
