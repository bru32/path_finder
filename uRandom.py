# Random utils

__author__ = "Bruce Wernick"
__date__ = "23 August 2021"


import random


def rand_point(rows, cols):
  """ random (r, c) point """
  r = random.randint(0, rows)
  c = random.randint(0, cols)
  return r, c


def rand_byte(value = (0, 255)):
  """ random byte """
  if type(value) is int:
    return value
  elif type(value) is tuple:
    return random.randint(value[0], value[1])
  return random.randint(0, 255)


def rand_color(red=(92,220), green=(92,220), blue=(92,220)):
  """ Random red, green, blue with the option to limit the ranges.
      The ranges are tuples 0..255.
  """
  r = rand_byte(red)
  g = rand_byte(green)
  b = rand_byte(blue)
  return f"#{r:02x}{g:02x}{b:02x}"


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
  else: # d = 3
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

if __name__ == "__main__":

  print(rand_point(255, 255))

  color = rand_color()
  print(color)

  color = rand_color(red=255)
  print(color)

  color = rand_color(blue=64, green=128, red=255)
  print(color)

  color = rand_color(red=(0,255))
  print(color)
