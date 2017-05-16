"""
Game Gathering: a simple 2D grid world game
originally proposed by Joel & Vinicius et al. in the paper of
Multi-agent Reinforcement Learning in Sequential Social Dilemmas
"""
import arcade
import numpy as np
from player import *
from constant import  *
from apple import *
class Gathering(arcade.Window):
    """
    main environment for the game Gathering
    """
    def __init__(self, width, height):
        """
        set up the game
        :param width: the screen width
        :param height: the screen height
        """
        super().__init__(width, height)

        self.grid = np.zeros([ROW_COUNT,COLUMN_COUNT],'int8')
        self.player = None
        self.apples = []
        self.total_time = 0.0


        # self.set_update_rate(10.)

    def setup(self):
        self.player = Player(0,0)
        self.apples.append(Apple(10,0))
        self.apples.append(Apple(8,0))
        self.total_time = 0.0

        arcade.set_background_color(arcade.color.BLACK)

    def update(self, dt):
        """ Move everything """
        self.total_time += dt

        self.player.move()

        self.grid.fill(0)
        # print(self.apples.Collected)
        # print(self.apples.collected_time)
        for apple in self.apples:

            # Check if there is any apple can be respawn
            if apple.is_collected:
                if self.total_time - apple.collected_time \
                        >= RESPOWN_TIME:
                    apple.respawn()

            #Mark apples in the grid
            if not apple.is_collected:
                self.grid[apple.row][apple.col] = APPLE

        if self.check_apple(self.player.row,self.player.col):
            self.collect_apple(self.player.row,self.player.col)

        self.grid[self.player.row][self.player.col] = PLAYER

    def check_apple(self, row, col):
        """Check if a apple is collected"""
        if self.grid[row][col] == APPLE:
            return True
        else:
            return False

    def collect_apple(self, row, col):
        for apple in self.apples:
            if apple.row == row and apple.col==col:
                apple.getCollected(self.total_time)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the grid
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Figure out what color to draw the box
                if self.grid[row][column] == PLAYER:
                    color = arcade.color.BLUE
                elif self.grid[row][column] == APPLE:
                    color = arcade.color.GREEN
                else:
                    color = arcade.color.BLACK

                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                # Draw the box
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def on_key_press(self, key, modifiers):
        """
        Called whenever the kep is pressed.
        """
        if key == arcade.key.UP:
            self.player.delta_row = 1
        elif key == arcade.key.DOWN:
            self.player.delta_row = -1
        elif key == arcade.key.LEFT:
            self.player.delta_col = -1
        elif key == arcade.key.RIGHT:
            self.player.delta_col = 1

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.delta_row = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.delta_col = 0

def main():
    window = Gathering(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()

main()