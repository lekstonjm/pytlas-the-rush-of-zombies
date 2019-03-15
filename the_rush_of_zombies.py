import time
import random
import logging
import threading
from pytlas import on_agent_created, on_agent_destroyed, training, intent, translations
from datetime import datetime
from uuid import uuid4

# This entity will be shared among training data since it's not language specific

help_en = """
A skill that will make you shudder.
"""

@training('en')
def en_data(): return """
%[help]
  what is the rush of zombies skill

%[play]
  play to the rush of zombies

%[rush_of_zombies/quit]
  quit the game
"""

class Knife(object):
  def __init__(self):
    object.__init__(self)
    self.attack = 1
    self.is_distant = False
  def hit(self, zombie, agent):
    if zombie.state == zombie.CONTACT:
      zombie.damage(self.attack)
      agent.answer('scroutch! ... grrreu')
    else:
      agent.answer('ffffffwit...')
  def reload(self, zombie, agent):
    pass

class Pistol(object):
  def __init__(self):
    object.__init__(self)
    self.attack = 1
    self.is_distant = True
    self.number = 0
    self.limit = 2
  def hit(self, zombie, agent):
    if (self.number < self.limit):
      self.number = self.number + 1
      zombie.damage(self.attack)
      agent.answer('PAN! ... grrreu')
    else:
      agent.answer('click!')

  def reload(self, zombie, agent):
    self.number = 0
    agent.answer('click clack!')


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

class Zombie(object):
  def __init__(self, name, speed, attack_speed, attack , defense, loot):
    object.__init__(self)
    self.MOVING = 0
    self.CONTACT = 1
    self.name = name
    self.reference = datetime.now()
    self.speed = speed
    self.attack_speed = attack_speed
    self.attack = attack
    self.defense = defense
    self.loot = loot
    self.state = self.MOVING
    self.is_overkilled = False
  def update(self, player, agent):
    if self.is_overkilled: return
    if (self.state == self.MOVING):
      delay = (datetime.now() - self.reference).total_seconds()
      if (delay > self.speed):
        self.reference = datetime.now()
        self.state = self.CONTACT
    elif (self.state == self.CONTACT):
      delay = (datetime.now() - self.reference).total_seconds()
      if (delay > self.attack_speed):        
        agent.answer('{0} is biting you'.format(self.name))
        player.damage(self.attack, agent)
        self.reference = datetime.now()        
  def damage(self, amount):
    if self.defense < amount:
      self.is_overkilled = True

class RushOfZombiesGame(threading.Thread):
  def __init__(self, agent):
    threading.Thread.__init__(self)
    self.agent =  agent
    self.loop = True
    self.plan_zombie_spawn()
    self.zombies = []
    self.player = Player(20)

  def stop(self):  
    self.loop = False

  def run(self):
    while(self.loop):
      if not self.player.is_dead:
        self.update_zombies()
        self.spawn_zombie()        
      time.sleep(1.0)

  def update_zombies(self):
    overkilled_zombies = []
    for zombie in self.zombies:
      if zombie.is_overkilled:
        overkilled_zombies.append(zombie)
      else:
        zombie.update(self.player, self.agent)
    for overkilled_zombie in overkilled_zombies:
      self.zombies.remove(overkilled_zombie)

  def spawn_zombie(self):
      if self.check_zombie_spawn():
        zombie = Zombie("Mike", 4, 1, 3, 0, Pistol())
        self.zombies.append(zombie)
        self.agent.answer('grrrrr! Mike the chocked wet zombie is coming')
        self.plan_zombie_spawn()

  def plan_zombie_spawn(self):
    self.zombie_spawn_date_reference = datetime.now() 
    self.zombie_spawn_delay =  (random.random() * 10.0 + 1)
  
  def check_zombie_spawn(self):
    current_delay = (datetime.now() - self.zombie_spawn_date_reference).total_seconds() 
    if  current_delay > self.zombie_spawn_delay:
      return True
    else:
      return False
  

agents =  {}
games = {}

version = "v1.0"

stop_timeout = 1.0

def stop_game(agt_id):
  global games
  global stop_timeout
  game = games.pop(agt_id, None)
  if game != None:  
    game.stop()
    game.join(stop_timeout)    
    if game.is_alive():
      raise Exception('game thread frozen')


@on_agent_created()
def when_an_agent_is_created(agt):
  # On conserve une référence à l'agent
  global agents
  agents[agt.id] = agt


@on_agent_destroyed()
def when_an_agent_is_destroyed(agt):
  # On devrait clear les timers pour l'agent à ce moment là
  global agents  
  stop_game(agt.id)
  agents.pop(agt.id, None)
  
@intent('help')
def on_help(req):
  req.agent.answer(req._(help_en).format(version))
  return req.agent.done()

@intent('play')
def on_play(req):
  global games
  global agents
  if req.agent.id in games:
    req.agent.answer(req._('A game is already started'))
    return req.agent.done()
  req.agent.context('rush_of_zombies')
  game = RushOfZombiesGame(agents[req.agent.id])
  games[req.agent.id] = game
  game.start()
  req.agent.answer(req._('Don\'t be afraid ... They are coming'))
  return req.agent.done()

@intent('rush_of_zombies/quit')
def on_quit(req):
  try:
    stop_game(req.agent.id)
  except:
    req.agent.answer(req._("Error: Unable to stop the game"))
  req.agent.answer(req._("Bye"))
  return req.agent.done()
