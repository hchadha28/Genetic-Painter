import random
import copy
from src.genome.individual import Individual
from src.genome.constraints import CANVAS_WIDTH

def crossover(parent1, parent2):
    # 1. Randomly inherit background color
    bg_color = parent1.bg_color if random.random() < 0.5 else parent2.bg_color

    # 2. Pick a random vertical line to cut the canvas
    split_x = random.randint(0, CANVAS_WIDTH)

    child_strokes = []

    # 3. Inherit "Left Side" strokes from Parent 1
    for stroke in parent1.strokes:
        # Calculate the horizontal center of the stroke
        center_x = (stroke.x1 + stroke.x2) // 2
        
        # If it sits on the left of the cut, keep it
        if center_x < split_x:
            child_strokes.append(copy.deepcopy(stroke))

    # 4. Inherit "Right Side" strokes from Parent 2
    for stroke in parent2.strokes:
        center_x = (stroke.x1 + stroke.x2) // 2
        
        # If it sits on the right of the cut, keep it
        if center_x >= split_x:
            child_strokes.append(copy.deepcopy(stroke))

    return Individual(bg_color, child_strokes)