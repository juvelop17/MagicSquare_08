"""Boundary validation for external input."""

from __future__ import annotations

from magic_square.boundary.api import CompletionError, complete_magic_square
from magicsquare.constants import MATRIX_SIZE

GRID_SIZE_ERROR_MESSAGE = f"Grid must be {MATRIX_SIZE}x{MATRIX_SIZE}."


def _ensure_grid_shape(grid: list[list[int]]) -> None:
    if len(grid) != MATRIX_SIZE:
        raise ValueError(GRID_SIZE_ERROR_MESSAGE)
    if any(len(row) != MATRIX_SIZE for row in grid):
        raise ValueError(GRID_SIZE_ERROR_MESSAGE)


def validate(grid: list[list[int]]) -> None:
    """Validate input matrix shape for the 4x4 contract."""
    _ensure_grid_shape(grid)


def solve(grid: list[list[int]]) -> list[int]:
    """Delegate solving to domain flow and return int[6]."""
    result = complete_magic_square(grid)
    if isinstance(result, CompletionError):
        raise ValueError(result.message)
    return list(result.values)
