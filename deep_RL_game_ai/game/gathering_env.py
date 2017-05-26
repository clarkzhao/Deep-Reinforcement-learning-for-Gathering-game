from .base_env import *

class EnvironmentGathering(EnvironmentBase):

    def __init__(self, config):
        super(EnvironmentGathering, self).__init__(config)
        self.apple_list = []

    def new_episode(self):
        """Reset the environment and begin a new episode"""
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
        # self.current_action = None
        self.is_game_over = False
        self.generate_apples()
        self.grid.place_apples(self.apple_list)


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
        is valid
        """
        # Clear the cell for the beam
        # self.grid.clear_beam_area()

        if not player.is_tagged:

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

        # Update the beam area
        if player.using_beam:
            self.grid.place_beam_area(player)
            # Check if the player is hit by the beam
            for possible_player in self.player_list:
                if self.grid.is_in_beam_area(possible_player.position):
                    if not possible_player.is_tagged:
                        print("Hit by beam!!!")
                        possible_player.get_hit(self.time_watch.time())
                        print("number of hit:", possible_player.num_hit_by_beam)
                    if possible_player.is_tagged:
                        self.grid.clear_player(possible_player)


    def move(self, player: Player):
        """
        In this method, the player is moved to the next position it should be 
        Any reward and beam detection is happened here
        """

        # If any apple can be respawn?
        for apple in self.apple_list:
            if apple.is_collected:
                if self.time_watch.time() - apple.collected_time \
                            >= GameSetting.APPLE_RESPAWN_TIME:
                    apple.respawn()

        # If any player can be respawn?
        for possible_player in self.player_list:
            if possible_player.is_tagged:
                if self.time_watch.time() - possible_player.tagged_time \
                            >= GameSetting.TAGGED_TIME:
                    possible_player.respawn()
                    self.grid.place_player(possible_player)

        # if the next position is the wall
        # the player is forced back to the current position
        if self.grid[player.next_position] in [CellType.WALL, CellType.PLAYER]:
            player.next_position = player.position

        # if the next position is outside the 2D grid
        # the player is forced to be on the edge of the grid
        if player.next_position.x < 0:
            player.next_position.x = 0
        elif player.next_position.x >= self.grid.width:
            player.next_position.x = self.grid.width - 1
        if player.next_position.y < 0:
            player.next_position.y = 0
        elif player.next_position.y >= self.grid.width:
            player.next_position.y = self.grid.height - 1

        # Update the grid to correct Celltype
        self.update_grid(player)

        # Check if the player is about to collect any apple
        for apple in self.apple_list:
            if not apple.is_collected and apple.position == player.position and not player.is_tagged:
                apple.get_collected(self.time_watch.time())
                player.apple_eaten += 1
                print("Player", player.idx, ", Apple eaten:", player.apple_eaten)
