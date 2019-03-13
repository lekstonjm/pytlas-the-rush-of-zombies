import logging
from threading import Thread
import time
import datetime
import random
from uuid import uuid4
from pytlas import on_agent_created, on_agent_destroyed, training, intent, translations

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
  def __init__(self, agent_id):
    Thread.__init__(self)
    self.agent_id = agent_id
    self.next_zombie_spawn_time = datetime.now().time() + random.randint(10)
    self.exit = false
  def run(self):
    while(not self.exit):
      if datetime.now().time() > self.next_zombie_spawn_time:
        agent[self.agent_id].answer('grrrrr')
        self.next_spawn_time = datetime.now().time() + random.randint(10)
      time.sleep(0.001)
  def stop(self):
    self.exit = true

agents = {}
game = None

version = "v1.0"

@on_agent_created()
def when_an_agent_is_created(agt):
  # On conserve une référence à l'agent
  agents[agt.id] = agt

@on_agent_destroyed()
def when_an_agent_is_destroyed(agt):
  # On devrait clear les timers pour l'agent à ce moment là
  global game
  if game != None:
    game.stop()
    game = None
  pass

@intent('help')
def on_help(req):
  req.agent.answer(req._(help_en).format(version))
  return req.agent.done()

@intent('play')
def on_play(req):
  global game
  game = RushOfZombiesGame(req.agent.id)
  game.start()
  req.agent.answer(req._(help_en).format(version))
  return req.agent.done()

@intent('rush_of_zombies/quit')
def on_quit(req):
  global game
  if game != None:
    game.stop()
    game = None
  req.agent.answer(req._("Bye"))
  return req.agent.done()
