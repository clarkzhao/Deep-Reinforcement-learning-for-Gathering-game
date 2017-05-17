# Set how many rows and columns we will have
ROW_COUNT = 12
COLUMN_COUNT = 36

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 1

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

# The time in second for the collected apple to recover
RESPOWN_TIME = 1

# Digits in the grid
EMPTY = 0
PLAYER = 1
FRONT_OF_PLAYER = -1
APPLE = 2
OPPONENT = 3


# The diamond size of the apple
SIZE_APPLE = 4

# Direction of the player
UP = 0
DOWN = 2
LEFT = 3
RIGHT = 1


