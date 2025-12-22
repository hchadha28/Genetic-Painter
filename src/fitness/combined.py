from src.fitness.delta_e import compute_delta_e
from src.fitness.ssim import compute_ssim
from src.fitness.euclidean import compute_euclidean

def combined_fitness(rendered_img, target_img):
    """
    Compute combined fitness score from SSIM and Delta E.

    Parameters
    ----------
    rendered_img : PIL.Image.Image
        The rendered image from an individual
    target_img : PIL.Image.Image
        The target image to match

    Returns
    -------
    float
        Combined fitness score (lower = better match)
    """
    # Weights (simple for now)
    w1 = 0.60  # weight for SSIM component
    w2 = 0.40
    # Compute metrics
    ssim_val = compute_ssim(rendered_img, target_img)
    delta_e_val = compute_delta_e(rendered_img, target_img)
    # euclidean_val = compute_euclidean(rendered_img, target_img)

    # # Combine: lower score = better (since 1-SSIM and Delta E are both lower=better)
    fitness = w1 * (1 - ssim_val) + w2 * delta_e_val
    return fitness