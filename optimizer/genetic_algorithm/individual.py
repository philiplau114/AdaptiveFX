"""
Gene encoding and decoding for trading strategy parameters in AdaptiveFX.

Each ``Individual`` represents a candidate solution in the Genetic Algorithm
population.  Strategy parameters are encoded as a flat list of genes, where
each gene position corresponds to a specific parameter defined in a strategy's
``PARAM_SPACE``.
"""

from __future__ import annotations

import random
from typing import Any

from loguru import logger


class GeneType:
    """Gene type constants."""

    INT = "int"
    FLOAT = "float"
    BOOL = "bool"


class Individual:
    """Encodes and decodes a set of strategy parameters as a gene list.

    Attributes:
        genes: Flat list of gene values (int, float, or bool).
        param_space: Strategy PARAM_SPACE dictionary defining gene structure.
        fitness: Scalar fitness value assigned after evaluation (default 0.0).
    """

    def __init__(
        self,
        param_space: dict[str, dict],
        genes: list[Any] | None = None,
    ) -> None:
        self.param_space = param_space
        self.fitness: float = 0.0
        self.genes: list[Any] = genes if genes is not None else self._random_genes()

    # ------------------------------------------------------------------
    def _random_genes(self) -> list[Any]:
        """Generate a random gene list within the param_space bounds.

        Returns:
            List of randomly initialised gene values.
        """
        # TODO: Generate random genes based on param_space types and ranges
        # genes = []
        # for key, spec in self.param_space.items():
        #     gene_type = spec.get("type", GeneType.FLOAT)
        #     low, high = spec["min"], spec["max"]
        #     if gene_type == GeneType.INT:
        #         genes.append(random.randint(int(low), int(high)))
        #     elif gene_type == GeneType.FLOAT:
        #         genes.append(random.uniform(low, high))
        #     elif gene_type == GeneType.BOOL:
        #         genes.append(random.choice([True, False]))
        # return genes
        logger.warning("_random_genes() not yet implemented — using defaults.")
        return [spec["default"] for spec in self.param_space.values()]

    # ------------------------------------------------------------------
    def decode(self) -> dict[str, Any]:
        """Decode the gene list back into a parameter dictionary.

        Returns:
            Dictionary mapping parameter names to gene values.
        """
        # TODO: Zip param_space keys with genes
        # return dict(zip(self.param_space.keys(), self.genes))
        logger.warning("decode() not yet implemented.")
        return dict(zip(self.param_space.keys(), self.genes))

    # ------------------------------------------------------------------
    @classmethod
    def from_params(
        cls, param_space: dict[str, dict], params: dict[str, Any]
    ) -> "Individual":
        """Create an Individual from an existing parameter dictionary.

        Args:
            param_space: Strategy PARAM_SPACE definition.
            params: Parameter dictionary to encode.

        Returns:
            New Individual with genes encoded from ``params``.
        """
        # TODO: Encode params dict into gene list ordering
        # genes = [params[key] for key in param_space.keys()]
        # return cls(param_space=param_space, genes=genes)
        logger.warning("from_params() not yet implemented.")
        genes = [params.get(key, spec["default"]) for key, spec in param_space.items()]
        return cls(param_space=param_space, genes=genes)

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return f"Individual(fitness={self.fitness:.4f}, genes={self.decode()})"
