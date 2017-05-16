# from constant import  *

class Apple():
    def __init__(self, row, col):

        # The position of the apple
        self.row = row
        self.col = col

        # The time when the apple is collected in seconds
        self.collected_time = 0.

        # True when the apple is collected by player
        # False when the apple is available to be collected
        self.is_collected = False

    def getCollected(self, time):
        """Called when the apple is collected by a player"""
        self.is_collected = True
        self.collected_time = time
        print("get Collected")
        print(self.collected_time)

    def respawn(self):
        """Called when the apple should be respawn"""
        self.is_collected = False
        self.collected_time = 0.
        print("Respawn")
