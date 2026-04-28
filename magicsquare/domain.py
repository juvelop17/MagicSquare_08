"""Domain rules for 4x4 magic square."""

from __future__ import annotations

from magicsquare.constants import EMPTY_VALUE, MATRIX_SIZE

REQUIRED_BLANK_CELLS = 2
BLANK_COUNT_ERROR_MESSAGE = "Grid must contain exactly two blank cells."


def _collect_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    blanks: list[tuple[int, int]] = []
    for row_idx in range(MATRIX_SIZE):
        for col_idx in range(MATRIX_SIZE):
            if grid[row_idx][col_idx] == EMPTY_VALUE:
                blanks.append((row_idx + 1, col_idx + 1))
    return blanks


def find_blank_coords(
    grid: list[list[int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return two blank coordinates in row-major order (1-indexed)."""
    blanks = _collect_blank_coords(grid)

    if len(blanks) != REQUIRED_BLANK_CELLS:
        raise ValueError(BLANK_COUNT_ERROR_MESSAGE)

    return blanks[0], blanks[1]
