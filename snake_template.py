# tkinter snake demo

__author__ = "Bruce Wernick"
__date__ = "22 August 2021"


import tkinter as tk
from random import randint, choice
from collections import deque


def hex_to_rgb(value):
  hex = value.lstrip('#')
  r,g,b = tuple(int(hex[i: i+2], 16) for i in (0, 2, 4))
  return (r,g,b)

def rgb_to_hex(r, g, b):
  return f'#{r:02x}{g:02x}{b:02x}'

def rgb_lerp(a, b, f):
  r = int(a[0] + f * (b[0] - a[0]))
  g = int(a[1] + f * (b[1] - a[1]))
  b = int(a[2] + f * (b[2] - a[2]))
  return (r, g, b)


def hex_lerp(a, b, f):
  a = hex_to_rgb(a)
  b = hex_to_rgb(b)
  rgb = rgb_lerp(a, b, f)
  return rgb_to_hex(*rgb)

# ---------------------------------------------------------------------


dirs = ('Left', 'Up', 'Right', 'Down')

# pause control
control = False

# key buffer
buffer = deque()

class Snake(tk.Frame):

  def __init__(self, parent):
    super().__init__(parent)
    fw, fh = 600, 600
    dx, dy = 25, 25
    self.fwidth = fw
    self.fheight = fh
    self.dx = dx
    self.dy = dy
    self.nx = fw // dx
    self.ny = fh // dy
    self.x0, self.x1 = 0, fw
    self.y0, self.y1 = 0, fh

    self.bind_all("<Key>", self.key_pressed)

    # score
    self.text = tk.StringVar()
    self.text.set("Score:")
    self.label = tk.Label(self, textvariable=self.text, font="Tahoma, 12")
    self.label.place(relx=0.5, rely=0.97, anchor=tk.CENTER)

    # drawing canvas
    self.canvas = tk.Canvas(self,
      width=fw, height=fh, bg="#384a51")

    self.canvas.bind_all("<space>", self.space_bar)

    self.draw_grid()

    self.x = self.nx // 2
    self.y = self.ny // 2
    self.dir = 'Right'
    self.tail = []
    self.ntail = 3 # starting tail
    self.score = 0
    self.move_food()
    self.canvas.place(x=20, y=20)
    self.pack(fill=tk.BOTH, expand=1)

  def draw_grid(self):
    x0, x1 = self.x0, self.x1
    y0, y1 = self.y0, self.y1
    dx, dy = self.dx, self.dy
    color = "#41565f"
    x = x0 + dx
    while x < x1:
      coords = x, y0, x, y1
      self.canvas.create_line(coords, width=1, fill=color)
      x += dx
    y = y0 + dy
    while y < y1:
      coords = x0, y, x1, y
      self.canvas.create_line(coords, width=1, fill=color)
      y += dy

  def key_pressed(self, e):
    """key pressed event
    """
    key = e.keysym
    if key in dirs:
      buffer.append(key)

  def move_snake(self):
    wrap = 0
    limit = 1
    edge = wrap

    # take step
    if self.dir == 'Right': self.x += 1
    elif self.dir == 'Up': self.y -= 1
    elif self.dir == 'Left': self.x -= 1
    elif self.dir == 'Down': self.y += 1

    if edge == wrap:
      if self.x < 0: self.x = self.nx - 1
      if self.y < 0: self.y = self.ny - 1
      if self.x > self.nx - 1: self.x = 0
      if self.y > self.ny - 1: self.y = 0
    elif edge == limit:
      if self.x < 0: self.x = 0
      if self.y < 0: self.y = 0
      if self.x > self.nx - 1: self.x = self.nx - 1
      if self.y > self.ny - 1: self.y = self.ny - 1

    # assign current point
    cp = (self.x, self.y)

    # check for crash
    if cp in self.tail:
      self.score -= 0.5
      self.text.set(f"Score: {self.score:0.0f}")

    # check food
    elif (cp == self.food) or (self.food in self.tail):

      if self.score > 10:
        self.score += 1.2
      else:
        self.score += 1

      self.text.set(f"Score: {self.score:0.0f}")
      self.ntail += 1
      self.move_food()

    # add to tail
    self.tail.append(cp)
    if len(self.tail) > self.ntail:
      self.tail = self.tail[1:self.ntail+1]

  def move_food(self):
    """ Randomly place food at free area
    """

    # try simple random
    x = randint(0, self.nx-1)
    y = randint(0, self.ny-1)
    cp = (x,y)
    if cp not in self.tail:
      self.food = cp
      return

    # pick from a list of available spaces
    # make list of available cells
    spaces = []
    for r in range(self.ny):
      for c in range(self.nx):
        cp = c,r
        if cp not in self.tail:
          spaces.append(cp)

    if len(spaces) == 0:
      print('Cannot find a place for the new food!')
      app.destroy()

    # place food in random spot
    self.food = choice(spaces)

  def draw_snake(self):
    g = 2
    dx = self.dx
    dy = self.dy
    for i, cp in enumerate(self.tail):
      x = cp[0] * dx
      y = cp[1] * dy
      if i == self.ntail - 1:
        color = "#ff0804"
      else:
        color = hex_lerp("#b89000", "#a82a00", i/(self.ntail-1))
      coords = x+g, y+g, x+dx-g, y+dy-g
      self.canvas.create_rectangle(coords, width=1,
        outline="#593408", fill=color, tag="snake")

  def draw_food(self):
    self.canvas.delete("food")
    g = 2
    dx = self.dx
    dy = self.dy
    x = self.food[0] * dx
    y = self.food[1] * dy
    coords = x+g, y+g, x+dx-g, y+dy-g
    self.canvas.create_rectangle(coords, width=1,
      outline="#593408", fill="green", tag="food")

  def space_bar(self, e):
    """pause animation
    """
    global control
    control = not control
    if control:
      print('press <space> to continue.')

  def animloop(self):
    """animation loop
    """
    if control:
      self.after(1000, self.animloop)
    else:
      if buffer:
        self.dir = buffer.popleft()
      self.canvas.delete("snake")
      self.move_snake()
      self.draw_snake()
      self.draw_food()
      self.after(200, self.animloop)


# ---------------------------------------------------------------------

if __name__ == "__main__":

  app = tk.Tk()
  app.title("tkinter Snake")
  app.geometry('640x680+880+50')
  app.resizable(False, False)
  snake = Snake(app)
  app.after(10, snake.animloop)
  app.mainloop()
