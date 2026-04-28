"""FR-01: 호출자 행렬 스키마 검증."""

from __future__ import annotations

from typing import Optional

from magic_square.prd_messages import (
    MSG_E_DUPLICATE,
    MSG_E_EMPTY_COUNT,
    MSG_E_SIZE,
    MSG_E_VALUE_RANGE,
)
from magic_square.entity.constants import GRID_SIZE


def validate_grid_structure(grid: list[list[int]]) -> Optional[tuple[str, str]]:
    """규약 위반 시 (code, message), 통과 시 None."""

    if not isinstance(grid, list) or len(grid) != GRID_SIZE:
        return ("E_SIZE", MSG_E_SIZE)
    for row in grid:
        if not isinstance(row, list) or len(row) != GRID_SIZE:
            return ("E_SIZE", MSG_E_SIZE)

    zeros = 0
    nonzero_values: list[int] = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            v = grid[r][c]
            if not isinstance(v, int):
                return ("E_VALUE_RANGE", MSG_E_VALUE_RANGE)
            if v == 0:
                zeros += 1
            elif 1 <= v <= 16:
                nonzero_values.append(v)
            else:
                return ("E_VALUE_RANGE", MSG_E_VALUE_RANGE)

    if zeros != 2:
        return ("E_EMPTY_COUNT", MSG_E_EMPTY_COUNT)

    if len(nonzero_values) != len(set(nonzero_values)):
        return ("E_DUPLICATE", MSG_E_DUPLICATE)

    return None
