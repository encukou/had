import textwrap

import had


def test_repr_empty_field():
    expected = textwrap.dedent("""
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
    """).strip()
    state = had.State()
    state.snake = []
    assert str(state) == expected


def test_repr_some_coords():
    expected = textwrap.dedent("""
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . X . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . X . . . . . .
        . . X . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
    """).strip()
    state = had.State()
    state.snake = [(2, 2), (3, 3), (4, 7)]
    assert str(state) == expected


def test_repr_snake():
    expected = textwrap.dedent("""
        . . . . . . . . . .
        . . . . X . . . . .
        . . . . X . . . . .
        . . . . X . . . . .
        . . . . X . . . . .
        . . . . X . . . . .
        . . . . X . . . . .
        . . X X X . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
    """).strip()
    state = had.State()
    state.snake = [(2, 2), (3, 2), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8)]
    assert str(state) == expected


def test_repr_size():
    expected = textwrap.dedent("""
        . . . . . . . . . . .
        . . . X . . . . . . .
        . . X . . . . . . . .
        . . . . . . . . . . .
        . . . . . . . . . . .
    """).strip()
    state = had.State()
    state.width = 11
    state.height = 5
    state.snake = [(2, 2), (3, 3)]
    assert str(state) == expected
