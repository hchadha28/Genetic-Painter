import random
from src.genome.individual import Individual
from src.genome.stroke import Stroke
from src.genome.constraints import (
    MIN_STROKES,
    MAX_STROKES,
    THICKNESS_MIN,
    THICKNESS_MAX,
    ALPHA_MIN,
    ALPHA_MAX,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)

def generate_random_stroke():
    return Stroke(
        x1=random.randint(0, CANVAS_WIDTH-1),
        y1=random.randint(0, CANVAS_HEIGHT-1),
        x2=random.randint(0, CANVAS_WIDTH-1),
        y2=random.randint(0, CANVAS_HEIGHT-1),
        thickness=random.randint(THICKNESS_MIN, THICKNESS_MAX),
        color=(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ),
        alpha=random.randint(ALPHA_MIN, ALPHA_MAX)
    )

def generate_random_individual():
    bg_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

    num_strokes = random.randint(MIN_STROKES, MAX_STROKES)
    strokes = [generate_random_stroke() for _ in range(num_strokes)]

    return Individual(bg_color, strokes)


def initialize_population(pop_size):
    return [generate_random_individual() for _ in range(pop_size)]
