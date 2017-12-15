import pyglet

import had

sprites = pyglet.image.load('sprites.png')

window = pyglet.window.Window(width=800, height=600)

state = had.State()
state.add_fruit()
state.width = window.width // 32
state.height = window.height // 32

queued_directions = []

def draw():
    window.clear()
    tile_width = window.width / state.width
    tile_height = window.height / state.height
    for x, y, in state.snake:
        sprites.get_region(32, 0, 32, 32).blit(
            x * tile_width, y * tile_height,
            width=tile_width, height=tile_height)
    for x, y, in state.fruit:
        sprites.get_region(32, 32, 32, 32).blit(
            x * tile_width, y * tile_height,
            width=tile_width, height=tile_height)
    if not state.alive:
        w = 64
        h = 64
        sprites.get_region(0, 0, 32, 32).blit(
            (window.width-w)/2, (window.height-h)/2,
            width=w, height=h)

def tick(dt):
    if not state.alive:
        return
    if queued_directions:
        old_x, old_y = state.direction
        new_direction = queued_directions[0]
        del queued_directions[0]
        new_x, new_y = new_direction
        if (old_x, old_y) != (-new_x, -new_y):
            state.direction = new_direction
    state.move()
    pyglet.clock.schedule_once(tick, state.speed*1.5 - dt/5)

def key_press(symbol, mod):
    if symbol in (pyglet.window.key.A, pyglet.window.key.LEFT):
        queued_directions.append((-1, 0))
    elif symbol in (pyglet.window.key.D, pyglet.window.key.RIGHT):
        queued_directions.append((1, 0))
    elif symbol in (pyglet.window.key.S, pyglet.window.key.DOWN):
        queued_directions.append((0, -1))
    elif symbol in (pyglet.window.key.W, pyglet.window.key.UP):
        queued_directions.append((0, 1))

window.push_handlers(
    on_draw=draw,
    on_key_press=key_press,
)

tick(state.speed)

def add_more_fruit(dt):
    state.add_fruit()

pyglet.clock.schedule_interval(add_more_fruit, 30)

pyglet.app.run()
