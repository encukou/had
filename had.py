import random

class Snake():
    def __init__(self, state):
        self.state = state
        self.alive = True
        self.coords = [(0, 0)]
        self.direction = 1, 0
        self.queued_directions = []

    def move(self):
        if not self.alive:
            return
        if self.queued_directions:
            old_x, old_y = self.direction
            new_direction = self.queued_directions[0]
            del self.queued_directions[0]
            new_x, new_y = new_direction
            if (old_x, old_y) != (-new_x, -new_y):
                self.direction = new_direction
        old_x, old_y = self.coords[-1]
        dx, dy = self.direction
        new_x = old_x + dx
        new_y = old_y + dy
        if new_x < 0:
            new_x = self.state.width - 1
        if new_y < 0:
            new_y = self.state.height - 1
        if new_x >= self.state.width:
            new_x = 0
        if new_y >= self.state.height:
            new_y = 0
        new_head = new_x, new_y
        if new_head in self.state.fruit:
            self.state.fruit.remove(new_head)
            self.state.add_fruit()
        else:
            del self.coords[0]
        for snake in self.state.snakes:
            if new_head in snake.coords:
                self.alive = False
                self.coords.append(new_head)
                return
        self.coords.append(new_head)

class State:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.fruit = []
        self.speed = 1/10
        self.snakes = [Snake(self) for i in range(2)]
        self.snakes[1].coords = [(0, 3), (1, 3)]

    def __str__(self):
        rows = []
        for i in range(self.height):
            row = []
            for i in range(self.width):
                row.append('.')
            rows.append(row)
        for x, y in self.snake:
            rows[y][x] = 'X'
        for x, y in self.fruit:
            rows[y][x] = '!'
        return '\n'.join(' '.join(row) for row in reversed(rows))

    def move(self):
        for snake in self.snakes:
            snake.move()

    def add_fruit(self):
        for i in range(100):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            if not (any(position in s.coords for s in self.snakes) or
                    position in self.fruit):
                self.fruit.append(position)
                return
