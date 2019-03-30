from pytlas import training, translations


help_en = """
A skill that will make you shudder.
"""

@training('en')
def en_data(): return """
%[help]
  what is the rush of zombies skill

%[play]
  play to the rush of zombies

%[the_rush_of_zombies/hit]
  hit @[zombie_name]
  kill @[zombie_name]
  shoot @[zombie_name]

@[zombie_name]
  mike
  kristal
  julien

%[the_rush_of_zombies/throw]
  throw @[item_name]

%[the_rush_of_zombies/use]
  use @[item_name]

%[the_rush_of_zombies/pickup]
  pick up @[item_name]
  get @[item_name]
  take @[item_name]

@[item_name]
  bandage
  grenade
  knife

%[the_rush_of_zombies/quit]
  quit the game
"""

class MessageHandler(object):
  def __init__(self, agent, traduction = None):
    object.__init__(self)
    self.agent = agent
    if traduction == None:    
      self._ = lambda m : m
    else:  
      self._ = lambda m : traduction(m)

    self.weapon_messages = {
      "fist":{"hit" : "baf", "miss" : "fff"},
      "knife":{"hit" : "scroutch", "miss" : "sssfffff" }, 
      "bat":{ "hit" : "PAF", "miss" : "fffouuuuuu"},
      "katana" : { "hit" : "Tchac", "miss" : "shhwwinnnng" },
      "crossbow" : { "hit" : "Chhh poc", "miss" : "sssssss", "out_of_ammo" : "clic", "reload" : "ccrrrriiii Clic"},
      "revolver" : { "hit" : "PAN", "miss" : "fffwweeeee", "out_of_ammo" : "clic", "reload" : "clic clac"},
      "pistol" : { "hit" : "pan", "miss" : "fffwweeeee", "out_of_ammo" : "clic", "reload" : "clic clac"},
      "shootgun" : { "hit" : "BAM", "miss" : "...", "out_of_ammo" : "clic", "reload" : "clic clac"},
    }
    self.item_messages = {
      "bandage" : "frot frot",
      "grenade" : "BOOM"
    }
    self.zombie_message = {
      "boozo": { "description" : "The decayed clown", "spawn" : "Gggrrrr", "death" : "rrr gueuh", "attack" : "niark niark" },
      "mike": { "description" : "The policeman witout jaw", "spawn" : "Gggrrrr", "death" : "rrr gueuh", "attack" : "niark niark" },
      "bob": { "description" : "The fat wet hobo coming from sewer", "spawn" : "Gggrrrr", "death" : "rrr gueuh", "attack" : "niark niark" },
      "kristal": { "description" : "The cheerleader with glue-like eyes and hanging arms", "spawn" : "Gggrrrr", "death" : "rrr gueuh", "attack" : "niark niark" },
      "julien": { "description" : "The creepy neerd", "spawn" : "Gggrrrr", "death" : "rrr gueuh", "attack" : "niark niark" },
      "carl": { "description" : "The runner who wears a dirty hoodie", "spawn" : "Gggrrrr", "death" : "rrr gueuh", "attack" : "niark niark" },
    }
  def on_help(self, version):
    return self.agent.answer(self._(help_en).format(version))
  def on_game_exists(self):
    return self.agent.answer(self._('A game is already started'))
  def on_welcome(self):
    return self.agent.answer(self._("Don't panic! ... They are coming"))
  def on_game_already_exists(self):
    return self.agent.answer(self._('mmmm! No game is available. Start a new game')) 
  def on_hit(self, weapon_name):
    return self.agent.answer(self._(self.weapon_messages[weapon_name]["hit"]))
  def on_use(self, item_name):
    return self.agent.answer(self._(self.item_messages[item_name]))
  def on_miss(self, weapon_name):
    return self.agent.answer(self._(self.weapon_messages[weapon_name]["miss"])) 
  def on_out_of_ammo(self, weapon_name):
    return self.agent.answer(self._(self.weapon_messages[weapon_name]["out_of_ammo"]))
  def on_reload(self, weapon_name):
    return self.agent.answer(self._(self.weapon_messages[weapon_name]["reload"]))
  def on_zombie_spawn(self, zombie_name):
    return self.agent.answer(self._('{0} {1} {2}').format(self._(self.zombie_message[zombie_name]["spawn"]), zombie_name, self._( self.zombie_message[zombie_name]["description"])))
  def on_zombie_contact(self, zombie_name):
    return self.agent.answer(self._("Warning! {0} is on you").format(zombie_name)) 
  def on_zombie_damage(self, zombie_name, amount):
    return self.agent.answer(self._("{0} receive {1}").format(zombie_name, amount))
  def on_zombie_explode(self, zombie_name):
    return self.agent.answer(self._('{0} explodes throwing decayed flesh and bones around him').format(zombie_name))
  def on_zombie_bite(self, zombie_name):
    return self.agent.answer(self._('{0} is biting you, {1}').format(zombie_name, self._(self.zombie_message[zombie_name]["attack"])))
  def on_zombie_dead_again(self, zombie_name):
    return self.agent.answer(self._(self.zombie_message[zombie_name]["death"]))
  def on_pickup_failed(self, item_name):
    return self.agent.answer(self._("You don't see any {0} on the floor").format(item_name))
  def on_pickup(self, item_name):
    return self.agent.answer(self._("You just picked up {0}").format(item_name))
  def on_drop(self, item_name):
    return self.agent.answer(self._("You just droped {0}").format(item_name))
  def on_ask_zombie_name(self):
    return self.agent.ask('zombie_name',self._("Which one?"))
  def on_ask_item_name(self):
    return self.agent.ask('item_name', self._("Which one?"))
  def on_item_not_available(self, item_name):
    return self.agent.answer(self._("You don't have any {0}".format(item_name)))
  def on_loot(self, loot_name):
    return self.agent.answer(self._('{0} fell on the floor').format(loot_name))
  def on_too_late(self):
    return self.agent.answer(self._('Too late you are  ... undead'))
  def on_heal(self, amount, life):
    return self.agent.answer(self._('You receive {0} healing. You have {1} life left').format(amount, life))
  def on_player_damage(self, amount, life):
    return self.agent.answer(self._('You receive {0} damage. You have {1} life left').format(amount, life))
  def on_player_death(self):
    return self.agent.answer(self._('You are dead ... or worse ... undead'))
 
  def on_unable_to_stop(self):
    return self.agent.answer(self._("Error: Unable to stop the game"))
  def on_quit(self):
    return self.agent.answer(self._("Bye"))
