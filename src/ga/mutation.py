import random
import copy
import math 
from src.ga.population import generate_random_stroke
from src.genome.constraints import (
    MIN_STROKES, MAX_MUTATION_STROKES, 
    THICKNESS_MAX, THICKNESS_MIN,
    MAX_LENGTH, MIN_LENGTH, ALPHA_MAX, ALPHA_MIN
)

def _clamp_stroke_length(stroke):
    """
    Helper function to force a stroke's length to stay within bounds.
    """
    dx = stroke.x2 - stroke.x1
    dy = stroke.y2 - stroke.y1
    dist = math.sqrt(dx**2 + dy**2)

    if dist == 0:
        stroke.x2 += MIN_LENGTH
        dist = MIN_LENGTH
        dx = stroke.x2 - stroke.x1

    if dist < MIN_LENGTH:
        scale = MIN_LENGTH / dist
        stroke.x2 = int(stroke.x1 + (dx * scale))
        stroke.y2 = int(stroke.y1 + (dy * scale))

    elif dist > MAX_LENGTH:
        scale = MAX_LENGTH / dist
        stroke.x2 = int(stroke.x1 + (dx * scale))
        stroke.y2 = int(stroke.y1 + (dy * scale))

def mutate(individual, mutation_rate):
    """
    Performs exactly ONE type of mutation with equal probability.
    options: [Modify Existing Stroke, Modify Background, Add Stroke, Delete Stroke]
    """
    
    # Define the possible moves
    options = ['modify_stroke', 'modify_bg', 'add_stroke', 'delete_stroke','split_stroke']
    # options = [ 'modify_bg', 'add_stroke', 'delete_stroke']
    # Pick one action
    action = random.choice(options)

    # --- ACTION 1: MODIFY ONE EXISTING STROKE ---
    if action == 'modify_stroke':
        if len(individual.strokes) > 0:
            # Pick ONE random stroke to modify (instead of looping through all)
            stroke = random.choice(individual.strokes)
            
            # Jitter Points
            stroke.x1 += random.randint(-1, 1)
            stroke.y1 += random.randint(-1, 1)
            stroke.x2 += random.randint(-1, 1)
            stroke.y2 += random.randint(-1, 1)
            
            # Enforce constraints
            _clamp_stroke_length(stroke)
            stroke.thickness = min(max(stroke.thickness + random.randint(-2, 2), THICKNESS_MIN), THICKNESS_MAX)
            
            # Jitter Color
            stroke.color = (
                min(max(stroke.color[0] + random.randint(-5, 5), 0), 255),
                min(max(stroke.color[1] + random.randint(-5, 5), 0), 255),
                min(max(stroke.color[2] + random.randint(-5, 5), 0), 255),
            )
            
            # Jitter Alpha
            stroke.alpha += random.randint(-5, 5)
            stroke.alpha = min(max(stroke.alpha, ALPHA_MIN), ALPHA_MAX)
        else:
            # Fallback: If no strokes exist, switch to 'add_stroke'
            action = 'add_stroke' 

    # --- ACTION 2: MODIFY BACKGROUND ---
    if action == 'modify_bg':
        r, g, b = individual.bg_color
        individual.bg_color = (
            min(max(r + random.randint(-5, 5), 0), 255),
            min(max(g + random.randint(-5, 5), 0), 255),
            min(max(b + random.randint(-5, 5), 0), 255),
        )

    # --- ACTION 3: ADD STROKE ---
    if action == 'add_stroke':
        if len(individual.strokes) < MAX_MUTATION_STROKES:
            
            # 80% Chance: Clone & Jitter (Exploitation)
            if random.random() > 0.3 and len(individual.strokes) > 0:
                parent_stroke = random.choice(individual.strokes)
                new_stroke = copy.deepcopy(parent_stroke)
                
                # Jitter Position
                jitter_pos = 10
                new_stroke.x1 += random.randint(-jitter_pos, jitter_pos)
                new_stroke.y1 += random.randint(-jitter_pos, jitter_pos)
                new_stroke.x2 += random.randint(-jitter_pos, jitter_pos)
                new_stroke.y2 += random.randint(-jitter_pos, jitter_pos)
                
                _clamp_stroke_length(new_stroke)
                
                # Jitter Color/Alpha slightly
                new_stroke.alpha = min(max(new_stroke.alpha + random.randint(-5, 5), ALPHA_MIN), ALPHA_MAX)
                
                # Insert at random depth (Painter's Algorithm Fix)
                insert_idx = random.randint(0, len(individual.strokes))
                individual.strokes.insert(insert_idx, new_stroke)

            # 20% Chance: Pure Random (Exploration)
            else:
                new_stroke = generate_random_stroke()
                # Ensure random strokes also obey length limits
                _clamp_stroke_length(new_stroke)
                
                insert_idx = random.randint(0, len(individual.strokes))
                individual.strokes.insert(insert_idx, new_stroke)

    # --- ACTION 4: DELETE STROKE ---
    if action == 'delete_stroke':
        if len(individual.strokes) > MIN_STROKES:
            idx = random.randint(0, len(individual.strokes) - 1)
            individual.strokes.pop(idx)
    # --- ACTION 5: SPLIT STROKE (Refining) ---
    if action == 'split_stroke':
        if len(individual.strokes) < MAX_MUTATION_STROKES and len(individual.strokes) > 0:
            # Pick a random stroke
            idx = random.randint(0, len(individual.strokes) - 1)
            parent = individual.strokes[idx]
            
            # Only split if it's long enough
            dx = parent.x2 - parent.x1
            dy = parent.y2 - parent.y1
            length = (dx**2 + dy**2)**0.5
            
            if length > MIN_LENGTH * 2:
                # Calculate Midpoint
                mid_x = (parent.x1 + parent.x2) // 2
                mid_y = (parent.y1 + parent.y2) // 2
                
                # Create Child A (Start -> Mid)
                child_a = copy.deepcopy(parent)
                child_a.x2, child_a.y2 = mid_x, mid_y
                # Fix length/clamping
                _clamp_stroke_length(child_a)
                
                # Create Child B (Mid -> End)
                child_b = copy.deepcopy(parent)
                child_b.x1, child_b.y1 = mid_x, mid_y
                _clamp_stroke_length(child_b)
                
                # Replace Parent with Child A, insert Child B right after
                individual.strokes[idx] = child_a
                individual.strokes.insert(idx + 1, child_b)
    return individual