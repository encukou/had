import random

class Crash(Exception):
    """The snake crashed"""

class State:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.snake = [(0, 0)]
        self.fruit = []
        self.direction = 1, 0
        self.speed = 1/10
        self.alive = True

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
        if not self.alive:
            return
        x, y = self.snake[-1]
        dx, dy = self.direction
        new_x = x + dx
        new_y = y + dy
        if new_x < 0:
            new_x = self.width - 1
        if new_y < 0:
            new_y = self.height - 1
        if new_x >= self.width:
            new_x = 0
        if new_y >= self.height:
            new_y = 0
        new_head = new_x, new_y
        if new_head in self.snake:
            self.alive = False
        self.snake.append(new_head)
        if new_head in self.fruit:
            self.fruit.remove(new_head)
            self.add_fruit()
        else:
            del self.snake[0]

    def add_fruit(self):
        for i in range(100):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            if position not in self.snake and position not in self.fruit:
                self.fruit.append(position)
                return
