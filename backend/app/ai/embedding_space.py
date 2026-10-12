"""Keep vector dimensions, model provenance and storage selection consistent."""

import math
from dataclasses import dataclass
from numbers import Real

from app.ai.ports import EmbeddingProvider


class EmbeddingError(RuntimeError):
    """Safe to display: messages never include credentials or gateway responses."""


@dataclass(frozen=True)
class EmbeddingSpace:
    dimension: int
    vector_attribute: str
    profile_attribute: str
    profile: str


def space_for(embedder: EmbeddingProvider) -> EmbeddingSpace:
    attributes = {
        1536: ("embedding", "embedding_profile"),
        1024: ("embedding_1024", "embedding_1024_profile"),
    }
    if embedder.dimension not in attributes:
        raise EmbeddingError("No database column supports this embedding dimension")
    profile = getattr(embedder, "profile", None)
    if not isinstance(profile, str) or not profile or len(profile) > 80:
        raise EmbeddingError("The embedding provider must declare a valid model profile")
    return EmbeddingSpace(embedder.dimension, *attributes[embedder.dimension], profile)


def validate_vector(vector, dimension: int) -> list[float]:
    if not isinstance(vector, (list, tuple)) or len(vector) != dimension:
        raise EmbeddingError(f"The embedding gateway must return exactly {dimension} numeric values")
    if any(isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value) for value in vector):
        raise EmbeddingError("The embedding vector contains invalid numeric values")
    values = [float(value) for value in vector]
    if not any(value != 0 for value in values):
        raise EmbeddingError("The embedding vector must not be all zeros")
    return values
