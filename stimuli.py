from psychopy import core, event
from image_container import ImageContainer
from helpers import StimulusType, Color, random_color_except_no_generator, random_color_no_generator, color_to_str

color_map = {
  Color.BLUE: "blue",
  Color.RED: "red",
  Color.GREEN: "green",
  Color.YELLOW: "yellow"
}

MAX_STIM_DURATION = 5 # in secs

# Fixation
class Fixation: 
  def __init__(self, container: ImageContainer) -> None: # takes preloaded image and window objects
    self.container = container

  def run(self, t=0.5) -> None:
    self.container.fixation.draw()
    self.container.window.flip()
    core.wait(t)

def maybe(p, e):
  if p != None:
    return e
  else:
    return p

class StimulusResponse:
  def __init__(self, time_out: bool, correct: bool, did_photo: bool, should_photo: bool, stim_color: Color, stim_left: bool, stroop: bool, swapped: bool, response_time: float, frames: int, refresh_rate: float, stroop_color: Color) -> None:
    self.time_out = time_out
    self.correct = correct

    self.did_photo = did_photo
    self.should_photo = should_photo
    self.stim_color = stim_color
    self.stim_left = stim_left

    self.stroop = stroop
    self.stroop_color = stroop_color
    self.swapped = swapped

    self.response_time = response_time
    self.frames = frames

    self.refresh_rate = refresh_rate
  
  def convert_to_dict(self):
    return {
      "time_out": self.time_out,
      "user_action": maybe(self.did_photo, "PHOTO" if self.did_photo else "SKIP"),
      "correct_action": maybe(self.should_photo, "PHOTO" if self.should_photo else "SKIP"),
      "stimulus_color": color_to_str(self.stim_color),
      "stroop_bird_color": color_to_str(self.stroop_color) if self.stroop else "NA",
      "facing_direction": "L" if self.stim_left else "R",
      "stroop": self.stroop,
      "inputs_swapped": self.swapped,
      "reaction_time": self.response_time
      # "reaction_time_frames": self.frames,
      # "reaction_time_ms": self.frames * self.refresh_rate
    }

# Stimulus class
class Stimulus:
  def __init__(self, color: Color, photograph: bool, container: ImageContainer, type: StimulusType=StimulusType.BIRD, facing_right=False, stroop=False, swapped=False) -> None:
    self.type = type
    self.color = color
    self.photograph = photograph
    self.container = container
    self.timer = core.Clock() # init clock as well
    self.facing_right = facing_right
    self.stroop = stroop
    self.swapped = swapped

    if self.facing_right:
      self.image = self.container.birds_facing_right[self.color]
    else:
      if self.type == StimulusType.BIRD:
        self.image = self.container.birds[self.color]
      elif self.type == StimulusType.SNAKE:
        self.image = self.container.snakes[self.color]
      elif self.type == StimulusType.SPIDER:
        self.image = self.container.spiders[self.color]

  def run(self) -> StimulusResponse: # blocks thread
    # Steps:
    #   Display stimulus
    #   While the time hasn't elapsed, record key presses
    #   Return stimulus response

    response = False # was a response given
    correct = None # was the participant correct
    t = None # time taken to respond

    did_photo = None # did the user photograph?

    random_color = None if not self.stroop else random_color_no_generator()
    random_bird = None if not self.stroop else self.container.birds[random_color]

    frames = 1
    event.clearEvents() # clear keys
    self.timer.reset() # reset timer

    while self.timer.getTime() <= MAX_STIM_DURATION:
      if self.stroop: # could optimize here
        random_bird.draw()
        self.container.stroop[self.color].color = color_map[random_color]
        self.container.stroop[self.color].draw()
      else:
        self.image.draw()
      self.container.window.flip()

      keys = event.getKeys(keyList=['q', 'p', 'escape']) # listen only for these keys

      if keys:
        t = self.timer.getTime();
        if keys[0] == 'escape': # escape should end experiment (TODO: implement)
          break
        response = True
        did_photo = (keys[0] == 'p') ^ self.swapped
        correct = self.photograph == ((keys[0] == 'p') ^ self.swapped) # XOR flips value of keys[0] == 'p' if reverse_keys is true
        break
      frames += 1
    
    if response: # show feedback
      if not self.stroop:
        self.image.draw()
      else:
        random_bird.draw()

      if correct: 
        self.container.correct_feedback_stim.draw()
      else:
        self.container.wrong_feedback_stim.draw()

      self.container.window.flip()
      core.wait(0.5)

    return StimulusResponse(
      not response, 
      correct, 
      did_photo, 
      self.photograph, 
      self.color, 
      not self.facing_right, 
      self.stroop, 
      self.swapped, 
      t, 
      frames, 
      self.container.window.monitorFramePeriod, 
      random_color)