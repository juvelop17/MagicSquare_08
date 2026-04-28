"""MagicSquare 4x4 dual-track package."""

from magicsquare.boundary import solve, validate
from magicsquare.domain import find_blank_coords

__all__ = ["find_blank_coords", "solve", "validate"]
