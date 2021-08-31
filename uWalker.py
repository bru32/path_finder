# Random walk utils

"""
Random step with boundary limits.
"""

__author__ = "Bruce Wernick"
__date__ = "31 August 2021"

import random


def limit(x, y, d, nx, ny):
  """ limit x,y values to edge of canvas. """
  if x < 0:
    x, d = 0, 0
  if x > nx - 1:
    x, d = nx - 1, 2
  if y < 0:
    y, d = 0, 3
  if y > ny - 1:
    y, d = ny - 1, 1
  return x, y, d


def wrap(x, y, d, nx, ny):
  """ Wrap x,y values around canvas edge. """
  if x < 0:
    x = nx - 1, 0
  if x > nx - 1:
    x = 0
  if y < 0:
    y = ny - 1
  if y > ny - 1:
    y = 0
  return x, y, d


def rand_step(x, y, d, nx, ny, edge_func=limit):
  """ Take random step in 0..nx and 0..ny. """

  # assign directions for forward, left, right
  if d == 0:
    forward, left, right = 0, 1, 3
  elif d == 1:
    forward, left, right = 1, 2, 0
  elif d == 2:
    forward, left, right = 2, 3, 1
  else:  # d = 3
    forward, left, right = 3, 0, 2

  # random choice of new direction
  d = random.choice([forward, left, right])

  # take step in direction d
  if d == 0:
    x += 1
  elif d == 1:
    y -= 1
  elif d == 2:
    x -= 1
  else:
    y += 1

  x, y, d = edge_func(x, y, d, nx, ny)
  return x, y, d


# ---------------------------------------------------------------------

def test1():
  """ Take n random steps """
  nx, ny = 20, 20  # set the board size
  x, y = 10, 10  # position in the middle
  d = 0  # right
  n = 1000
  for i in range(n):
    x, y, d = rand_step(x, y, d, nx, ny, limit)

  print(f"Final position after {n} steps = ({x}, {y})")


if __name__ == "__main__":

  test1()
