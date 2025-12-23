from src.fitness.delta_e import compute_delta_e
from src.fitness.ssim import compute_ssim
from src.fitness.euclidean import compute_euclidean

def combined_fitness(rendered_img, target_img,decay):
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
    # # Weights (simple for now)
    # w1 = min(max(decay,0.1),0.9)  # weight for SSIM component
    # w2 = 1 - w1
    w1 = 0.2
    w2 = 0.8
    # Compute metrics
    
    if decay >= 0.7:
        w1  = 0.5
        w2 = 0.5
    
    ssim_val = compute_ssim(rendered_img, target_img)
    delta_e_val = compute_delta_e(rendered_img, target_img)
    # euclidean_val = compute_euclidean(rendered_img, target_img)

    # # Combine: lower score = better (since 1-SSIM and Delta E are both lower=better)
    fitness = w1 * (1 - ssim_val) + w2 * delta_e_val
    return fitness