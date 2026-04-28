"""Boundary validation for external input."""

from __future__ import annotations

from magic_square.boundary.api import CompletionError, complete_magic_square
from magicsquare.constants import MATRIX_SIZE


def validate(grid: list[list[int]]) -> None:
    """Validate input matrix shape for the 4x4 contract."""
    if len(grid) != MATRIX_SIZE:
        raise ValueError(f"Grid must be {MATRIX_SIZE}x{MATRIX_SIZE}.")

    for row in grid:
        if len(row) != MATRIX_SIZE:
            raise ValueError(f"Grid must be {MATRIX_SIZE}x{MATRIX_SIZE}.")


def solve(grid: list[list[int]]) -> list[int]:
    """Delegate solving to domain flow and return int[6]."""
    result = complete_magic_square(grid)
    if isinstance(result, CompletionError):
        raise ValueError(result.message)
    return list(result.values)
