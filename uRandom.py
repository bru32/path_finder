# Random utils

__author__ = "Bruce Wernick"
__date__ = "23 August 2021"


import random


def rand_point(rows, cols):
  """ random (r, c) point """
  r = random.randint(0, rows)
  c = random.randint(0, cols)
  return r, c


def rand_byte(value=(0, 255)):
  """ random byte """
  if type(value) is int:
    return value
  elif type(value) is tuple:
    return random.randint(value[0], value[1])
  return random.randint(0, 255)


def rand_color(red=(92, 220), green=(92, 220), blue=(92, 220)):
  """ Random red, green, blue with the option to limit the ranges.
      The ranges are tuples 0..255.
  """
  r = rand_byte(red)
  g = rand_byte(green)
  b = rand_byte(blue)
  return f"#{r:02x}{g:02x}{b:02x}"


# ---------------------------------------------------------------------

def test1():
  print(rand_point(255, 255))

  color = rand_color()
  print(color)

  color = rand_color(red=255)
  print(color)

  color = rand_color(blue=64, green=128, red=255)
  print(color)

  color = rand_color(red=(0, 255))
  print(color)


# ---------------------------------------------------------------------

if __name__ == "__main__":

  test1()
