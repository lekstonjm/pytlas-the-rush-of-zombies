import threading
import time
import random
from datetime import datetime
from .zombies import ZombieFactory, ZombieSpawner
from .player import Player
from .loot_factory import LootFactory

class Floor(object):
    def __init__(self):
        self.drop = []
        self.drop_timeout = 10
    
    def add(self, item):
        self.drop.append([datetime.now(), item])

    def pickup_first(self, item_name):
        for item in self.drop:
            if item[1].name.lower() == item_name.lower():
                self.drop.remove(item)
                return item[1]                
        return None

    def update(self):
        removed_items = []
        for item in self.drop:
            if (datetime.now() - item[0]).total_seconds() > self.drop_timeout:
                removed_items.append(item)
        for removed_item in removed_items:
            self.drop.remove(removed_item)
  

class ZombiePack(object):
    def __init__(self):
        self.zombies = []

    def add(self, zombie):
        self.zombies.append(zombie)

    def get_first(self, zombie_name):
        for zombie in self.zombies:
            if zombie.name.lower() == zombie_name.lower():
                return zombie
        return None

    def update(self, message_handler, game):
        burried = []
        for zombie in self.zombies:
            if zombie.dead_again:
                burried.append(zombie)
                loot = game.loot_factory.create_loot()
                message_handler.on_loot(loot.name)
                #self.agent.answer('{0} fell on the floor'.format(loot.name))
                game.floor.add(loot)
            else:
                zombie.update(message_handler, game)
        for zombie in burried:
            self.zombies.remove(zombie)


class Game(threading.Thread):
    def __init__(self, message_handler):
        threading.Thread.__init__(self)
        self.message_handler_thread = message_handler
        self.loop = True
        self.loot_factory = LootFactory()
        self.zombies_pack = ZombiePack()
        self.zombies_spawner = ZombieSpawner()
        self.player = Player(20)
        self.floor = Floor()

    def stop(self):
        self.loop = False

    def player_hit(self, message_handler, zombie_name):
        return self.player.hit(message_handler, self, zombie_name)
    
    def player_pickup(self, message_handler, loot_name):
        return self.player.pickup(message_handler, self, loot_name)

    def player_use(self, message_handler, item_name):
        return self.player.use(message_handler, self, item_name)        

    def run(self):
        message_handler = self.message_handler_thread
        self.message_handler_thread = None
        while(self.loop):
            if not self.player.is_dead:
                self.zombies_pack.update(message_handler, self)
                self.zombies_spawner.update(message_handler, self)
            time.sleep(1.0)


