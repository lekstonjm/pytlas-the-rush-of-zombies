import time
import random
import logging
from pytlas import on_agent_created, on_agent_destroyed, training, intent, translations
from threading import Thread
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

class RushOfZombiesGame(Thread):
  def __init__(self, agent):
    Thread.__init__(self)
    self.agent = agent
    self.exit = False
    self.zombie_spawn_delay = 10.0
    self.zombie_spawn_date_reference = datetime.now()
    self.plan_zombie_spawn()
  def run(self):
    while(not self.exit):
      if self.check_zombie_spawn():
        self.agent.answer('grrrrr')
        self.plan_zombie_spawn()
      time.sleep(0.005)
  def stop(self):
    self.exit = True
  def plan_zombie_spawn(self):
    self.zombie_spawn_date_reference = datetime.now() 
    self.zombie_spawn_delay =  (random.random() * 10.0 + 1)
  def check_zombie_spawn(self):
    if (datetime.now() - self.zombie_spawn_date_reference).total_seconds() > self.zombie_spawn_delay:
      return True
    else:
      return False


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


#@on_agent_created()
#def when_an_agent_is_created(agt):
  # On conserve une référence à l'agent


@on_agent_destroyed()
def when_an_agent_is_destroyed(agt):
  # On devrait clear les timers pour l'agent à ce moment là
  stop_game(agt.id)
    

@intent('help')
def on_help(req):
  req.agent.answer(req._(help_en).format(version))
  return req.agent.done()

@intent('play')
def on_play(req):
  global games
  if req.agent.id in games:
    req.agent.answer(req._('A game is already started'))
    return req.agent.done()
  game = RushOfZombiesGame(req.agent)
  games[req.agent.id] = game
  game.start()
  req.agent.answer(req._('Don\'t be afraid'))
  return req.agent.done()

@intent('rush_of_zombies/quit')
def on_quit(req):
  try:
    stop_game(agt.id)
  except:
    req.agent.answer(req._("Error: Unable to stop the game"))
  req.agent.answer(req._("Bye"))
  return req.agent.done()
