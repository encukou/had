import pytest

import had

def test_movement_length_one():
    field = had.State()
    field.direction = 0, 1
    field.move()
    assert field.snake == [(0, 1)]
    field.direction = 0, -1
    field.move()
    assert field.snake == [(0, 0)]
    field.direction = 1, 0
    field.move()
    assert field.snake == [(1, 0)]
    field.direction = -1, 0
    field.move()
    assert field.snake == [(0, 0)]
    assert field.alive

def test_movement_length_two():
    field = had.State()
    field.snake = [(5, 5), (5, 6), (5, 7)]
    field.direction = 0, 1
    field.move()
    assert field.snake == [(5, 6), (5, 7), (5, 8)]
    field.direction = 0, 1
    field.move()
    assert field.snake == [(5, 7), (5, 8), (5, 9)]
    field.direction = -1, 0
    field.move()
    assert field.snake == [(5, 8), (5, 9), (4, 9)]
    field.direction = -1, 0
    field.move()
    assert field.snake == [(5, 9), (4, 9), (3, 9)]
    field.direction = 0, -1
    field.move()
    assert field.snake == [(4, 9), (3, 9), (3, 8)]
    field.direction = 0, -1
    field.move()
    assert field.snake == [(3, 9), (3, 8), (3, 7)]
    field.direction = 1, 0
    field.move()
    assert field.snake == [(3, 8), (3, 7), (4, 7)]
    field.direction = 1, 0
    field.move()
    assert field.snake == [(3, 7), (4, 7), (5, 7)]
    assert field.alive

@pytest.mark.parametrize('direction', [(0, 1), (0, -1), (1, 0), (-1, 0)])
def test_crash_wall(direction):
    field = had.State()
    field.width = 1
    field.height = 1
    field.direction = direction
    field.move()
    assert not field.alive

@pytest.mark.parametrize('direction', [(0, 1), (0, -1), (1, 0), (-1, 0)])
def test_crash_self(direction):
    field = had.State()
    field.snake = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2),
                   (0, 1), (1, 1)]
    field.direction = direction
    field.move()
    assert not field.alive

@pytest.mark.parametrize('direction', [(0, 1), (0, -1), (1, 0), (-1, 0)])
def test_eat_fruit(direction):
    field = had.State()
    field.width = 5
    field.height = 5
    field.snake = [(2, 2)]
    field.fruit = [(2, 1), (2, 3), (1, 2), (3, 2)]
    field.direction = direction
    field.move()
    assert len(field.snake) == 2
    assert field.snake[0] == (2, 2)
    field.move()
    assert len(field.snake) == 2
    assert (2, 2) not in field.snake

    assert len(field.fruit) == 4
    assert len(set(field.fruit)) == 4
    assert set(field.fruit).isdisjoint(field.snake)
    assert field.alive

    field.move()
    field.move()
    field.move()
    assert field.snake[-1] == (2, 2)
    assert field.alive
