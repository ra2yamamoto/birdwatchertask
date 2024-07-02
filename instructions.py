from image_container import ImageContainer
from psychopy import visual, core, event, gui
import sys

class InstructionPage:
  def __init__(self, instructions: str, container: ImageContainer, include_default=True, keys_switched=False, stroop=False, show_instructions=True) -> None:
    self.instructions = instructions
    self.include_default = include_default
    self.keys_switched = keys_switched
    self.container = container
    self.photograph_key = "P" if not keys_switched else "Q"
    self.skip_key = "Q" if not keys_switched else "P"
    self.stroop = stroop
    self.show_instructions = show_instructions
    self.time = core.Clock()

  def run(self):
    instruction_text = "Instructions: \n"
    if not self.show_instructions:
      instruction_text = ""
    stroop_text = ""
    if self.stroop:
      stroop_text = ("Now you will see the color written over the birds. Ignore the color of the birds, and only react to the word.\n\n")

    default_text = f"Press '{self.photograph_key}' to take a picture, and press '{self.skip_key}' to skip this bird\n\n"
    if not self.include_default:
      default_text = ""

    s = (instruction_text + stroop_text + default_text
         + self.instructions
         + "\n\nPress any key to continue")
    
    text_box = visual.TextBox2(self.container.window, s, color="black", size=[20, None])

    t = None
    frames = 1
    event.clearEvents()
    self.time.reset()
    while True:
      if self.keys_switched: 
        self.container.switched_text_stim.draw()
      text_box.draw()
      self.container.window.flip()

      keys = event.getKeys()
      if keys:
        if keys[0] == 'escape':
          print("Task aborted because escape pressed")
          self.container.window.close()
          core.quit()
        t = self.time.getTime()
        break
      frames += 1

    return (t, frames)

class UserInfo:
  def __init__(self) -> None:
    self.user_id = None
  def run(self):
    dialogue = gui.Dlg(title="Bird Watcher Task ID")
    dialogue.addText("Please type in the ID you have been given: *")
    dialogue.addField("id", label="ID:", required=True)
    inp = dialogue.show()

    if inp != None:
      self.user_id = inp["id"]
      return inp
    else:
      print("Input cancelled")
      return None