from random import randint

class WeaponFactory(object):
    def create_weapon(self):
        index = randint(1,7)

class Knife(object):
    def __init__(self):
        object.__init__(self)
        self.name = "Knife"
        self.attack = 1
        self.is_distant = False

    def hit(self, zombie, agent):
        if zombie.state == zombie.CONTACT:
            zombie.damage(self.attack)
            agent.answer('scroutch! ...')
        else:
            agent.answer('ffffffwit...')

    def reload(self, zombie, agent):
        pass


class BaseballBat(object):
    def __init__(self):
        object.__init__(self)
        self.attack = 2
        self.is_distant = False

    def hit(self, zombie, agent):
        if zombie.state == zombie.CONTACT:
            zombie.damage(self.attack)
            agent.answer('PAF! ...')
        else:
            agent.answer('ffffffwit...')

    def reload(self, zombie, agent):
        pass


class Katana(object):
    def __init__(self):
        object.__init__(self)
        self.attack = 3
        self.is_distant = False

    def hit(self, zombie, agent):
        if zombie.state == zombie.CONTACT:
            zombie.damage(self.attack)
            agent.answer('Tchac! ...')
        else:
            agent.answer('ffffffwit...')

    def reload(self, zombie, agent):
        pass


class Revolver(object):
    def __init__(self):
        object.__init__(self)
        self.attack = 2
        self.is_distant = True
        self.number = 0
        self.limit = 6

    def hit(self, zombie, agent):
        if (self.number < self.limit):
            self.number = self.number + 1
            zombie.damage(self.attack)
            agent.answer('PAN! ...')
        else:
            agent.answer('click!')

    def reload(self, zombie, agent):
        self.number = 0
        agent.answer('click clack!')


class Pistol(object):
    def __init__(self):
        object.__init__(self)
        self.attack = 2
        self.is_distant = True
        self.number = 0
        self.limit = 15

    def hit(self, zombie, agent):
        if (self.number < self.limit):
            self.number = self.number + 1
            zombie.damage(self.attack)
            agent.answer('PAN! ...')
        else:
            agent.answer('click!')

    def reload(self, zombie, agent):
        self.number = 0
        agent.answer('click clack!')


class Shootgun(object):
    def __init__(self):
        object.__init__(self)
        self.attack = 4
        self.is_distant = True
        self.number = 0
        self.limit = 2

    def hit(self, zombie, agent):
        if (self.number < self.limit):
            self.number = self.number + 1
            zombie.damage(self.attack)
            agent.answer('BAM! ...')
        else:
            agent.answer('click!')

    def reload(self, zombie, agent):
        self.number = 0
        agent.answer('click clack!')


class Grenade(object):
    def __init__(self):
        object.__init__(self)
        self.attack = 10
        self.is_distant = True
        self.number = 0
        self.limit = 1

    def hit(self, zombie, agent):
        if (self.number < self.limit):
            self.number = self.number + 1
            zombie.damage(self.attack)
            agent.answer('BAM! ...')
        else:
            agent.answer('click!')

    def reload(self, zombie, agent):
        self.number = 0
        agent.answer('click clack!')
