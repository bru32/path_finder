# tkinter random walker demo

__author__ = "Bruce Wernick"
__date__ = "20 August 2021"


from tkinter import *
from random import choice
from recordclass import recordclass
from copy import copy
from uColor import *


# Declaring Current Position class (using a recordclass)
CurrPos = recordclass('CurrPos', 'x y d color')


# ---------------------------------------------------------------------

class MainForm(Frame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    # init dimensions
    self.fwidth = 400
    self.fheight = 400
    self.dx = 40
    self.dy = 40
    self.nx = self.fwidth // self.dx
    self.ny = self.fheight // self.dy
    self.x0, self.x1 = 0, self.fwidth
    self.y0, self.y1 = 0, self.fheight

    # crate a drawing surface
    self.canvas = Canvas(self, width=self.fwidth, height=self.fheight, bg="#384a51")

    # store current position cp = (x, y, d, color)
    self.cp = CurrPos(self.nx // 2, self.ny // 2, 0, "red")

    # a_node with empty trail
    self.trail = []
    self.trail_size = 12

    self.canvas.place(x=20, y=20)
    self.pack(fill=BOTH, expand=1)

  def draw_gridlines(self):
    """ Draw vertical and horizontal gridlines
    """
    x0, x1 = self.x0, self.x1
    y0, y1 = self.y0, self.y1
    dx, dy = self.dx, self.dy
    gcolor = "#325b6c"
    gwidth = 1

    # vertical grid lines
    x = x0 + dx
    while x < x1:
      self.canvas.create_line(x, y0, x, y1, width=gwidth, fill=gcolor)
      x += dx

    # horizontal grid lines
    y = y0 + dy
    while y < y1:
      self.canvas.create_line(x0, y, x1, y, width=gwidth, fill=gcolor)
      y += dy

  def shade_rect(self, cp, i, imax):
    g = 2  # cell gap
    dx = self.dx
    dy = self.dy
    x = cp.x * dx
    y = cp.y * dy
    color = color_step(i, imax)
    self.canvas.create_rectangle(x+g, y+g, x+dx-g, y+dy-g, width=1, outline="#593408", fill=color)

  def draw_trail(self):
    """ Draw the full trail
    """
    for i, cp in enumerate(self.trail):
      self.shade_rect(cp, i, self.trail_size)

  def limit(self):
    """ limit x,y values to edge of canvas.
    """
    x = self.cp.x
    y = self.cp.y
    d = self.cp.d
    nx = self.nx
    ny = self.ny

    if x < 0:
      x, d = 0, 0
    if x > nx - 1:
      x, d = nx - 1, 2
    if y < 0:
      y, d = 0, 3
    if y > ny - 1:
      y, d = ny - 1, 1

    self.cp.x = x
    self.cp.y = y
    self.cp.d = d

  def rand_step(self):
    """ Take random step in 0..nx and 0..ny.
    """
    stride = 1
    x = self.cp.x
    y = self.cp.y
    d = self.cp.d

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
    d = choice([forward, left, right])

    # take step in direction d
    if d == 0:
      x += stride
    elif d == 1:
      y -= stride
    elif d == 2:
      x -= stride
    else:
      y += stride

    self.cp.x = x
    self.cp.y = y
    self.cp.d = d

  def update_trail(self):
    cp = copy(self.cp)
    self.trail.insert(0, cp)
    if len(self.trail) > self.trail_size:
      self.trail = self.trail[:self.trail_size]

  def animloop(self):
    """ Animation loop
    """

    # clear canvas
    self.canvas.delete("all")
    self.draw_gridlines()

    # get the new position
    self.rand_step()
    self.limit()

    # update trail and draw
    self.update_trail()
    self.draw_trail()

    # repeat to animate
    app.after(100, self.animloop)


# ---------------------------------------------------------------------

if __name__ == "__main__":

  # Example of animation with tkinter
  app = Tk()
  app.title("tkinter animation")
  app.geometry('440x440+1000+100')
  main = MainForm(app)
  app.after(1, main.animloop)
  app.mainloop()
