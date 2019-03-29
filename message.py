from pytlas import training, translations

messages = {
  "fist":{"hit" : "baf", "miss" : "fff"},
  "knife":{"hit" : "scroutch", "miss" : "sssfffff" }, 
  "bat":{ "hit" : "PAF", "miss" : "fffouuuuuu"},
  "katana" : { "hit" : "Tchac", "miss" : "shhwwinnnng" },
  "crossbow" : { "hit" : "Chhh poc", "miss" : "sssssss", "out_of_ammo" : "clic", "reload" : "ccrrrriiii Clic"},
  "revolver" : { "hit" : "PAN", "miss" : "fffwweeeee", "out_of_ammo" : "clic", "reload" : "clic clac"},
  "pistol" : { "hit" : "pan", "miss" : "fffwweeeee", "out_of_ammo" : "clic", "reload" : "clic clac"},
  "shootgun" : { "hit" : "BAM", "miss" : "...", "out_of_ammo" : "clic", "reload" : "clic clac"},
}

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
  def __init__(self, messages, agent, traduction = None):
    object.__init__(self)
    self.messages = messages
    self.agent = agent
    if traduction == None:    
      self._ = lambda m : m
    else:  
      self._ = lambda m : traduction(m)
  def on_hit(self, weapon_name):
    self.agent.answer(self._(self.messages[weapon_name]["hit"]))
  def on_miss(self, weapon_name):
    self.agent.answer(self._(self.messages[weapon_name]["miss"])) 
  def on_zombie_contact(self, zombie_name):
    self.agent.answer(self._("Warning! {0} is on you").format(zombie_name)) 