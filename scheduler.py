
from datetime import datetime
import random 

class RandomScheduler(object):
    def __init__(self, period_min, period_max):
        self.reference = datetime.now()
        self.period_min = period_min
        self.period_max = period_max
        self.delay = 0
    def plan(self, now = False):
        self.reference = datetime.now()
        if now:
            self.delay = 0
        else:
            self.delay = (random.random() * (self.period_min - self.period_max) + self.period_min)
    def check(self):
        delay = (datetime.now() -self.reference).total_seconds()
        if delay > self.delay:
            return True
        else:
            return False  