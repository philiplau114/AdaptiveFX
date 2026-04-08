"""
Population management for the Genetic Algorithm in AdaptiveFX.

The ``Population`` class owns the collection of :class:`Individual` candidates
and coordinates selection, crossover, and mutation across generations to
drive the GA towards better-performing strategy parameter sets.
"""

from __future__ import annotations

from loguru import logger

from optimizer.genetic_algorithm.individual import Individual
from optimizer.genetic_algorithm.operators import (
    crossover,
    mutate,
    select_tournament,
)
from config.settings import settings


class Population:
    """Manages a generation of strategy parameter candidates.

    Attributes:
        individuals: Current list of Individual instances.
        param_space: Strategy PARAM_SPACE shared by all individuals.
        generation: Current generation counter.
    """

    def __init__(self, param_space: dict[str, dict]) -> None:
        self.param_space = param_space
        self.individuals: list[Individual] = []
        self.generation: int = 0

    # ------------------------------------------------------------------
    def initialize(self, size: int = settings.GA_POPULATION_SIZE) -> None:
        """Create the initial population with randomly generated individuals.

        Args:
            size: Number of individuals in the population.
        """
        # TODO: Create ``size`` random Individual instances
        # self.individuals = [Individual(self.param_space) for _ in range(size)]
        # logger.info(f"Initialised population with {size} individuals.")
        logger.warning("initialize() not yet implemented.")
        self.individuals = [Individual(self.param_space) for _ in range(size)]

    # ------------------------------------------------------------------
    def evolve(self, fitness_scores: list[float]) -> None:
        """Apply selection, crossover, and mutation to produce the next generation.

        Args:
            fitness_scores: Fitness value for each individual in
                ``self.individuals`` (same order).
        """
        # TODO: Implement full generational evolution
        # # Assign fitness scores
        # for ind, score in zip(self.individuals, fitness_scores):
        #     ind.fitness = score
        #
        # new_population = []
        # pop_size = len(self.individuals)
        # while len(new_population) < pop_size:
        #     parent1 = select_tournament(self.individuals, settings.GA_TOURNAMENT_SIZE)
        #     parent2 = select_tournament(self.individuals, settings.GA_TOURNAMENT_SIZE)
        #     child1, child2 = crossover(parent1, parent2, settings.GA_CROSSOVER_PROB)
        #     child1 = mutate(child1, settings.GA_MUTATION_PROB, self.param_space)
        #     child2 = mutate(child2, settings.GA_MUTATION_PROB, self.param_space)
        #     new_population.extend([child1, child2])
        #
        # self.individuals = new_population[:pop_size]
        # self.generation += 1
        # logger.info(f"Generation {self.generation} complete. "
        #             f"Best fitness: {max(fitness_scores):.4f}")
        logger.warning("evolve() not yet implemented.")
        for ind, score in zip(self.individuals, fitness_scores):
            ind.fitness = score
        self.generation += 1

    # ------------------------------------------------------------------
    def get_best(self) -> Individual | None:
        """Return the individual with the highest fitness score.

        Returns:
            Best-performing Individual, or None if the population is empty.
        """
        # TODO: Return the individual with the maximum fitness
        # if not self.individuals:
        #     return None
        # return max(self.individuals, key=lambda ind: ind.fitness)
        logger.warning("get_best() not yet implemented.")
        if not self.individuals:
            return None
        return max(self.individuals, key=lambda ind: ind.fitness)

    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self.individuals)

    def __repr__(self) -> str:
        best = self.get_best()
        return (
            f"Population(gen={self.generation}, size={len(self)}, "
            f"best_fitness={best.fitness:.4f if best else 'N/A'})"
        )
