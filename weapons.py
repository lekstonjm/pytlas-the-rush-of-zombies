from .loot import Loot

class Weapon(Loot):    
    def __init__(self):
        Loot.__init__(self)
        self.attack_level = 1
    def use(self, message_handler, game,  zombi_name):
        pass
    def reload(self, message_handler, game):        
        pass
    def pickedup_by(self, message_handler, player):
        if player.weapon != None:
            message_handler.on_drop(player.weapon.name)
        player.weapon = self

class ContactWeapon(Weapon):
    def __init__(self):
        Weapon.__init__(self)

    def use(self, message_handler, game,  zombi_name):
        zombie = None
        if zombi_name:
            zombie = game.zombies_pack.get_first(zombi_name)        
        if zombie and zombie.state == zombie.CONTACT:
            message_handler.on_hit(self.name)
            zombie.damage(message_handler, self.attack_level)
            #game.agent.answer(self.hit_message)
        else:
            message_handler.on_miss(self.name)
            #game.agent.answer(self.miss_message)    
        
class DistantWeapon(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.use_limit = 0
        self.use_number = 0    
        self.out_of_ammo_message = ""
        self.reload_message = ""

    def use(self, message_handler, game, zombi_name):
        zombie = None
        if zombi_name:
            zombie = game.zombies_pack.get_first(zombi_name)        
        if zombie:
            if self.use_number > self.use_limit :
                message_handler.on_out_of_ammo(self.name)
                #game.agent.answer(self.out_of_ammo_message)
            else:
                self.use_number += 1
                message_handler.on_hit(self.name)
                zombie.damage(message_handler, self.attack_level)
                #game.agent.answer(self.hit_message)
        else:
            message_handler.on_miss(self.name)
            #game.agent.answer(self.miss_message)
    def reload(self, message_handler, game):
        self.use_number = 0
        message_handler.on_reload(self.name)
        #game.agent.answer(self.reload_message)
        pass

class Fist(ContactWeapon):
    def __init__(self):
        ContactWeapon.__init__(self)
        self.name = "fist"
        self.attack_level = 1


class Knife(ContactWeapon):
    def __init__(self):
        ContactWeapon.__init__(self)
        self.name = "knife"
        self.attack_level = 1

class BaseballBat(ContactWeapon):
    def __init__(self):
        ContactWeapon.__init__(self)
        self.name = "bat"
        self.attack_level = 2

class Katana(ContactWeapon):
    def __init__(self):
        ContactWeapon.__init__(self)
        self.name = "Katana"
        self.attack_level = 3

class Crossbow(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "crossbow"
        self.attack_level = 1
        self.use_limit = 1

class Revolver(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "revolver"
        self.attack_level = 3
        self.use_limit = 6


class Pistol(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "pistol"
        self.attack_level = 2
        self.use_limit = 15


class Shootgun(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "shootgun"
        self.attack_level = 4
        self.use_limit = 2



