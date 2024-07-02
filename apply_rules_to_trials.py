def count_states_and_transitions(rule_set): # rule_set is a list of rules (containing states + transitions) as structured in the JSON file
  # return total no. of transitions and targets (including targets we transition on)
  if any("startCondition" in rule for rule in rule_set):
    # assume no transitions for startConditions in this case, only because we only use that case (not necessarily true always)
    return 1
  else:
    return sum(("target" in rule) 
               + ("transitionToRule" in rule) 
               + ("transitionOnTarget" in rule) 
              for rule in rule_set)

def single_target_matches(target, index, trials): # not correct in all use cases
  # check to see if a target string matches a specific trial (given by index)
  if target == "*": 
    return True
  elif index >= len(trials):
    return False

  target_index = 0
  negate = False

  # ! only negates the color, not the direction
  if target[0] == "!":
    negate = True
    target_index += 1

  target_color = target[target_index]
  target_direction = target[target_index + 1] if target_index + 1 < len(target) else None

  if target[target_index].isnumeric(): # resolve ordinal
    target_color = trials[int(target[target_index]) - 1][0]
  
  trial_color = trials[index][0]
  trial_direction = trials[index][1] if len(trials[index]) > 1 else None

  return (((target_color == trial_color) ^ negate) 
          and (trial_direction == target_direction if target_direction else True))

def sequence_target_matches(target_seq, index, trials):
  # check to see if a sequence of target strings matches a sequence of trials starting at index
  if len(target_seq) == 1:
    return single_target_matches(target_seq[0], index, trials)
  elif len(target_seq) == 0:
    return False
  else:
    for i, t in enumerate(target_seq):
      if not single_target_matches(t, i + index, trials):
        return False
  return True

def states_and_transitions_reached(rule_set, trials):
  # this could be made cleaner, but it works for our use cases
  # run the trial_set through the FSA described in rule_set, 
  # tracking the number of times each state or transition is satisfied

  # transform the list of rules into a list of lists
  # one element for each target, transition and transition_target
  # fill out this table with the number of rules reached

  # each sublist represents [target, transition on target, transition]
  tracker = [[0, 0, 0] for _ in rule_set]

  start_conditions = [rule for rule in rule_set if "startCondition" in rule]

  if start_conditions:
    # match all the starting conditions
    current_rule_index = 0
    for sc in start_conditions:
      if sequence_target_matches(sc["startCondition"], 0, trials):
        for i in range(len(sc["startCondition"]) - 1, len(trials)):
          # if we match the current target

          if "target" in sc:
            if sequence_target_matches(sc["target"], i, trials):
              tracker[current_rule_index][0] += 1
              if "transitionToRule" in sc and not "transitionOnTarget" in sc:
                tracker[current_rule_index][2] += 1
                current_rule_index = sc["transitionToRule"]
            elif "transitionOnTarget" in sc:
              if sequence_target_matches(sc["transitionOnTarget"], i, trials):
                tracker[current_rule_index][1] += 1
                tracker[current_rule_index][2] += 1
                current_rule_index = sc["transitionToRule"] # we assume it's there in this case
        break
  else:
    current_rule_index = 0
    for i in range(len(trials)):
      # if we match the current target

      if "target" in rule_set[current_rule_index]:
        if sequence_target_matches(rule_set[current_rule_index]["target"], i, trials):
          tracker[current_rule_index][0] += 1
          if "transitionToRule" in rule_set[current_rule_index] and not "transitionOnTarget" in rule_set[current_rule_index]:
            tracker[current_rule_index][2] += 1
            current_rule_index = rule_set[current_rule_index]["transitionToRule"]
        elif "transitionOnTarget" in rule_set[current_rule_index]:
          if sequence_target_matches(rule_set[current_rule_index]["transitionOnTarget"], i, trials):
            tracker[current_rule_index][1] += 1
            tracker[current_rule_index][2] += 1
            current_rule_index = rule_set[current_rule_index]["transitionToRule"] # we assume it's there in this case
  
  return tracker

def evaluate_fsa_on_trials(rule_set, trials):
  # run an fsa on a trial, annotating each trial with photograph or don't photograph (True/False)
  # code could be cleaner

  photograph_or_not = [False] * len(trials)

  start_conditions = [(i, rule) for i, rule in enumerate(rule_set) if "startCondition" in rule]

  if start_conditions:
    for i, sc in start_conditions:
      start_target = sc["startCondition"]
      if sequence_target_matches(start_target, 0, trials):
        current_rule_index = i
        trial_i = len(start_target) - 1

        while trial_i < len(trials):
          if "target" in rule_set[current_rule_index]:
            current_target = rule_set[current_rule_index]["target"]
            if sequence_target_matches(current_target, trial_i, trials):
              # advance by that many and photograph
              trial_i += len(current_target) - 1
              photograph_or_not[trial_i] = True
              if "transitionToRule" in rule_set[current_rule_index] and not "transitionOnTarget" in rule_set[current_rule_index]:
                current_rule_index = rule_set[current_rule_index]["transitionToRule"]
            elif "transitionOnTarget" in rule_set[current_rule_index]:
              transition_target = rule_set[current_rule_index]["transitionOnTarget"]
              if sequence_target_matches(transition_target, trial_i, trials):
                current_rule_index = rule_set[current_rule_index]["transitionToRule"]
                # trial_i += len(transition_target) - 1
          trial_i += 1
        break
  else:
    current_rule_index = 0
    trial_i = 0

    while trial_i < len(trials):
      if "target" in rule_set[current_rule_index]:
        current_target = rule_set[current_rule_index]["target"]
        if sequence_target_matches(current_target, trial_i, trials):
          # advance by that many and photograph
          trial_i += len(current_target) - 1
          photograph_or_not[trial_i] = True
          if "transitionToRule" in rule_set[current_rule_index] and not "transitionOnTarget" in rule_set[current_rule_index]:
            current_rule_index = rule_set[current_rule_index]["transitionToRule"]
        elif "transitionOnTarget" in rule_set[current_rule_index]:
          transition_target = rule_set[current_rule_index]["transitionOnTarget"]
          if sequence_target_matches(transition_target, trial_i, trials):
            current_rule_index = rule_set[current_rule_index]["transitionToRule"]
            # trial_i += len(transition_target) - 1
            trial_i -= 1 # re-evaluate this one
      trial_i += 1
  
  return photograph_or_not