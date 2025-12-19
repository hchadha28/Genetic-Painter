import random

def mutate(individual, mutation_rate):

    for stroke in individual.strokes:

        if random.random() < mutation_rate:
            stroke.x1 += random.randint(-3, 3)
            stroke.y1 += random.randint(-3, 3)
            stroke.x2 += random.randint(-3, 3)
            stroke.y2 += random.randint(-3, 3)

    # small color mutation for bg
    if random.random() < mutation_rate:
        r,g,b = individual.bg_color
        individual.bg_color = (
            min(max(r + random.randint(-10,10),0),255),
            min(max(g + random.randint(-10,10),0),255),
            min(max(b + random.randint(-10,10),0),255),
        )

    return individual
