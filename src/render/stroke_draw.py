
from PIL import ImageDraw
from src.genome.constraints import CANVAS_WIDTH, CANVAS_HEIGHT
from src.render.utils import clamp_coords


def draw_stroke(canvas, stroke):
    """
    Draw a single stroke on the canvas.

    Parameters
    ----------
    canvas : PIL.Image.Image
        The RGBA canvas to draw on
    stroke : Stroke
        The stroke to draw
    """
    # Clamp coordinates to canvas bounds
    x1, y1 = clamp_coords(stroke.x1, stroke.y1, CANVAS_WIDTH, CANVAS_HEIGHT)
    x2, y2 = clamp_coords(stroke.x2, stroke.y2, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Prepare color with alpha
    r, g, b = stroke.color
    fill = (r, g, b, stroke.alpha)

    # Draw the line
    draw = ImageDraw.Draw(canvas)
    draw.line([(x1, y1), (x2, y2)], fill=fill, width=stroke.thickness)
