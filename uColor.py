# Color Utils

__author__ = 'Bruce Wernick'
__date__ = '29 August 2021'

from colorsys import hls_to_rgb
from random import randint


def color_step(i, imax):
  """ Step to a color based on the index. """
  h = 0.36 * i / imax
  l = 0.65
  s = 0.6
  r, g, b = hls_to_rgb(h, l, s)
  r, g, b = int(r * 255), int(g * 255), int(b * 255)
  hx = rgb_to_hex(r, g, b)
  return hx


def hex_to_rgb(value):
  """ Convert hex color to r,g,b values. """
  hex = value.lstrip('#')
  r, g, b = tuple(int(hex[i: i + 2], 16) for i in (0, 2, 4))
  return r, g, b


def rgb_to_hex(r, g, b):
  """ Red, Green, Blue colors 0-255,
     returns hex color string.
  """
  return f'#{r:02x}{g:02x}{b:02x}'


def rgb_lerp(a, b, f):
  """ linear blend rgb color a and b. """
  r = int(a[0] + f * (b[0] - a[0]))
  g = int(a[1] + f * (b[1] - a[1]))
  b = int(a[2] + f * (b[2] - a[2]))
  return r, g, b


def hex_lerp(a, b, f):
  """ linear blend hex colors a and b. """
  a = hex_to_rgb(a)
  b = hex_to_rgb(b)
  rgb = rgb_lerp(a, b, f)
  return rgb_to_hex(*rgb)


def rand_color(r0=0, r1=255, g0=0, g1=255, b0=0, b1=255):
  """ Random rgb with the option to limit the ranges. """
  r = randint(r0, r1)
  g = randint(g0, g1)
  b = randint(b0, b1)
  return f"#{r:02x}{g:02x}{b:02x}"

