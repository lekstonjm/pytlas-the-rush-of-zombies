from .loot import Loot

class Weapon(Loot):    
    def __init__(self):
        Loot.__init__(self)
        self.attack_level = 1
        self.hit_message = ""
        self.miss_message = ""
    def use(self, game, zombi_name):
        pass
    def reload(self, game):        
        pass
    def pickedup_by(self, player):
        player.weapon = self

class ContactWeapon(Weapon):
    def __init__(self):
        Weapon.__init__(self)

    def use(self, game, zombi_name):
        zombie = None
        if zombi_name:
            zombie = game.zombies_pack.get_first(zombi_name)        
        if zombie and zombie.state == zombie.CONTACT:
            zombie.damage(self.attack_level, game.agent)
            game.agent.answer(self.hit_message)
        else:
            game.agent.answer(self.miss_message)    
        
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
            zombie = game.zombies.get_first(zombi_name)        
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
        self.name = "Fist"
        self.attack_level = 1
        self.hit_message = "baf"
        self.miss_message = "chuiit"


class Knife(ContactWeapon):
    def __init__(self):
        ContactWeapon.__init__(self)
        self.name = "Knife"
        self.attack_level = 1
        self.hit_message = "scroutch"
        self.miss_message = "ffffffweet"

class BaseballBat(ContactWeapon):
    def __init__(self):
        ContactWeapon.__init__(self)
        self.name = "Bat"
        self.attack = 2
        self.hit_message = "PAF"
        self.miss_message = "fffouuuuuu"

class Katana(ContactWeapon):
    def __init__(self):
        ContactWeapon.__init__(self)
        self.name = "Katana"
        self.attack = 3
        self.hit_message = "Tchac"
        self.miss_message = "shhwwinnnng"


class Crossbow(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "Crossbow"
        self.attack = 1
        self.use_limit = 1
        self.hit_message = "Chhh poc"
        self.miss_message = "sssssss"
        self.out_of_ammo_message = "click"
        self.reload_message = "ccrrrriiii Clic"

class Revolver(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "Revolver"
        self.attack = 3
        self.use_limit = 6
        self.hit_message = "PAN"
        self.miss_message = "fffwweeeee"
        self.out_of_ammo_message = "clic"
        self.reload_message = "clic clac"


class Pistol(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "Pistol"
        self.attack = 2
        self.use_limit = 15
        self.hit_message = "pan"
        self.miss_message = "fffwweeeee"
        self.out_of_ammo_message = "clic"
        self.reload_message = "clic clac"


class Shootgun(DistantWeapon):
    def __init__(self):
        DistantWeapon.__init__(self)
        self.name = "Shootgun"
        self.attack = 4
        self.use_limit = 2
        self.hit_message = "BAM"
        self.miss_message = "..."
        self.out_of_ammo_message = "clic"
        self.reload_message = "clic clac"



