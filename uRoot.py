# Root finder

"""
Experiment with minimal root finders.
Uses args to make the error function more useful.
"""

__author__ = "Bruce Wernick"
__date__ = "31 August 2021"


TINY = 1e-16


def within_tol(fx, dx, tol):
  """ true if fx or dx are within +- tol """
  return abs(fx) <= tol or abs(dx) <= tol


def newt(f, x, args=(), maxi=24, tol=1e-5):
  """ Newton root finder """
  for i in range(maxi):
    xo = x
    fx, dfx = f(x, *args)
    if abs(dfx) <= TINY:
      raise Exception('Curve too flat!')
    x -= fx / dfx
    if within_tol(fx, x - xo, tol):
      return x
  raise Exception('Maxits reached!')


# ---------------------------------------------------------------------

def test_newt():
  """ example of using newt root finder """

  def test_func(x, a, b):
    """ Return function value and slope at x.
        Roots are -a and -b (3, -5).
    """
    return (x + a) * (x + b), 2 * x + a + b

  # solve with starting guess
  guess_x = 1.0
  root = newt(test_func, guess_x, args=(-3, 5))
  print(f"{root=:0.4f}")


if __name__ == "__main__":

  test_newt()
