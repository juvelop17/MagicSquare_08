"""FR-02 ~ FR-05: 빈칸·누락 수·두 고정 시도."""

from __future__ import annotations

import copy
from typing import Optional

from magic_square.entity.constants import GRID_SIZE
from magic_square.entity.magic import is_magic_square_complete


def find_empty_cells_1indexed(grid: list[list[int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """INV 만족 그리드에서 row-major 순 빈칸 두 개 좌표 (1-index)."""

    positions: list[tuple[int, int]] = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                positions.append((r + 1, c + 1))
    assert len(positions) == 2
    return positions[0], positions[1]


def missing_pair_sorted(grid: list[list[int]]) -> tuple[int, int]:
    """1~16 중 비어 있는 두 수를 (n_small, n_large) 로 반환."""

    present: set[int] = set()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            v = grid[r][c]
            if v != 0:
                present.add(v)
    missing = [x for x in range(1, 17) if x not in present]
    assert len(missing) == 2
    missing.sort()
    return missing[0], missing[1]


def solve_valid_grid(grid: list[list[int]]) -> Optional[tuple[int, int, int, int, int, int]]:
    """유효 입력 그리드에 대해 성공 시 int[6] (1-index 좌표·값), 불가 시 None."""

    base = copy.deepcopy(grid)
    (r1, c1), (r2, c2) = find_empty_cells_1indexed(base)
    n_small, n_large = missing_pair_sorted(base)
    ir1, ic1, ir2, ic2 = r1 - 1, c1 - 1, r2 - 1, c2 - 1

    def trial(a: int, b: int) -> bool:
        g = copy.deepcopy(base)
        g[ir1][ic1] = a
        g[ir2][ic2] = b
        return is_magic_square_complete(g)

    if trial(n_small, n_large):
        return (r1, c1, n_small, r2, c2, n_large)
    if trial(n_large, n_small):
        return (r1, c1, n_large, r2, c2, n_small)
    return None
