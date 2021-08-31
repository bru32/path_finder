# Priority Queue using Python's heapq

__author__ = 'Bruce Wernick'
__date__ = '29 August 2021'


import heapq


class PQueue:

  """ Priority Queue using python heapq """

  def __init__(self):
    self.elements = []

  def empty(self):
    return not self.elements

  def put(self, item, priority):
    heapq.heappush(self.elements, (priority, item))

  def get(self):
    return heapq.heappop(self.elements)[1]
