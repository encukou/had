import re

from flask import Flask, Response, render_template_string, abort, request
from flask import send_from_directory, url_for, redirect

from had import State

app = Flask(__name__)

TILE_SIZE = 64

@app.route('/')
def home():
    return redirect(url_for('game_page', width=10, height=10))

@app.route('/<int:width>/<int:height>/')
def game_page(width, height):
    state = State()
    state.width = width
    state.height = height
    state.add_food()
    state_str = encode_state(state)
    return f"""<!doctype html>
        <html>
            <head>
                <title>HAD</title>
            </head>
            <body>
                <div style="font-size: 2cm;">
                    <div
                        id="game"
                        style="
                            width: {state.width}em;
                            height: {state.height}em;
                            position: relative;
                            background-color: black;
                            border-radius: 4px;
                        "
                    >
                        { game(state_str) }
                    </div>
                </div>
                <div style="margin-top: .5em;">
                    Hýbej se pomocí kláves
                    <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd>.
                </div>
                <input
                    type="hidden"
                    id="instructions"
                    data-baseurl="{ url_for('game', state_str='_STATE_',
                                            instructions='_INSTRUCTIONS_') }"
                />
                <script>{ SCRIPT }</script>
            </body>
        </html>
    """

SCRIPT = """
    window.addEventListener('load', function () {
        var instructions_elem = document.getElementById("instructions");
        var game_elem = document.getElementById("game");
        function move() {
            var state_elem = document.getElementById("game-state");
            var state = state_elem.value;
            var baseurl = instructions_elem.getAttribute("data-baseurl");
            var instructions = instructions_elem.value;
            instructions_elem.value = "";
            var url = baseurl.
                replace('_STATE_', state).
                replace('_INSTRUCTIONS_', '+' + instructions);
            console.log(url);
            var oReq = new XMLHttpRequest();
            oReq.addEventListener("load", update);
            oReq.open("GET", url);
            oReq.send();
        }
        function update () {
            game_elem.innerHTML = this.responseText;
            setTimeout(move, 1000/5);
        }
        setTimeout(move, 1000/5);

        window.addEventListener('keydown', function (event) {
            if (['w', 'a', 's', 'd', 'W', 'A', 'S', 'D'].includes(event.key)) {
                instructions_elem.value = instructions_elem.value + event.key;
            } else {
                console.log(event);
            }
        });
    });
"""

@app.route('/next/<state_str>/')
@app.route('/next/<state_str>/<instructions>')
def game(state_str, instructions=None):
    state = decode_state(state_str)
    if instructions is not None:
        for c in instructions.lower():
            state.snake_queued_directions.extend({
                'w': [(0, 1)],
                'a': [(-1, 0)],
                's': [(0, -1)],
                'd': [(1, 0)],
            }.get(c, []))
        state.move()
        return redirect(url_for('game', state_str=encode_state(state)))
    images = []
    for x, y in state.food:
        images.append((x, y, url_for('apple_image')))
    for a, b, c in zip(
            [None] + state.snake_coords,
            state.snake_coords,
            state.snake_coords[1:] + [None],
            ):
        x, y = b
        u = direction(a, b)
        v = direction(c, b)
        if v == 'tail':
            if not state.snake_alive:
                v = 'dead'
            #elif time.time() % 1 < 0.2:
            #    v = 'tongue'
            else:
                v = 'head'
        images.append((x, y, url_for('tile_image', a=u, b=v)))
    result = [f"""
            <img
                src="{ url }"
                style="
                    position: absolute;
                    left: {x}em;
                    top: {state.height-y-1}em;
                    width: 1em;
                    height: 1em;
                "
            >
        """ for x, y, url in images]
    state_str = encode_state(state)
    result.append(
        f"""<input type="hidden" id="game-state" value="{ state_str }">""")
    return ''.join(result)

def encode_state(state):
    def encode_coords(coords):
        return '_'.join(f'{x}:{y}' for x, y in coords)
    return '|'.join([
        str(state.width),
        str(state.height),
        encode_coords(state.snake_coords),
        encode_coords(state.food),
        encode_coords([state.snake_direction]),
        encode_coords(state.snake_queued_directions),
        '0_0' if state.snake_alive else 'X_X',
    ])

def decode_state(state_str):
    state = State()
    w, h, coords, food, direction, queued, alive = state_str.split('|')
    state.width = int(w)
    state.height = int(h)
    def decode_coords(coords):
        return [tuple(int(c) for c in coord.split(':'))
                for coord in coords.split('_') if coord]
    state.snake_coords = decode_coords(coords)
    state.food = decode_coords(food)
    [state.snake_direction] = decode_coords(direction)
    state.snake_queued_directions = decode_coords(queued)
    state.snake_alive = (alive == '0_0')
    return state

def direction(a, b):
    if a is None:
        return 'tail'
    if b is None:
        return 'tail'
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
        return 'tail'

@app.route('/tile/<a>-<b>.png')
def tile_image(a, b):
    if not re.match('^[a-z]+$', a) or not re.match('^[a-z]+$', a):
        abort(404)
    return send_from_directory('snake-tiles', f'{a}-{b}.png')

@app.route('/tile/apple.png')
def apple_image():
    return send_from_directory('.', 'apple.png')


if __name__ == '__main__':
    app.run()

