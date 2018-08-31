import time

import pyglet

import had
from pathlib import Path

TILE_SIZE = 64
MARGIN = 8

red_image = pyglet.image.load('apple.png')

snake_tiles = {}
for path in Path('snake-tiles').glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)

window = pyglet.window.Window(width=800, height=600)

state = had.State()
state.add_food()
state.width = window.width // TILE_SIZE
state.height = window.height // TILE_SIZE

queued_directions = []

def draw():
    window.clear()
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    tile_width = window.width // state.width
    tile_height = window.height // state.height
    for a, b, c in zip(
            [None] + state.snake_coords,
            state.snake_coords,
            state.snake_coords[1:] + [None],
            ):
        x, y = b
        u = direction(a, b)
        v = direction(c, b)
        if v == 'end':
            if not state.snake_alive:
                v = 'dead'
            elif time.time() % 1 < 0.2:
                v = 'tongue'
        snake_tiles[u + "-" + v].blit(
            x * tile_width, y * tile_height,
            width=tile_width, height=tile_height)
    for x, y, in state.food:
        red_image.blit(
            x * tile_width, y * tile_height,
            width=tile_width, height=tile_height)

def tick(dt):
    state.move()
    pyglet.clock.schedule_once(tick, state.speed*1.5 - dt/5)

def direction(a, b):
    if a is None:
        return 'end'
    if b is None:
        return 'end'
    x1, y1 = a
    x2, y2 = b
    if x1 == x2 - 1:
        return 'left'
    elif x1 == x2 + 1:
        return 'right'
    elif y1 == y2 - 1:
        return 'bottom'
    elif y1 == y2 + 1:
        return 'top'
    elif x1 > x2:
        return 'left'
    elif x1 < x2:
        return 'right'
    elif y1 > y2:
        return 'bottom'
    elif y1 < y2:
        return 'top'
    else:
        return 'end'


def key_press(symbol, mod):
    if symbol == pyglet.window.key.LEFT:
        state.snake_queued_directions.append((-1, 0))
    if symbol == pyglet.window.key.RIGHT:
        state.snake_queued_directions.append((1, 0))
    if symbol == pyglet.window.key.DOWN:
        state.snake_queued_directions.append((0, -1))
    if symbol == pyglet.window.key.UP:
        state.snake_queued_directions.append((0, 1))

window.push_handlers(
    on_draw=draw,
    on_key_press=key_press,
)

tick(state.speed)

def add_more_food(dt):
    state.add_food()

pyglet.clock.schedule_interval(add_more_food, 30)

pyglet.app.run()
