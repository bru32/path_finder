# tkinter walker demo

"""
Random walker with a trail.
"""

__author__ = "Bruce Wernick"
__date__ = "25 August 2021"

import tkinter as tk
from collections import deque
from uWalker import rand_step
from uColor import *


class MainForm(tk.Frame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    # define constants
    self.width = 520
    self.height = 520
    self.x0 = 0
    self.x1 = self.width
    self.y0 = 0
    self.y1 = self.height
    self.dx = 13
    self.dy = 13
    self.nx = self.width // self.dx
    self.ny = self.height // self.dy

    self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg='#00284d')

    self.draw_gridlines()

    # initial position
    x = self.nx // 2
    y = self.ny // 2
    d = randint(0, 4)
    self.cp = (x, y, d)

    # create a fixed length tail
    self.ntail = 120
    self.tail = deque(maxlen=self.ntail)
    self.tail.append(self.cp)

    self.pack(fill="both", expand=1)
    self.canvas.pack(fill="both", expand=1, padx=10, pady=10)

  def draw_gridlines(self):
    x = self.x0 + self.dx
    while x < self.x1:
      coords = x, self.y0, x, self.y1
      self.canvas.create_line(coords, width=1, fill="gray")
      x += self.dx
    y = self.y0 + self.dy
    while y < self.y1:
      coords = self.x0, y, self.x1, y
      self.canvas.create_line(coords, width=1, fill="gray")
      y += self.dy

  def move_snake(self):
    x, y, d = self.cp
    x, y, d = rand_step(x, y, d, self.nx, self.ny)
    self.cp = x, y, d
    self.tail.append(self.cp)

  def draw_snake(self):
    self.canvas.delete('tail')
    g = 2
    dx = self.dx
    dy = self.dy
    for i, cp in enumerate(self.tail):
      x, y, d = cp
      x *= dx
      y *= dy
      coords = x+g, y+g, x+dx-g, y+dy-g
      color = color_step(i, self.ntail)
      self.canvas.create_rectangle(coords, fill=color, width=0, tag="tail")
    self.canvas.update()

  def animloop(self):
    """ animation loop """
    self.move_snake()
    self.draw_snake()
    app.after(24, self.animloop)


# ---------------------------------------------------------------------

if __name__ == "__main__":

  app = tk.Tk()
  app.title("Random Walker")
  app.geometry('540x540+960+40')
  app.configure(bg='black')
  app.minsize(300, 300)
  main = MainForm(app)
  app.after(10, main.animloop)
  app.mainloop()
