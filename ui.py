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
    for i, snake in enumerate(state.snakes):
        for x, y, in snake.coords:
            sprites.get_region(0, i*32, 32, 32).blit(
                x * tile_width, y * tile_height,
                width=tile_width, height=tile_height)
        if not snake.alive:
            x, y = snake.coords[-1]
            sprites.get_region(32, 0, 32, 32).blit(
                x * tile_width, y * tile_height,
                width=tile_width, height=tile_height)
    for x, y, in state.fruit:
        sprites.get_region(32, 32, 32, 32).blit(
            x * tile_width, y * tile_height,
            width=tile_width, height=tile_height)

def tick(dt):
    state.move()
    pyglet.clock.schedule_once(tick, state.speed*1.5 - dt/5)

def key_press(symbol, mod):
    snakes = state.snakes
    if symbol == pyglet.window.key.A:
        snakes[0].queued_directions.append((-1, 0))
    if symbol == pyglet.window.key.LEFT:
        snakes[1].queued_directions.append((-1, 0))
    if symbol == pyglet.window.key.D:
        snakes[0].queued_directions.append((1, 0))
    if symbol == pyglet.window.key.RIGHT:
        snakes[1].queued_directions.append((1, 0))
    if symbol == pyglet.window.key.S:
        snakes[0].queued_directions.append((0, -1))
    if symbol == pyglet.window.key.DOWN:
        snakes[1].queued_directions.append((0, -1))
    if symbol == pyglet.window.key.W:
        snakes[0].queued_directions.append((0, 1))
    if symbol == pyglet.window.key.UP:
        snakes[1].queued_directions.append((0, 1))

window.push_handlers(
    on_draw=draw,
    on_key_press=key_press,
)

tick(state.speed)

def add_more_fruit(dt):
    state.add_fruit()

pyglet.clock.schedule_interval(add_more_fruit, 30)

pyglet.app.run()
