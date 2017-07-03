from .environment import *

class EnvironmentGathering(EnvironmentBase):

    def __init__(self, config):
        super(EnvironmentGathering, self).__init__(config)
        self.apple_list = []

    def new_episode(self):
        """Reset the environment and begin a new episode"""
        self.player_list = []
        self.apple_list = []
        self.time_watch.reset()
        self.grid.create_grid()
        # self.stats.reset()
        for point in self.grid.find_player():
            self.player_list.append(Player(point))
        idx = 1
        for player in self.player_list:
            self.grid.place_player(player)
            player.new_episode()
            player.idx = idx
            idx += 1
        self.generate_apples()
        self.grid.place_apples(self.apple_list)

        # self.current_action = None
        self.is_game_over = False
        self.get_observation()


    def generate_apples(self, size=3, start=np.array([4,14])):
        """
        add apples of the diamond shape with given size
        :param size: the size of diamond
        :param start: the starting point of the diamond in 
                        the left-bottom corner
        :return: the added apple
        """
        l = size * 2 - 1
        top = start + l - 1
        for idx in range(size - 1):
            for i in range(idx * 2 + 1):
                y = top[0] - idx
                x = start[1] + size - 1 - idx + i
                self.apple_list.append(Apple(Point(x, y)))
        for idx in range(size - 1, -1, -1):
            for i in range(idx * 2 + 1):
                y = start[0] + idx
                x = start[1] + size - 1 - idx + i
                self.apple_list.append(Apple(Point(x, y)))

    def update_grid(self, player: Player):
        """
        In this method, we assume the next position/direction of the player
        is valid and the player and apples will be placed on the grid
        """

        # Clear the cell for the front of the player
        if self.grid[player.current_front] == CellType.PLAYER_FRONT:
            self.grid[player.current_front] = CellType.EMPTY

        # Clear the cell for the current position of the player
        self.grid[player.position] = CellType.EMPTY

        # Move the player
        player.move()

        # Place the player in the new position
        self.grid.place_player(player)

        # Place the apples
        self.grid.place_apples(self.apple_list)

    def move(self, player: Player):
        """
        In this method, the player is moved to the next position it should be 
        Any reward and beam detection is happened here
        """
        self.respawn_apples()
        self.respawn_player()
        if not player.is_tagged:
            self.put_player_back(player)

        # Update the grid to correct Celltype
            self.update_grid(player)
            self.check_if_using_beam(player)
            self.collect_apple(player)
        self.get_observation()
        # self.update_beam_area()

    def respawn_apples(self):
        """
        the valid apple will be respawn in this method
        """
        for apple in self.apple_list:
            if apple.is_collected:
                if self.time_watch.time() - apple.collected_time \
                            >= GameSetting.APPLE_RESPAWN_TIME:
                    apple.respawn()

    def collect_apple(self, player):
        """
        check if the player is about to collect any apple
        """
        # A flag for the player collecting any apple
        eaten_any_apple = False
        for apple in self.apple_list:
            if not apple.is_collected and apple.position == player.position and not player.is_tagged:
                apple.get_collected(self.time_watch.time())
                player.apple_eaten += 1
                player.reward = 1
                eaten_any_apple = True
        if not eaten_any_apple:
            player.reward = 0
