import threading
import time
import random
from datetime import datetime
from .zombies import ZombieFactory, ZombiePack, ZombieSpawner
from .weapons import WeaponFactory
from .items import ItemFactory

class LootFactory(object):
    def __init__(self):
        self.weapon_factory = WeaponFactory()
        self.item_factory = ItemFactory()
    
    def create_loot(self):
        number = random.randint(1,2)
        if number == 1:
            return self.item_factory.create_item()
        else: 
            return self.weapon_factory.create_weapon()

class Player(object):
  def __init__(self, life):
    object.__init__(self)
    self.life = life
    self.is_dead = False
    self.weapon = None
    self.item = None

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
  
class Floor(object):
    def __init__(self):
        self.drop = []
        self.drop_timeout = 10
    
    def add(self, item):
        self.drop.append([datetime.now(), item])

    def pickup_first(self, item_name):
        for item in self.drop:
            if item[1].name == item_name:
                self.drop.remove(item)
                return item[1]                

    def update(self):
        removed_items = []
        for item in self.drop:
            if (datetime.now() - item[0]).total_seconds() > self.drop_timeout:
                removed_items.append(item)
        for removed_item in removed_items:
            self.drop.remove(removed_item)
  

class Game(threading.Thread):
    def __init__(self, agent):
        threading.Thread.__init__(self)
        self.agent = agent
        self.loop = True
        self.loot_factory = LootFactory()
        self.zombies_pack = ZombiePack()
        self.zombies_spawner = ZombieSpawner()
        self.player = Player(20)
        self.floor = Floor()

    def stop(self):
        self.loop = False

    def on_loot(self):
        self.floor.add(self.loot_factory.create_loot())

    def run(self):
        while(self.loop):
            if not self.player.is_dead:
                self.zombies_pack.update(self)
                self.zombies_spawner.update(self)
            time.sleep(1.0)


