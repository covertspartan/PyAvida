__author__ = 'covertar'

from time import time

class cContext:


    def __init__(self, seed = time()):
        import random
        self.random = random.Random()

        self.random.seed(seed)
