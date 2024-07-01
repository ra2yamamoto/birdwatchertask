from generate_trial_sequences import generate_group, block_data
from instructions import InstructionPage, UserInfo
from pandas import DataFrame

class Task:
  def __init__(self, container) -> None:
    self.groups = []
    self.experiment_data = None
    for i in range(len(block_data)):
      self.groups.append((i, generate_group(i, container)))

    # for i in range(3, 4):
    #   self.groups.append((i, generate_group(i, container)))

    explanation1 = ("A scientist is looking for patterns in the migration of birds. "
      "Your job is to help him. Birds will appear one after another, and he wants you to "
        "take a pictures when you spot a particular pattern in their sequence (for example: a "
          "red on followed by a green one.)")
    explanation2 = ("We will always tell you what pattern to look for. Every few birds, there "
        "will be a new pattern to watch for. When you spot the pattern, press your photograph "
          "button to take a picture! Otherwise press the appropriate button to skip that bird. "
            "We'll tell you which button is which on each trial. The birds can appear in any "
              "order, including several of the same colour in a row.")
    
    self.intro1 = InstructionPage(explanation1, container, include_default=False, show_instructions=False)
    self.intro2 = InstructionPage(explanation2, container, include_default=False, show_instructions=False)

    self.dataframe = None
    self.user_info = None
    self.container = container
  
  def run(self):
    self.user_info = UserInfo()
    self.user_info.run()

    if self.user_info.user_id == None or self.user_info.user_id == "":
      print("No user ID given, task aborted")
      return None
    
    self.container.window.fullscr = True

    self.intro1.run()
    self.intro2.run()
    experiment_data = []
    for i, g in self.groups:
      blocks_data = []
      for b in g:
        instruction_times, trial_results, iti, rule = b.run()
        blocks_data.append({"iti": iti, "attempts": list(zip(instruction_times, trial_results)), "rule_name": rule})
      experiment_data.append({"name": block_data[i]["name"], "data": blocks_data}) 

    self.experiment_data = experiment_data
    return experiment_data
  
  def process_data(self):
    # experiment data structure:
    # [
    #   {'name': str, 'data': [[{"iti": float, "attempts": ((float, int), [stimulus response, ...]), "rule_name": str}, ...], ...]},
    #   ...
    # ]
    # A list of dict blocks, each with a name and a data field, where each data field represents a list of block data, 
    # where each block data contains a list of attempts, where each attempt is a list of tuples pairing the time taken 
    # to read the instructions and a list of stimulus responses 
    # (not very clean, but reflects call structure in order to be efficient during the task's runtime)

    # Variables: 
    #   trial number
    #   trial attempt number
    #   trial name
    #   block number
    #   sequence name

    #   user action
    #   correct action
    #   stimulus color
    #   stimulus direction
    #   reaction time clock
    #   reaction time ms

    #   rule name*
    #   stroop
    #   swapped
    #   iti
    #   reading time clock
    #   reading time ms

    # Task-wide variables:
    #   monitor refresh rate
    #   user id

    # first, group by name
    grouped_by_name = []
    current = []

    i = 0
    while i < len(self.experiment_data):
      current = [self.experiment_data[i]]
      i += 1
      while i < len(self.experiment_data) and self.experiment_data[i]["name"] == self.experiment_data[i - 1]["name"]:
        current.append(self.experiment_data[i])
        i += 1
      grouped_by_name.append(current)
    
    total = []
    
    # nesting... :-O
    trial_no = 0
    for name_i, name_group in enumerate(grouped_by_name):
      name = name_group[0]["name"]
      for group in name_group: # each of these follows the data structure described above
        for block_data in group["data"]: 
          trial_no += 1
          for attempt_num, (instruction_time, stimuli_data) in enumerate(block_data["attempts"]):
            for i, stimulus in enumerate(stimuli_data):
              # create a dict here with all of the variables
              d = stimulus.convert_to_dict()
              d["iti"] = block_data["iti"]
              d["reading_time"] = instruction_time[0]
              # d["reading_time_frames"] = instruction_time[1]
              # d["reading_time_ms"] = instruction_time[1] * self.container.window.monitorFramePeriod
              d["group_name"] = name
              d["stimulus_num"] = i
              d["rule_name"] = block_data["rule_name"]
              d["attempt"] = attempt_num
              d["block_num"] = trial_no
              d["sequence_num"] = name_i
              total.append(d)
    
    df = DataFrame.from_dict(total)
    self.dataframe = df
  
  def save_data(self):
    self.dataframe.to_csv(f'output/{self.user_info.user_id}.csv', index=False)