
from datetime import datetime
import random 

class RandomScheduler(object):
    def __init__(self, period_min, period_max):
        self.reference = datetime.now()
        self.period = [period_min, period_max]
        self.delay = 0
    def plan(self):
        self.reference = datetime.now()
        self.delay = (random.random() * (self.period[1] - self.period[0]) + self.period[0])
    def check(self):
        delay = (datetime.now() -self.reference).total_seconds()
        if delay > self.delay:
            return True
        else:
            return False  