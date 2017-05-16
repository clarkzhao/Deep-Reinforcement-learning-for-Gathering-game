"""
Game Gathering: a simple 2D grid world game
originally proposed by Joel & Vinicius et al. in the paper of
Multi-agent Reinforcement Learning in Sequential Social Dilemmas
"""
import arcade
import numpy as np
import player
import constant
import apple


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

        self.grid = np.zeros([constant.ROW_COUNT, constant.COLUMN_COUNT], 'int8')
        self.player = None
        self.apples = []
        self.total_time = 0.0

    def setup(self):
        self.player = player.Player(0, 0)
        center_row = int(constant.ROW_COUNT/2)-1
        center_col = int(constant.COLUMN_COUNT/2)-1
        center_point = np.array([center_row, center_col])
        self.add_apples(size=constant.SIZE_APPLE,
                        start=center_point-constant.SIZE_APPLE+1)
        self.total_time = 0.0

        arcade.set_background_color(arcade.color.BLACK)

    def add_apples(self, size=3, start=np.array([0, 0])):
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
                row = top[0] - idx
                col = start[1] + size - 1 - idx + i
                self.apples.append(apple.Apple(row, col))
        for idx in range(size - 1, -1, -1):
            for i in range(idx * 2 + 1):
                row = start[0] + idx
                col = start[1] + size - 1 - idx + i
                self.apples.append(apple.Apple(row, col))

    def update(self, dt):
        """ Move everything """
        self.total_time += dt

        self.player.move()

        self.grid.fill(0)
        for apple in self.apples:
            # Check if there is any apple can be respawn
            if apple.is_collected:
                if self.total_time - apple.collected_time \
                        >= constant.RESPOWN_TIME:
                    apple.respawn()

            # Mark apples in the grid
            if not apple.is_collected:
                self.grid[apple.row][apple.col] = constant.APPLE

        if self.check_apple(self.player.row, self.player.col):
            self.collect_apple(self.player.row, self.player.col)

        self.grid[self.player.row][self.player.col] = constant.PLAYER

    def check_apple(self, row, col):
        """Check if a apple is collected"""
        if self.grid[row][col] == constant.APPLE:
            return True
        else:
            return False

    def collect_apple(self, row, col):
        for apple in self.apples:
            if apple.row == row and apple.col == col:
                apple.get_collected(self.total_time)
                self.player.get_reward()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the grid
        for row in range(constant.ROW_COUNT):
            for column in range(constant.COLUMN_COUNT):
                # Figure out what color to draw the box
                if self.grid[row][column] == constant.PLAYER:
                    color = arcade.color.BLUE
                elif self.grid[row][column] == constant.APPLE:
                    color = arcade.color.GREEN
                else:
                    color = arcade.color.BLACK

                # Do the math to figure out where the box is
                x = (constant.MARGIN + constant.WIDTH) * column + constant.MARGIN + constant.WIDTH // 2
                y = (constant.MARGIN + constant.HEIGHT) * row + constant.MARGIN + constant.HEIGHT // 2

                # Draw the box
                arcade.draw_rectangle_filled(x, y, constant.WIDTH, constant.HEIGHT, color)

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
    window = Gathering(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)
    window.setup()
    arcade.run()

main()
