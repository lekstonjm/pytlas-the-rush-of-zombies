import logging
from pytlas import on_agent_created, on_agent_destroyed, training, intent, translations
from uuid import uuid4
from .game import Game 
# This entity will be shared among training data since it's not language specific

from .message import *

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
  message_handler = MessageHandler(req.agent, req._)
  message_handler.on_help(version)
  return req.agent.done()

@intent('play')
def on_play(req):
  global games
  global agents
  message_handler = MessageHandler(req.agent, req._)
  if req.agent.id in games:
    message_handler.on_game_exists()
    return req.agent.done()
  req.agent.context('the_rush_of_zombies')
  
  agent_async = agents[req.agent.id]
  message_handler = MessageHandler(agent_async, req._)

  game = Game(message_handler)
  games[req.agent.id] = game
  game.start()
  message_handler.on_welcome()
  return req.agent.done()

@intent('the_rush_of_zombies/hit')
def on_hit(req):
  global games
  message_handler = MessageHandler(req.agent, req._)
  if not req.agent.id in games:
    message_handler.on_game_already_exists()
    return req.agent.done()
  game = games[req.agent.id]

  zombie_name = req.intent.slot("zombie_name").first().value
  if zombie_name == None:
    return message_handler.on_ask_zombie_name()
  game.player_hit(message_handler, zombie_name)
  return req.agent.done()

@intent('the_rush_of_zombies/pickup')
def on_pickup(req):
  global games
  message_handler = MessageHandler(req.agent, req._)
  if not req.agent.id in games:
    message_handler.on_game_already_exists()
    return req.agent.done()
  game = games[req.agent.id]

  item_name = req.intent.slot("item_name").first().value
  if item_name == None:
    return message_handler.on_ask_item_name()
  game.player_pickup(message_handler, item_name)
  return req.agent.done()

@intent('the_rush_of_zombies/use')
def on_use(req):
  global games
  message_handler = MessageHandler(req.agent, req._)
  if not req.agent.id in games:
    message_handler.on_game_already_exists()
    return req.agent.done()
  game = games[req.agent.id]

  item_name = req.intent.slot("item_name").first().value
  if item_name == None:
    return message_handler.on_ask_item_name()
  game.player_use(message_handler, item_name)
  return req.agent.done()

@intent('the_rush_of_zombies/quit')
def on_quit(req):
  message_handler = MessageHandler(req.agent, req._)
  try:
    stop_game(req.agent.id)
  except:
    message_handler.on_unable_to_stop()
    #req.agent.answer(req._("Error: Unable to stop the game"))
  req.agent.context(None)
  message_handler.on_quit()
  #req.agent.answer(req._("Bye"))
  return req.agent.done()

