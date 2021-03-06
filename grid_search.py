# Grid Search

__author__ = 'Bruce Wernick'
__date__ = '29 August 2021'


from collections import deque
from pqueue import PQueue
import uGrid


def find_path(graph, a_node, b_node, search_path=None):
  """ recursive path find (by Guido van Rossum) """

  if search_path:
    path = search_path + [a_node]
  else:
    path = [a_node]

  # check if we have reached the b_node
  if a_node == b_node:
    return path

  for np in graph.neighbors(a_node):
    if np not in path:
      new_path = find_path(graph, np, b_node, path)
      if new_path:
        return new_path

  return None


def find_all_paths(graph, a_node, b_node, search_path=None):

  if search_path:
    path = search_path + [a_node]
  else:
    path = [a_node]

  if a_node == b_node:
    return [path]

  paths = []
  for np in graph.neighbors(a_node):
    if np not in path:
      new_paths = find_all_paths(graph, np, b_node, path)
      for new_path in new_paths:
        paths.append(new_path)

  return paths


def find_shortest_path(graph, a_node, b_node, search_path=None):

  if search_path:
    path = search_path + [a_node]
  else:
    path = [a_node]

  if a_node == b_node:
    return path

  shortest = None
  for np in graph.neighbors(a_node):
    if np not in path:
      new_path = find_shortest_path(graph, np, b_node, path)
      if new_path:
        if not shortest or len(new_path) < len(shortest):
          shortest = new_path

  return shortest


def flatten(arr):
  flat = []
  for row in arr:
    flat += row
  return flat


def shortest_path(graph, a_node, b_node):
  """ code by Eryk Kopczynski """
  front = deque()
  front.append(a_node)
  came_from = {a_node: [a_node]}
  while front:
    cp = front.popleft()
    for np in graph.neighbors(cp):
      if np not in came_from:
        front.append(np)
        came_from[np] = [came_from[cp], np]

  """flatten added by Bruce Wernick. This is purely cosmetic and not ideal.
     It looks like the came_from dict is storing unnecessary information!
  """
  return flatten(came_from.get(b_node))


def fsp(graph, a_node, b_node):
  """ Simplified Kopczynski code (actually, it turns out
      to be pretty much the same as Patel's Depth First
      Search), except for the early exit.
  """
  front = deque()
  front.append(a_node)
  came_from = {a_node: None}
  while front:
    cp = front.popleft()
    for np in graph.neighbors(cp):
      if np not in came_from:
        front.append(np)
        came_from[np] = cp
  return make_path(came_from, a_node, b_node)


# ---------------------------------------------------------------------

# Iterative searches (by Amit Patel)

def make_path(came_from, start, goal):
  """ retrace breadcrumbs to reconstruct path """
  cp = goal
  path = []
  while cp != start:
    path.append(cp)
    if cp in came_from:
      cp = came_from[cp]
    else:
      return []
  path.append(start)
  path.reverse()
  return path


def bfs_search(graph, a_node, b_node):
  """ Iterative path find based on breadth first search """
  front = deque()
  front.append(a_node)
  came_from = {a_node: None}
  while front:
    cp = front.popleft()
    if cp == b_node:
      break  # early exit
    for np in graph.neighbors(cp):
      if np not in came_from:
        front.append(np)
        came_from[np] = cp
  return make_path(came_from, a_node, b_node)


def dijkstra_search(graph, a_node, b_node):
  """ Dijkstra Search """
  front = PQueue()
  front.put(a_node, 0)
  came_from = {a_node: None}
  cost_so_far = {a_node: 0}
  while not front.empty():
    cp = front.get()
    if cp == b_node:
      break
    for np in graph.neighbors(cp):
      new_cost = cost_so_far.get(cp) + graph.cost(cp, np)
      if np not in cost_so_far or new_cost < cost_so_far[np]:
        cost_so_far[np] = new_cost
        k = new_cost
        front.put(np, k)
        came_from[np] = cp
  return make_path(came_from, a_node, b_node)


def heuristic(a, b):
  (x1, y1) = a
  (x2, y2) = b
  return abs(x1 - x2) + abs(y1 - y2)


def astar_search(graph, a_node, b_node):
  """ AStar search """
  front = PQueue()
  front.put(a_node, 0)
  came_from = {a_node: None}
  cost_so_far = {a_node: 0}
  while not front.empty():
    cp = front.get()
    if cp == b_node:
      break
    for np in graph.neighbors(cp):
      new_cost = cost_so_far.get(cp) + graph.cost(cp, np)
      if np not in cost_so_far or new_cost < cost_so_far[np]:
        cost_so_far[np] = new_cost
        k = new_cost + heuristic(np, b_node)
        front.put(np, k)
        came_from[np] = cp
  return make_path(came_from, a_node, b_node)


# ---------------------------------------------------------------------

def test1():
  """ example usage """
  rows = 10
  cols = 10
  walls = 19
  grid, start, goal = uGrid.rand_grid(rows, cols, walls)
  path = astar_search(grid, start, goal)
  print(path)


# ---------------------------------------------------------------------

if __name__ == "__main__":

  test1()
