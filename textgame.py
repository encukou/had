import had

state = had.State()
state.add_fruit()

while state.snake_alive:
    print(state)
    if state.snake_queued_directions:
        result = ''
    else:
        result = input('Next move (W, S, A, D): ')
    for letter in result:
        if letter.lower() == 'a':
            state.snake_queued_directions.append((-1, 0))
        elif letter.lower() == 'd':
            state.snake_queued_directions.append((1, 0))
        elif letter.lower() == 's':
            state.snake_queued_directions.append((0, -1))
        elif letter.lower() == 'w':
            state.snake_queued_directions.append((0, 1))
        else:
            print('Unknown direction:', letter)
    state.move()

print(state)
print('GAME OVER')
