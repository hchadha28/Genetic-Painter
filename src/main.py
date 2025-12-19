import yaml

from src.ga.population import initialize_population
from src.ga.evolve import evolve

from src.render.renderer import Renderer
from src.fitness.combined import combined_fitness
from src.utils.image_io import load_image


def main():

    print("Starting Evolution Phase...")

    # load GA config
    with open("config/ga.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    pop_size      = cfg["population_size"]
    generations   = cfg["generations"]
    mutation_rate = cfg["mutation_rate"]
    tournament_k  = cfg["tournament_k"]
    elite_size    = cfg["elitism"]

    # load target image
    target = load_image("data/target/target.jpg")

    renderer = Renderer()

    # generate initial population
    population = initialize_population(pop_size)

    for gen in range(generations):

        # render each individual
        rendered_images = [
            renderer.render(individual)
            for individual in population
        ]

        # compute fitness for each rendered image
        fitness_values = [
            combined_fitness(img, target)
            for img in rendered_images
        ]

        # evolve population for next generation
        population = evolve(
            population,
            fitness_values,
            pop_size,
            tournament_k,
            mutation_rate,
            elite_size,
        )

        # report progress (best score)
        print(f"Generation {gen}: best fitness = {min(fitness_values)}")


if __name__ == "__main__":
    main()
