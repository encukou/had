import pytest

import had

def test_movement_length_one():
    field = had.State()
    field.snake_direction = 0, 1
    field.move()
    assert field.snake_coords == [(0, 1)]
    field.snake_direction = 0, -1
    field.move()
    assert field.snake_coords == [(0, 0)]
    field.snake_direction = 1, 0
    field.move()
    assert field.snake_coords == [(1, 0)]
    field.snake_direction = -1, 0
    field.move()
    assert field.snake_coords == [(0, 0)]
    assert field.snake_alive

def test_movement_length_three():
    field = had.State()
    field.snake_coords = [(5, 5), (5, 6), (5, 7)]
    field.snake_direction = 0, 1
    field.move()
    assert field.snake_coords == [(5, 6), (5, 7), (5, 8)]
    field.snake_direction = 0, 1
    field.move()
    assert field.snake_coords == [(5, 7), (5, 8), (5, 9)]
    field.snake_direction = -1, 0
    field.move()
    assert field.snake_coords == [(5, 8), (5, 9), (4, 9)]
    field.snake_direction = -1, 0
    field.move()
    assert field.snake_coords == [(5, 9), (4, 9), (3, 9)]
    field.snake_direction = 0, -1
    field.move()
    assert field.snake_coords == [(4, 9), (3, 9), (3, 8)]
    field.snake_direction = 0, -1
    field.move()
    assert field.snake_coords == [(3, 9), (3, 8), (3, 7)]
    field.snake_direction = 1, 0
    field.move()
    assert field.snake_coords == [(3, 8), (3, 7), (4, 7)]
    field.snake_direction = 1, 0
    field.move()
    assert field.snake_coords == [(3, 7), (4, 7), (5, 7)]
    assert field.snake_alive

@pytest.mark.parametrize('direction', [(0, 1), (0, -1), (1, 0), (-1, 0)])
def test_crash_wall(direction):
    field = had.State()
    field.width = 1
    field.height = 1
    field.snake_direction = direction
    field.move()
    assert field.snake_alive

@pytest.mark.parametrize('direction', [(0, 1), (0, -1), (1, 0), (-1, 0)])
def test_crash_self(direction):
    field = had.State()
    field.snake_coords = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2),
                          (0, 1), (1, 1)]
    field.snake_direction = direction
    field.move()
    assert not field.snake_alive

@pytest.mark.parametrize('direction', [(0, 1), (0, -1), (1, 0), (-1, 0)])
def test_eat_fruit(direction):
    field = had.State()
    field.width = 5
    field.height = 5
    field.snake_coords = [(2, 2)]
    field.fruit = [(2, 1), (2, 3), (1, 2), (3, 2)]
    field.snake_direction = direction
    print(field, '\n')
    field.move()
    print(field, '\n')
    assert len(field.fruit) == 4
    assert len(set(field.fruit) - {(2, 1), (1, 2), (2, 3), (3, 2)}) == 1
    field.fruit = [(2, 1), (2, 3), (1, 2), (3, 2)]
    field.fruit.remove((2+direction[0], 2+direction[1]))
    print(field, '\n')
    assert len(field.snake_coords) == 2
    assert field.snake_coords[0] == (2, 2)
    field.move()
    print(field, '\n')
    assert len(field.snake_coords) == 2
    assert (2, 2) not in field.snake_coords

    assert len(field.fruit) == 3
    assert len(set(field.fruit)) == 3
    assert set(field.fruit).isdisjoint(field.snake_coords)
    assert field.snake_alive

    field.move()
    print(field, '\n')
    field.move()
    print(field, '\n')
    field.move()
    print(field, '\n')
    assert field.snake_coords[-1] == (2, 2)
    assert field.snake_alive
