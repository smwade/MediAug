"""Base transform classes: Transform ABC, Compose, OneOf."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from mediaug._types import CellSample


class Transform(ABC):
    """Abstract base class for all transforms.

    Every transform accepts a ``CellSample`` and a ``numpy.random.Generator``
    and returns a new ``CellSample``.  The ``p`` parameter controls the
    probability that the transform is actually applied.
    """

    def __init__(self, p: float = 1.0) -> None:
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"p must be in [0, 1], got {p}")
        self.p = p

    def __call__(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        if rng.random() < self.p:
            return self.apply(sample, rng)
        return sample

    @abstractmethod
    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(p={self.p})"


class Compose(Transform):
    """Apply a sequence of transforms in order."""

    def __init__(self, transforms: list[Transform]) -> None:
        super().__init__(p=1.0)
        self.transforms = transforms

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        for t in self.transforms:
            sample = t(sample, rng)
        return sample

    def __repr__(self) -> str:
        lines = [f"  {t!r}," for t in self.transforms]
        body = "\n".join(lines)
        return f"Compose([\n{body}\n])"


class OneOf(Transform):
    """Randomly pick one transform from a list and apply it."""

    def __init__(self, transforms: list[Transform], p: float = 1.0) -> None:
        super().__init__(p=p)
        self.transforms = transforms

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        t = self.transforms[rng.integers(len(self.transforms))]
        return t.apply(sample, rng)

    def __repr__(self) -> str:
        lines = [f"  {t!r}," for t in self.transforms]
        body = "\n".join(lines)
        return f"OneOf([\n{body}\n], p={self.p})"
