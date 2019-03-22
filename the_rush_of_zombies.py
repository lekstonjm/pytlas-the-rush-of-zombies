import logging
from pytlas import on_agent_created, on_agent_destroyed, training, intent, translations
from uuid import uuid4
from .game import Game 
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

%[rush_of_zombies/hit]
  hit @[zombie_name]
  kill @[zombie_name]
  shoot @[zombie_name]

@[zombie_name]
  Mike
  Kristal
  Julien

%[rush_of_zombies/throw]
  throw @[item_name]

%[rush_of_zombies/use]
  use @[item_name]

%[rush_of_zombies/pickup]
  pick up @[item_name]
  loot [@item_name]
  get [@item_name]

@[item_name]
  bandage
  grenade
  knife

%[rush_of_zombies/quit]
  quit the game
"""

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
  game = Game(agents[req.agent.id])
  games[req.agent.id] = game
  game.start()
  req.agent.answer(req._('Don\'t panic! ... They are coming'))
  return req.agent.done()

@intent('rush_of_zombies/quit')
def on_quit(req):
  try:
    stop_game(req.agent.id)
  except:
    req.agent.answer(req._("Error: Unable to stop the game"))
  req.agent.answer(req._("Bye"))
  return req.agent.done()
