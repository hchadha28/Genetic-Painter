import random
from src.genome.individual import Individual

def crossover(parent1, parent2):
    # randomly inherit bg color
    bg_color = parent1.bg_color if random.random() < 0.5 else parent2.bg_color

    # combine strokes
    split = random.randint(0, len(parent1.strokes))

    strokes = parent1.strokes[:split] + parent2.strokes[split:]

    return Individual(bg_color, strokes)
