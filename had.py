import random

class State:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.fruit = []
        self.speed = 1/10

        self.snake_alive = True
        self.snake_coords = [(0, 0)]
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
        for x, y in self.fruit:
            rows[y][x] = '!'
        return '\n'.join(' '.join(row) for row in reversed(rows))

    def move(self):
        if not self.snake_alive:
            return
        if self.snake_queued_directions:
            old_x, old_y = self.snake_direction
            new_direction = self.snake_queued_directions[0]
            del self.snake_queued_directions[0]
            new_x, new_y = new_direction
            if (old_x, old_y) != (-new_x, -new_y):
                self.snake_direction = new_direction
        old_x, old_y = self.snake_coords[-1]
        dx, dy = self.snake_direction
        new_x = old_x + dx
        new_y = old_y + dy
        new_x = new_x % self.width
        new_y = new_y % self.height
        new_head = new_x, new_y
        if new_head in self.fruit:
            self.fruit.remove(new_head)
            self.add_fruit()
        else:
            del self.snake_coords[0]
        if new_head in self.snake_coords:
            self.snake_alive = False
            self.snake_coords.append(new_head)
            return
        self.snake_coords.append(new_head)

    def add_fruit(self):
        for i in range(100):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            if not (position in self.snake_coords or position in self.fruit):
                self.fruit.append(position)
                return
