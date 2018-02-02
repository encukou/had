import time

import pyglet

import had

TILE_SIZE = 64
MARGIN = 8

sprites = pyglet.image.load('sprites.png')

window = pyglet.window.Window(width=800, height=600)

state = had.State()
state.add_fruit()
state.width = window.width // TILE_SIZE
state.height = window.height // TILE_SIZE

queued_directions = []

def get_tile(u, v):
    return sprites.get_region(
        MARGIN+u*(TILE_SIZE+MARGIN*2),
        MARGIN+v*(TILE_SIZE+MARGIN*2),
        TILE_SIZE, TILE_SIZE)

def draw():
    window.clear()
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    tile_width = window.width // state.width
    tile_height = window.height // state.height
    for a, b, c in zip(
            state.snake_coords[1:] + [None],
            state.snake_coords,
            [None] + state.snake_coords):
        x, y = b
        u = direction(a, b)
        v = direction(b, c)
        if a is None:
            if not state.snake_alive:
                u += 6
            elif time.time() % 1 < 0.2:
                u += 5
        get_tile(u, v).blit(
            x * tile_width, y * tile_height,
            width=tile_width, height=tile_height)
    for x, y, in state.fruit:
        get_tile(0, 5).blit(
            x * tile_width, y * tile_height,
            width=tile_width, height=tile_height)

def tick(dt):
    state.move()
    pyglet.clock.schedule_once(tick, state.speed*1.5 - dt/5)

def direction(a, b):
    if a is None:
        return 0
    if b is None:
        return 0
    x1, y1 = a
    x2, y2 = b
    if x1 == x2 - 1:
        return 1
    elif x1 == x2 + 1:
        return 2
    elif y1 == y2 - 1:
        return 3
    elif y1 == y2 + 1:
        return 4
    elif x1 > x2:
        return 1
    elif x1 < x2:
        return 2
    elif y1 > y2:
        return 3
    elif y1 < y2:
        return 4
    else:
        return 0


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

def add_more_fruit(dt):
    state.add_fruit()

pyglet.clock.schedule_interval(add_more_fruit, 30)

pyglet.app.run()
