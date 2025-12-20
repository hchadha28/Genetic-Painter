import random
import copy
from src.ga.population import generate_random_stroke
from src.genome.constraints import MIN_STROKES, MAX_STROKES

def mutate(individual, mutation_rate):

    # --- 1. Existing Coordinate Mutation (Fine-tuning)
    for stroke in individual.strokes:
        if random.random() < mutation_rate:
            stroke.x1 += random.randint(-1, 1)
            stroke.y1 += random.randint(-1, 1)
            stroke.x2 += random.randint(-1, 1)
            stroke.y2 += random.randint(-1, 1)
            # Constrain thickness between 1 and 4
            stroke.thickness = min(max(stroke.thickness + random.randint(-1, 1), 1), 4)
            stroke.color = (
                min(max(stroke.color[0] + random.randint(-5, 5), 0), 255),
                min(max(stroke.color[1] + random.randint(-5, 5), 0), 255),
                min(max(stroke.color[2] + random.randint(-5, 5), 0), 255),
            )
            stroke.alpha += random.randint(-5, 5)
            stroke.alpha = min(max(stroke.alpha, 0), 255)

    # --- 2. Background Color Mutation
    if random.random() < mutation_rate:
        r, g, b = individual.bg_color
        individual.bg_color = (
            min(max(r + random.randint(-10, 10), 0), 255),
            min(max(g + random.randint(-10, 10), 0), 255),
            min(max(b + random.randint(-10, 10), 0), 255),
        )

    # --- 3. NEW: Add Stroke with 80/20 Rule
    if random.random() < mutation_rate:
        if len(individual.strokes) < MAX_STROKES:
            
            # 80% Chance: Clone & Jitter (Exploitation)
            # (Only possible if we actually have strokes to copy)
            if random.random() > 0.2 and len(individual.strokes) > 0:
                parent_stroke = random.choice(individual.strokes)
                new_stroke = copy.deepcopy(parent_stroke)
                
                # Jitter Position (move slightly)
                jitter_pos = 2
                new_stroke.x1 += random.randint(-jitter_pos, jitter_pos)
                new_stroke.y1 += random.randint(-jitter_pos, jitter_pos)
                new_stroke.x2 += random.randint(-jitter_pos, jitter_pos)
                new_stroke.y2 += random.randint(-jitter_pos, jitter_pos)
                
                # Jitter Color (shift slightly)
                jitter_col = 15
                new_col_list = list(new_stroke.color)
                new_col_list[0] = min(max(new_col_list[0] + random.randint(-jitter_col, jitter_col), 0), 255)
                new_col_list[1] = min(max(new_col_list[1] + random.randint(-jitter_col, jitter_col), 0), 255)
                new_col_list[2] = min(max(new_col_list[2] + random.randint(-jitter_col, jitter_col), 0), 255)
                new_stroke.color = tuple(new_col_list)

                individual.strokes.append(new_stroke)

            # 20% Chance: Pure Random (Exploration)
            else:
                new_stroke = generate_random_stroke()
                individual.strokes.append(new_stroke)

    # --- 4. Delete Stroke
    if random.random() < mutation_rate:
        if len(individual.strokes) > MIN_STROKES:
            idx = random.randint(0, len(individual.strokes) - 1)
            individual.strokes.pop(idx)

    return individual