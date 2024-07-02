from enum import Enum
import numpy as np

class StimulusType(Enum):
  BIRD = 0
  SNAKE = 1
  SPIDER = 2

class Color(Enum):
  BLUE = 0
  GREEN = 1
  RED = 2
  YELLOW = 3

# class ExperimentEndedEarlyException()

def color_to_str(c: Color) -> str:
  if c == Color.BLUE:
    return "BLUE"
  elif c == Color.GREEN:
    return "GREEN"
  elif c == Color.RED:
    return "RED"
  else:
    return "YELLOW"

def random_color_no_generator():
  return Color(np.random.randint(0, 4))

def random_color_except_no_generator(c):
  return np.random.choice([x for x in [Color.BLUE, Color.GREEN, Color.RED, Color.YELLOW] if x != c])