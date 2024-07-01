import stimuli as stim
from image_container import ImageContainer
import instructions
from typing import List

class Block:
  def __init__(self, instructions: List[instructions.InstructionPage], container: ImageContainer, rule_name: str, iti=0.5, stimuli_groups: List[stim.Stimulus] = None) -> None:
    self.instructions = instructions
    self.fixation = stim.Fixation(container)
    self.stimuli_groups = [] if stimuli_groups == None else stimuli_groups
    self.tries = 0
    self.container = container
    self.iti = iti
    self.rule_name = rule_name

  def add_stimuli(self, s: List[stim.Stimulus]) -> None:
    self.stimuli_groups += [s]

  def run(self) -> None:
    instruction_times = []
    trial_data = []

    while self.tries < 3:
      i_t = self.instructions[self.tries].run()
      instruction_times.append(i_t)

      trial_results = []
      for s in self.stimuli_groups[self.tries]:
        self.fixation.run(t=self.iti)
        response = s.run()
        trial_results.append(response)

        if response.time_out:
          self.tries += 1
          i = instructions.InstructionPage("Timeout. Please respond faster.",
                                        self.container, include_default=False)
          i.run()
          trial_data.append(trial_results)
          break
        elif not response.correct:
          self.tries += 1
          trial_data.append(trial_results)
          break
      else: # if we successfully reach the end of the loop
        trial_data.append(trial_results)
        break
    return (instruction_times, trial_data, self.iti, self.rule_name)