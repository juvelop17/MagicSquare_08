"""Domain rules for 4x4 magic square."""

from __future__ import annotations

from magicsquare.constants import EMPTY_VALUE, MATRIX_SIZE


def find_blank_coords(
    grid: list[list[int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return two blank coordinates in row-major order (1-indexed)."""
    blanks: list[tuple[int, int]] = []
    for row_idx in range(MATRIX_SIZE):
        for col_idx in range(MATRIX_SIZE):
            if grid[row_idx][col_idx] == EMPTY_VALUE:
                blanks.append((row_idx + 1, col_idx + 1))

    if len(blanks) != 2:
        raise ValueError("Grid must contain exactly two blank cells.")

    return blanks[0], blanks[1]
