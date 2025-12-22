import random
import copy
import math  # <--- Required for length calculations
from src.ga.population import generate_random_stroke
from src.genome.constraints import (
    MIN_STROKES, MAX_MUTATION_STROKES, 
    THICKNESS_MAX, THICKNESS_MIN,
    MAX_LENGTH, MIN_LENGTH
)

def _clamp_stroke_length(stroke):
    """
    Helper function to force a stroke's length to stay within bounds.
    It preserves the angle/direction but adjusts x2/y2.
    """
    dx = stroke.x2 - stroke.x1
    dy = stroke.y2 - stroke.y1
    dist = math.sqrt(dx**2 + dy**2)

    # Edge case: If points are identical (length 0), force a tiny length
    if dist == 0:
        stroke.x2 += MIN_LENGTH
        dist = MIN_LENGTH
        dx = stroke.x2 - stroke.x1

    # If too short, extend vector
    if dist < MIN_LENGTH:
        scale = MIN_LENGTH / dist
        stroke.x2 = int(stroke.x1 + (dx * scale))
        stroke.y2 = int(stroke.y1 + (dy * scale))

    # If too long, shorten vector
    elif dist > MAX_LENGTH:
        scale = MAX_LENGTH / dist
        stroke.x2 = int(stroke.x1 + (dx * scale))
        stroke.y2 = int(stroke.y1 + (dy * scale))

def mutate(individual, mutation_rate):

    # --- 1. Existing Coordinate Mutation (Fine-tuning)
    for stroke in individual.strokes:
        if random.random() < mutation_rate:
            # Randomly shift points
            stroke.x1 += random.randint(-5, 5)
            stroke.y1 += random.randint(-5, 5)
            stroke.x2 += random.randint(-5, 5)
            stroke.y2 += random.randint(-5, 5)
            
            # --- FIX: Enforce Length Constraints ---
            _clamp_stroke_length(stroke)
            # ---------------------------------------

            # Constrain thickness
            stroke.thickness = min(max(stroke.thickness + random.randint(-5, 5), THICKNESS_MIN), THICKNESS_MAX)
            
            # Constrain Color
            stroke.color = (
                min(max(stroke.color[0] + random.randint(-15, 15), 0), 255),
                min(max(stroke.color[1] + random.randint(-15, 15), 0), 255),
                min(max(stroke.color[2] + random.randint(-15, 15), 0), 255),
            )
            
            # Constrain Alpha
            stroke.alpha += random.randint(-5, 5)
            stroke.alpha = min(max(stroke.alpha, 30), 180)

    # --- 2. Background Color Mutation
    if random.random() < mutation_rate:
        r, g, b = individual.bg_color
        individual.bg_color = (
            min(max(r + random.randint(-15, 15), 0), 255),
            min(max(g + random.randint(-15, 15), 0), 255),
            min(max(b + random.randint(-15, 15), 0), 255),
        )

    # --- 3. Add Stroke with 80/20 Rule
    if random.random() < mutation_rate:
        if len(individual.strokes) < MAX_MUTATION_STROKES:
            
            # 80% Chance: Clone & Jitter (Exploitation)
            if random.random() > 0.6 and len(individual.strokes) > 0:
                parent_stroke = random.choice(individual.strokes)
                new_stroke = copy.deepcopy(parent_stroke)
                
                # Jitter Position
                jitter_pos = 32
                new_stroke.x1 += random.randint(-jitter_pos, jitter_pos)
                new_stroke.y1 += random.randint(-jitter_pos, jitter_pos)
                new_stroke.x2 += random.randint(-jitter_pos, jitter_pos)
                new_stroke.y2 += random.randint(-jitter_pos, jitter_pos)
                
                # --- FIX: Enforce Length Constraints on Clone ---
                _clamp_stroke_length(new_stroke)
                # ------------------------------------------------
                
                # Jitter Color
                jitter_col = 30
                new_col_list = list(new_stroke.color)
                new_col_list[0] = min(max(new_col_list[0] + random.randint(-jitter_col, jitter_col), 0), 255)
                new_col_list[1] = min(max(new_col_list[1] + random.randint(-jitter_col, jitter_col), 0), 255)
                new_col_list[2] = min(max(new_col_list[2] + random.randint(-jitter_col, jitter_col), 0), 255)
                new_stroke.color = tuple(new_col_list)

                individual.strokes.append(new_stroke)

            # 20% Chance: Pure Random (Exploration)
            else:
                new_stroke = generate_random_stroke()
                # Assuming generate_random_stroke handles constraints internally
                # If not, you can call _clamp_stroke_length(new_stroke) here too
                individual.strokes.append(new_stroke)

    # --- 4. Delete Stroke
    if random.random() < mutation_rate:
        if len(individual.strokes) > MIN_STROKES:
            idx = random.randint(0, len(individual.strokes) - 1)
            individual.strokes.pop(idx)

    return individual