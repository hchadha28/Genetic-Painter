# Canvas size
CANVAS_WIDTH = 64
CANVAS_HEIGHT = 64

# Stroke count limits
# INCREASED: 200 is often too low to resolve fine details. 
# 400-500 gives the GA enough "budget" to fix tiny errors.
MIN_STROKES = 20
MAX_STROKES = 50
MAX_MUTATION_STROKES = 1000

# Stroke Lengths
# INCREASED MAX: Allow strokes to span the full diagonal (~90px).
# This helps establish background gradients with fewer strokes.
MIN_LENGTH = 1
MAX_LENGTH = 10  

# Stroke appearance limits
# INCREASED MAX: Allow a single stroke to cover half the screen (32px).
# This lets the GA solve "large flat areas" instantly.
THICKNESS_MIN = 1
THICKNESS_MAX = 10

# Alpha (Transparency) -- CRITICAL CHANGE
# LOWERED MIN: Allows subtle shading/tinting (glazing). 
# LOWERED MAX: Prevents a single bad stroke from destroying the image.
ALPHA_MIN = 30   # Was 120 (Too opaque)
ALPHA_MAX = 150  # Was 255 (Too destructive)