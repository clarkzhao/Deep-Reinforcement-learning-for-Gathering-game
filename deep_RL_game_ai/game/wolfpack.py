from .environment import *
from .player import *

class EnvironmentWolfpack(EnvironmentBase):
    def __init__(self, config):
        super(EnvironmentWolfpack, self).__init__(config)
        self.prey = None

    def new_episode(self):
        self.time_watch.reset()
        self.grid.create_grid()
        # Generate two random players as wolves
        for point in self.grid.generate_random_player_position(num_player=3):
            self.player_list.append(Player(point))
        idx = 0
        for player in self.player_list:
            self.grid.place_player(player)
            player.new_episode()
            player.idx = idx
            idx += 1

        # self.current_action = None
        self.is_game_over = False
        self.get_observation()


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

        # Update the beam area
        if player.using_beam:
            self.grid.place_beam_area(player)
            # Check if the player is hit by the beam
            for possible_player in self.player_list:
                if self.grid.is_in_beam_area(possible_player.position):
                    if not possible_player.is_tagged:
                        # print("Hit by beam!!!")
                        possible_player.get_hit(self.time_watch.time())
                        # print("number of hit:", possible_player.num_hit_by_beam)
                    if possible_player.is_tagged:
                        self.grid.clear_player(possible_player)

    def move(self, player: Player):
        """
        In this method, the player is moved to the next position it should be 
        Any reward and beam detection is happened here
        """


        # if the next position is the wall
        # the player is forced back to the current position
        if self.grid[player.next_position] in [CellType.WALL]:
            player.next_position = player.position

        if self.grid[player.next_position] in [CellType.PLAYER]:
            for prey in self.player_list:
                if prey.position == player.next_position:
                    if not prey.is_prey:
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

        # Check if the player is about to hunt the prey
        for prey in self.player_list:
            if player.idx != prey.idx:
                if prey.is_prey and prey.position == player.position and not player.is_tagged:
                    # print("Player", player.idx, ", prey is hunted")
                    self.is_game_over = True
                    prey.is_tagged = True
                    self.grid.clear_player(prey)

    # def convert_view(self):
    #     """Convert the player cells in grid to different colours"""
    #     self.view_array = self.grid.copy_cells()
    #     for player in self.player_list:
    #         if not player.is_tagged:
    #             if player.is_prey:
    #                 self.view_array[player.position.y, player.position.x] = CellType.PLAYER
    #             else:
    #                 self.view_array[player.position.y, player.position.x] = CellType.OPPONENT