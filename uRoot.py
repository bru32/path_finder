# mini root finder

"""
Experiment with minimal root finders.
Uses args to make the error function more useful.
"""

__author__ = "Bruce Wernick"
__date__ = "31 August 2021"


import sys

eps = sys.float_info.epsilon


def zbrac(f, x, args=()):
  """ Given range x = (x1, x2),
      expand geometrically until a root is bracketed.
      If successful, return (x1,x2) else return None.
  """
  g = 1.6
  maxi = 12
  x1, x2 = x
  if x1 == x2:
    h = 0.1
    dx = h * x1
    if abs(dx) <= eps:
      dx = h
    x2 = x1 + dx
  f1 = f(x1, *args)
  f2 = f(x2, *args)
  for _ in range(maxi):
    if f1 * f2 < 0.0:
      return x1, x2
    dx = g * (x1 - x2)
    if abs(f1) < abs(f2):
      x1 += dx
      f1 = f(x1, *args)
    else:
      x2 -= dx
      f2 = f(x2, *args)
  return None


def zbrak(f, x, n, args=()):
  """ Take n steps over given range [x0, x1].
      If root exists in step, add to list.
  """
  rb = []  # root brackets
  dx = (x[1] - x[0]) / n
  a, fa = x[0], f(x[0], *args)
  for _ in range(n-1):
    b = a + dx
    fb = f(b, *args)
    if fa * fb <= 0.0:
      rb.append((a, b))
    a, fa = b, fb
  return rb


def irq_mod(f, x, args=(), tol=1e-5, maxi=48):
  """ Solve for root by modified irq. """
  a, b = x

  fa = f(a, *args)
  if abs(fa) <= eps:
    return a

  fb = f(b, *args)
  if abs(fb) <= eps:
    return b

  i = 12
  while fa * fb > 0:
    # try to expand bracket
    if abs(fa) < abs(fb):
      a += 1.6*(a - b)
      fa = f(a, *args)
    else:
      b += 1.6*(b - a)
      fb = f(b, *args)
    i -= 1
    if i <= 0:
      raise Exception('Cannot bracket root!')

  for i in range(maxi):
    dx = b - a

    c = a + 0.5 * dx
    if abs(dx) <= tol:
      return c

    fc = f(c, *args)
    if abs(fc) <= tol:
      return c

    if fa != fc and fb != fc:
      fab, fac, fbc = fa-fb, fa-fc, fb-fc
      s = a*fc*fb/fac/fab + c*fa*fb/fac/fbc - b*fa*fc/fab/fbc
    else:
      s = a + dx * fb / (fa - fb)

    fs = f(s, *args)
    if abs(fs) <= tol:
      return s

    if fc * fs < 0:
      a, fa = c, fc
      b, fb = s, fs

    elif fa * fc < 0:
      b, fb = c, fc

    elif fs * fb < 0:
      a, fa = s, fs

  raise Exception("Max its reached!")


def dydx(f, x, args=()):
  """ Function and Slope. """
  fx = f(x, *args)
  h = 1e-4
  dx = h * x
  if dx < eps:
    dx = h
  h = x + dx
  fh = f(h, *args)
  return fx, (fh-fx) / (h-x)


def dxdy(f, x, args=()):
  """f(x) and slope inverse dx/df
  """
  e = 0.1
  xo = x
  fo = f(xo, *args)
  h = e * abs(xo)
  if h <= eps:
    h = e
  x = xo + h
  fx = f(x, *args)
  return fo, (x-xo) / (fx-fo)


def newt(f, x, args=(), tol=1e-5, maxi=48):
  """ Root find by Newton-Raphson. """
  for i in range(maxi):
    xo = x
    fx, dfx = dydx(f, x, args)
    if abs(dfx) < eps:
      raise Exception('Curve too flat!')
    x -= fx / dfx
    if abs(x - xo) < tol * (1 + abs(x)):
      return x
  raise Exception("Max its reached!")


def broydn1(f, x, args=(), tol=1e-6, maxi=96):
  """ Method derived from multi-dim Broyden method.
      The reason is to not be forced to bracket the root.
      Also, it does not need a slope function.  The slope
      is updated at each iteration.
  """
  fo, k = dxdy(f, x, args)
  if abs(fo) <= tol:
    return x
  for i in range(maxi):
    dx = -k * fo
    x += dx
    fx = f(x, *args)
    if abs(fx) <= tol:
      return x
    dfx = fx - fo
    if abs(dfx) <= eps:
      return x
    a = dx * k * dfx
    dk = -k * (a - dx * dx) / a
    k += dk
    fo = fx
  raise Exception("Max its reached!")


# ---------------------------------------------------------------------

def test_irq_mod():

  def efunc(x, a, b):
    return (x + a) * (x + b)

  args = (-3, 5)
  guess = (1, 5)
  root = irq_mod(efunc, guess, args=args)
  print(f"irq_mod: {root=:0.6f}")


def test_broydn():

  def efunc(x, a, b):
    """ Return function value and slope at x.
        Roots are -a and -b (3, -5).
    """
    return (x + a) * (x + b)

  # solve with starting guess
  guess_x = 1.0
  root = broydn1(efunc, guess_x, args=(-3, 5))
  print(f"broydn: {root=:0.4f}")


def test_newt():
  """ example of using newt root finder """

  def efunc(x, a, b):
    """ Return function value and slope at x.
        Roots are -a and -b (3, -5).
    """
    return (x + a) * (x + b)

  # solve with starting guess
  guess_x = 1.0
  root = newt(efunc, guess_x, args=(-3, 5))
  print(f"newt: {root=:0.4f}")


# --------------------------------------------------------------------------

if __name__ == "__main__":

  test_newt()
  test_broydn()
  test_irq_mod()
