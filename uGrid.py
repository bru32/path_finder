# Grid Search

"""
2D Square grid thanks to Amit Patel Red Blob Games.
"""

__author__ = 'Bruce Wernick'
__date__ = '29 August 2021'


import uRandom


class Grid:
  """ 2D Square grid with walls and weights.
  """
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.walls = []
    self.weights = {}

  def add_wall(self, cp):
    self.walls.append(cp)

  def toggle_wall(self, cp):
    if cp in self.walls:
      self.walls.remove(cp)
    else:
      self.walls.append(cp)

  def cost(self, a, b):
    """ cost from a to b """
    return self.weights.get(b, 1)

  def in_bounds(self, cp):
    """ true if cp is within the bounds of the grid """
    r, c = cp
    return 0 <= r < self.rows and 0 <= c < self.cols

  def passable(self, cp):
    """ true if cp is not blocked """
    return cp not in self.walls

  def neighbors(self, cp):
    """ return all possible steps from cp """
    r, c = cp
    steps = [(r + 1, c), (r - 1, c), (r, c - 1), (r, c + 1)]
    if (r + c) % 2 == 0:
      steps.reverse()
    steps = filter(self.in_bounds, steps)
    steps = filter(self.passable, steps)
    return steps


def rand_grid(rows, cols, walls):
  """ Create a random grid with a_node and b_node """
  grid = Grid(rows, cols)
  grid.walls = []
  while len(grid.walls) < walls:
    cp = uRandom.rand_point(rows - 1, cols - 1)
    if cp not in grid.walls:
      grid.walls.append(cp)
  while 1:
    start = uRandom.rand_point(rows - 1, cols - 1)
    if start not in grid.walls:
      break
  while 1:
    goal = uRandom.rand_point(rows - 1, cols - 1)
    if goal not in grid.walls and goal != start:
      break
  return grid, start, goal
