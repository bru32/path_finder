# math_util

__author__ = "Bruce Wernick"
__date__ = "20 August 2021"

__all__ = ['linear_range']


def linear_range(start_value, end_value, step_count):
  """ linear range from x0 to x1 in n steps. """
  arr = []
  step_size = (end_value - start_value) / (step_count - 1)
  value = 1.0 * start_value
  while value <= end_value:
    arr.append(round(value, 6))
    value += step_size
  return arr


# ---------------------------------------------------------------------

if __name__ == "__main__":

  print(linear_range(10, 20, 11))
