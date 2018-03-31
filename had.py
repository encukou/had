import random

class State:
    """Object holding the whole state of a snake game"""

    def __init__(self):
        self.width = 10
        self.height = 10
        self.food = []
        self.speed = 1/10

        self.snake_alive = True
        self.snake_coords = [(0, 0), (1, 0)]
        self.snake_direction = 1, 0
        self.snake_queued_directions = []

    def __str__(self):
        rows = []
        for i in range(self.height):
            row = []
            for i in range(self.width):
                row.append('.')
            rows.append(row)
        for x, y in self.snake_coords:
            rows[y][x] = 'X'

        if self.snake_direction == (1, 0):
            rows[y][x] = '>'
        elif self.snake_direction == (-1, 0):
            rows[y][x] = '<'
        elif self.snake_direction == (0, 1):
            rows[y][x] = '^'
        elif self.snake_direction == (0, -1):
            rows[y][x] = 'v'

        for x, y in self.food:
            rows[y][x] = '!'
        return '\n'.join(' '.join(row) for row in reversed(rows))

    def move(self):
        """One game turn"""
        if not self.snake_alive:
            return
        # If there is a queued direction, set it, unless it's opposite
        # of the current direction (that would make the snake crash immediately!)
        if self.snake_queued_directions:
            old_x, old_y = self.snake_direction
            new_direction = self.snake_queued_directions[0]
            del self.snake_queued_directions[0]
            new_x, new_y = new_direction
            if (old_x, old_y) != (-new_x, -new_y):
                self.snake_direction = new_direction
        # Get the old and new snake coordinates
        old_x, old_y = self.snake_coords[-1]
        dx, dy = self.snake_direction
        new_x = old_x + dx
        new_y = old_y + dy
        new_x = new_x % self.width
        new_y = new_y % self.height
        new_head = new_x, new_y

        # Handle the snake crashing into itself
        if new_head in self.snake_coords:
            self.snake_alive = False

        # Add the new coordinate to the snake
        self.snake_coords.append(new_head)

        if new_head in self.food:
            # Eating food: remove the food and add a new one
            self.food.remove(new_head)
            self.add_food()
        else:
            # Not eating fruit: remove last part of the snake
            del self.snake_coords[0]

    def add_food(self):
        """Add a new piece of food to the game"""
        for i in range(100):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            if not (position in self.snake_coords or position in self.food):
                self.food.append(position)
                return
