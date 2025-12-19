def apply_elitism(population, fitness_values, elite_size):
    paired = list(zip(population, fitness_values))
    paired.sort(key=lambda x: x[1])  # lower score = better
    elites = [ind for ind, score in paired[:elite_size]]
    return elites
