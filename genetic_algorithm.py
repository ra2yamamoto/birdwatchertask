from apply_rules_to_trials import *
import numpy as np

MIN_ANIMALS_PER_BLOCK = 5;
MAX_ANIMALS_PER_BLOCK = 12;
POP_SIZE = 50
MAX_GENERATIONS = 500

int_letter_map = {
  0: "a",
  1: "b",
  2: "c",
  3: "d"
}

facing_map = {
  0: "L",
  1: "R"
}

def random_trial(vary_facing):
  if vary_facing:
    return int_letter_map[np.random.randint(0, 4)] + facing_map[np.random.randint(0, 2)]
  else:
    return int_letter_map[np.random.randint(0, 4)]

def generate_random_trials(vary_facing=False):
  n = np.random.randint(MIN_ANIMALS_PER_BLOCK, MAX_ANIMALS_PER_BLOCK)
  return [random_trial(vary_facing) for _ in range(n)]

def cross_over(mom, dad, vary_facing=False):
  n = np.random.randint(MIN_ANIMALS_PER_BLOCK, MAX_ANIMALS_PER_BLOCK)
  trials = []
  parents = [mom, dad]

  for i in range(n):
    p = parents[np.random.randint(0, 2)]
    if i < len(p):
      trials.append(p[i])
    else:
      trials.append(random_trial(vary_facing))
  
  if np.random.random() < 0.05:
    np.random.shuffle(trials)

  return trials

def longest_a_sequence(trials):
  max_counter = 0
  counter = 0
  for i in range(1, len(trials)):
    if trials[i] == 'a' and trials[i - 1] == 'a':
      counter += 1
      max_counter = max(max_counter, counter)
    else:
      counter = 0
  return max_counter

def fitness(rule_set, trials, rule_name=None):
  # returns (perfect match, fitness)
  reached = sum(
    sum(1 if t > 0 else 0 for t in r) 
    for r in states_and_transitions_reached(rule_set, trials))
  desired = count_states_and_transitions(rule_set)
  if rule_name == "sequence with negation":
    # special case, check for sequences longer than two
    reached -= 1 if longest_a_sequence(trials) > 1 else 0
  return (desired == reached, reached)

def generate_trials(rule_set, rule_name=None, pop_size=50, vary_facing=False, verbose=False):
  generation = 1
  population = [generate_random_trials(vary_facing=vary_facing) for _ in range(pop_size)]

  # main loop
  while generation <= MAX_GENERATIONS:
    fitnesses = []

    for individual in population:
      (perfect_match, f) = fitness(rule_set, individual, rule_name=rule_name)
      if perfect_match:
        if verbose: print(f"Trial sequence generated in {generation} generations")
        return individual
      else:
        fitnesses.append(f)

    index_and_fitness = list(zip(range(len(population)), fitnesses))
    index_and_fitness.sort(key=lambda a: a[1])

    dead_set = []
    alive_set = []

    death_prob = [(i, 1 - f / pop_size) for (i, f) in index_and_fitness]

    for i, p in death_prob:
      if np.random.random() < p:
        dead_set.append(i)
      else:
        alive_set.append(i)

    rescue_size= pop_size // 2
    if len(alive_set) < 2:
      # rescue population, take top half
      dead_set = [i for i, _ in index_and_fitness[rescue_size:]]
      alive_set = [i for i, _ in index_and_fitness[:rescue_size]]
    
    for i in dead_set:
      population[i] = None
    
    for i in range(len(population)):
      if population[i] == None:
        mom = population[alive_set[np.random.randint(0, len(alive_set))]]
        dad = population[alive_set[np.random.randint(0, len(alive_set))]]
        population[i] = cross_over(mom, dad)

    generation += 1
  else:
    print("No match found")

  return None