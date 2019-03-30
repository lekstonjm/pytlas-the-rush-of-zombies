class Loot(object):
    def __init__(self):
        object.__init__(self)
        self.name = ""

    def pickedup_by(self, message_handler, player):
        pass

    def use(self, message_handler, game, target_name = None):
        pass
