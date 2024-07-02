from genetic_algorithm import generate_trials
from apply_rules_to_trials import evaluate_fsa_on_trials
from stimuli import Stimulus
from block import Block
from instructions import InstructionPage
from helpers import Color
import json
import numpy as np

HUMAN_READABLE_COLORS = {
  Color.BLUE: "<c=blue>BLUE</c>",
  Color.RED: "<c=red>RED</c>",
  Color.GREEN: "<c=green>GREEN</c>",
  Color.YELLOW: "<c=(0.75, 0.75, 0)>YELLOW</c>",
}

data = None
with open("smaller_rules.json") as f:
  data = json.load(f)

block_data = None
with open("rule_blocks.json") as f:
  block_data = json.load(f)

def assign_color_to_trial(trial, map):
  if len(trial) < 2:
    return (map[trial[0]], False)
  else:
    return (map[trial[0]], trial[1] == 'R')

def substitute_colors_in_explanation(explanation, map, photograph_key="P"):
  # stimulus/stimuli
  # a, b, c, d
  # key_act
  # L, R

  substituted = []

  i = 0
  while i < len(explanation):
    while i < len(explanation) and explanation[i] != "{":
      substituted.append(explanation[i])
      i += 1

    if i >= len(explanation):
      break

    i += 1

    if explanation[i] in {"a", "b", "c", "d"}:
      substituted.append(HUMAN_READABLE_COLORS[map[explanation[i]]])
    elif explanation[i] == "s":
      if explanation[i + 6] == "i":
        substituted.append("birds")
      else:
        substituted.append("bird")
    elif explanation[i] == "k":
      substituted.append(photograph_key)
    elif explanation[i] in {"L", "R"}:
      if explanation[i] == "L":
        substituted.append("facing left")
      else:
        substituted.append("facing right")
    else:
      print("unrecognized var")
      return None
    
    while i < len(explanation) and explanation[i] != "}":
      i += 1
    i += 1

  return "".join(substituted)

def assign_colors(explanation, trials, swapped=False):
  vars = ["a", "b", "c", "d"]
  np.random.shuffle(vars)
  var_map = dict(zip(vars, [Color.BLUE, Color.GREEN, Color.RED, Color.YELLOW]))

  translated = [assign_color_to_trial(t, var_map) for t in trials]

  return (translated, substitute_colors_in_explanation(explanation, var_map, photograph_key="P" if not swapped else "Q"))

def generate_block(rule, container, swapped=False, stroop=False, iti=0.5):
  vf = False

  if "stimuliMirroring" in data[rule]:
    vf = data[rule]["stimuliMirroring"]

  stimuli_groups = []
  explanations = []
  for i in range(3):
    sequence = generate_trials(data[rule]["rules"], rule_name=rule, vary_facing=vf)
    photograph_sequence = evaluate_fsa_on_trials(data[rule]["rules"], sequence)
    color_sequence, exp = assign_colors(data[rule]["humanReadableExplanation"], sequence, swapped=swapped)

    stimuli_groups.append([Stimulus(color, photograph, container, facing_right=facing, stroop=stroop, swapped=swapped) 
                for (color, facing), photograph in zip(color_sequence, photograph_sequence)])
    explanations.append(exp)

    instruction_pages = [InstructionPage(e, container, stroop=stroop, keys_switched=swapped) for e in explanations]

  return Block(instruction_pages, container, rule, iti=iti, stimuli_groups=stimuli_groups)

def generate_group(rule_block_index, container):
  rule_block = block_data[rule_block_index]

  iti = rule_block["iti"] / 1000
  stroop = rule_block["stroop"] if "stroop" in rule_block else False
  swapped = rule_block["swapped"] if "swapped" in rule_block else False

  blocks = []
  for rule in rule_block["ruleOrder"]:
    blocks += [generate_block(rule, container, swapped=swapped, stroop=stroop, iti=iti)]
  
  return blocks
