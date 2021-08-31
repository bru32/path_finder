# show grid search

__author__ = 'Bruce Wernick'
__date__ = '29 August 2021'

import tkinter as tk
from grid_search import *
from uColor import hex_lerp
import uGrid


class MainForm(tk.Frame):

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    # init dimensions
    self.fwidth = 400
    self.fheight = 400
    self.dx = 20
    self.dy = 20
    self.nx = self.fwidth // self.dx
    self.ny = self.fheight // self.dy
    self.x0, self.x1 = 0, self.fwidth
    self.y0, self.y1 = 0, self.fheight

    # crate a drawing surface
    self.canvas = tk.Canvas(self, width=self.fwidth, height=self.fheight, bg="#384a51")

    # bind buttons
    self.canvas.bind_all('<F9>', self.random_find_path)
    self.canvas.bind_all('<Button-1>', self.place_start)
    self.canvas.bind_all('<Button-3>', self.place_goal)
    self.canvas.bind_all('<Control-Button-1>', self.toggle_wall)

    self.draw_gridlines()

    # game variables
    self.path = []

    nwalls = int(1.616*(self.ny + self.nx))
    self.grid, self.start, self.goal = uGrid.rand_grid(self.ny, self.nx, nwalls)
    self.do_search()

    self.canvas.place(x=20, y=20)
    self.pack(fill=tk.BOTH, expand=1)

  def draw_gridlines(self):
    """ Draw x/y grid lines """
    x0, x1 = self.x0, self.x1
    y0, y1 = self.y0, self.y1
    dx, dy = self.dx, self.dy
    grid_color = "#325b6c"
    grid_width = 1

    # vertical grid lines
    x = x0 + dx
    while x < x1:
      self.canvas.create_line(x, y0, x, y1, width=grid_width, fill=grid_color)
      x += dx

    # horizontal grid lines
    y = y0 + dy
    while y < y1:
      self.canvas.create_line(x0, y, x1, y, width=grid_width, fill=grid_color)
      y += dy

  def shade_rect(self, j, i, color, tag):
    """ Shade cell at the current position """
    g = 1  # cell gap
    dx = self.dx
    dy = self.dy
    x = i * dx
    y = j * dy
    self.canvas.create_rectangle(x+g, y+g, x+dx-g, y+dy-g, width=1, outline="#593408", fill=color, tag=tag)

  def do_search(self):
    """ Search for a path """
    self.canvas.delete("wall")
    for cp in self.grid.walls:
      j, i = cp
      self.shade_rect(j, i, "#486270", "wall")

    #  find_path, shortest_path, fsp, bfs_search, dijkstra_search, astar_search
    search_func = astar_search
    self.path = search_func(self.grid, self.start, self.goal)

    self.canvas.delete("path")
    n = len(self.path) - 1
    for k, cp in enumerate(self.path):
      j, i = cp
      color = hex_lerp("#ff5b0f", "#9fff0f", k/n)
      self.shade_rect(j, i, color, "path")
    self.canvas.update()

    self.canvas.delete("a_node", "b_node")
    j, i = self.start
    self.shade_rect(j, i, "#ff1a1a", "a_node")

    j, i = self.goal
    self.shade_rect(j, i, "#009407", "b_node")

  def random_find_path(self):
    """ Create random game """
    ny = self.ny
    nx = self.nx
    nwalls = int(1.616*(ny+nx))
    self.grid, self.start, self.goal = uGrid.rand_grid(ny, nx, nwalls)
    self.do_search()

  def place_start(self, event):
    """ place a_node position """
    j = int(event.y / self.dy)
    i = int(event.x / self.dx)
    self.start = (j, i)
    self.do_search()

  def place_goal(self, event):
    """ place b_node position """
    j = int(event.y / self.dy)
    i = int(event.x / self.dx)
    self.goal = (j, i)
    self.do_search()

  def toggle_wall(self, event):
    """ toggle wall on/off """
    j = int(event.y / self.dy)
    i = int(event.x / self.dx)
    cp = (j, i)
    self.grid.toggle_wall(cp)
    self.do_search()


# ---------------------------------------------------------------------

if __name__ == "__main__":

  app = tk.Tk()
  app.title("AStar Path Finder")
  app.geometry('440x440+1000+100')
  main = MainForm(app)
  app.mainloop()
