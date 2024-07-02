from psychopy import visual
from helpers import StimulusType, Color

class ImageContainer: # also contains reference to window obj
  def __init__(self, win) -> None:
    self.window = win

    self.birds = {
      Color.BLUE: visual.ImageStim(self.window, image="assets/bird-blue.png"),
      Color.GREEN: visual.ImageStim(self.window, image="assets/bird-green.png"),
      Color.RED: visual.ImageStim(self.window, image="assets/bird-red.png"),
      Color.YELLOW: visual.ImageStim(self.window, image="assets/bird-yellow.png")
    }

    self.birds_facing_right = {
      Color.BLUE: visual.ImageStim(self.window, image="assets/bird-blue-right.png"),
      Color.GREEN: visual.ImageStim(self.window, image="assets/bird-green-right.png"),
      Color.RED: visual.ImageStim(self.window, image="assets/bird-red-right.png"),
      Color.YELLOW: visual.ImageStim(self.window, image="assets/bird-yellow-right.png")
    }

    # self.snakes = {
    #   Color.BLUE: visual.ImageStim(self.window, image="assets/snake-blue.png"),
    #   Color.GREEN: visual.ImageStim(self.window, image="assets/snake-green.png"),
    #   Color.RED: visual.ImageStim(self.window, image="assets/snake-red.png"),
    #   Color.YELLOW: visual.ImageStim(self.window, image="assets/snake-yellow.png")
    # }

    # self.spiders = {
    #   Color.BLUE: visual.ImageStim(self.window, image="assets/spider-blue.png"), 
    #   Color.GREEN: visual.ImageStim(self.window, image="assets/spider-green.png"),
    #   Color.RED: visual.ImageStim(self.window, image="assets/spider-red.png"), 
    #   Color.YELLOW: visual.ImageStim(self.window, image="assets/spider-yellow.png")
    # }

    self.stroop = {
      Color.BLUE: visual.TextBox2(win=self.window, text="BLUE", color="black", bold=True, letterHeight=2.5, alignment="center"),
      Color.GREEN: visual.TextBox2(win=self.window, text="GREEN", color="black", bold=True, letterHeight=2.5, alignment="center"),
      Color.RED: visual.TextBox2(win=self.window, text="RED", color="black", bold=True, letterHeight=2.5, alignment="center"),
      Color.YELLOW: visual.TextBox2(win=self.window, text="YELLOW", color="black", bold=True, letterHeight=2.5, alignment="center")
    }

    self.fixation = visual.ImageStim(self.window, image="assets/fixation.png")

    self.correct_feedback_stim = visual.TextBox2(
      win=self.window, text="CORRECT", color="black", fillColor="white", bold=True, letterHeight=2, size=[11, 2.5], alignment="center", borderColor="black", borderWidth=2)
    self.wrong_feedback_stim = visual.TextBox2(
      win=self.window, text="WRONG", color="black", fillColor="white", bold=True, letterHeight=2, size=[11, 2.5], alignment="center", borderColor="black", borderWidth=2)

    self.switched_text_stim = visual.TextBox2(
        self.window, "The keys you must press have been switched!", color="red", letterHeight=1.2, pos=(2, 5), size=[30, None])

    self.loading = visual.TextBox2(self.window, "Please type the ID you were given into the prompt", alignment="center", color="black")