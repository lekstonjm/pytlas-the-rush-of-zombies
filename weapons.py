from .loot import Loot

class Weapon(Loot):    
    def __init__(self):
        Loot.__init__(self)
        self.attack_level = 1
    def use(self, game, zombi_name):
        pass
    def reload(self, game):        
        pass
    def pickedup_by(self, player):
        player.weapon = self

class ContactWeapon(Weapon):
    def __init__(self):
        Weapon.__init__(self)

    def use(self, game, zombi_name, message_handler):
        zombie = None
        if zombi_name:
            zombie = game.zombies_pack.get_first(zombi_name)        
        if zombie and zombie.state == zombie.CONTACT:
            message_handler.on_hit(self.name)
            zombie.damage(self.attack_level, game.agent)
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
    def use(self, game, zombi_name = None):
        zombie = None
        if zombi_name:
            zombie = game.zombies_pack.get_first(zombi_name)        
        if zombie:
            if self.use_number > self.use_limit :
                game.agent.answer(self.out_of_ammo_message)
            else:
                self.use_number += 1
                zombie.damage(self.attack_level)
                game.agent.answer(self.hit_message)
        else:
            game.agent.answer(self.miss_message)
    def reload(self, game):
        self.use_number = 0
        game.agent.answer(self.reload_message)
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
        self.attack = 2

class Katana(ContactWeapon):
    def __init__(self):
        ContactWeapon.__init__(self)
        self.name = "Katana"
        self.attack = 3

class Crossbow(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "Crossbow"
        self.attack = 1
        self.use_limit = 1

class Revolver(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "Revolver"
        self.attack = 3
        self.use_limit = 6


class Pistol(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "Pistol"
        self.attack = 2
        self.use_limit = 15


class Shootgun(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "Shootgun"
        self.attack = 4
        self.use_limit = 2



