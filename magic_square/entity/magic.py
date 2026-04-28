"""완전 채워진 4×4 그리드에 대한 마방진 판정."""

from magic_square.entity.constants import GRID_SIZE, MAGIC_CONSTANT


def is_magic_square_complete(grid: list[list[int]]) -> bool:
    """모든 셀이 1~16일 때 행·열·두 주 대각선 합이 MAGIC_CONSTANT 인지 판정."""

    n = GRID_SIZE
    expected = MAGIC_CONSTANT
    for i in range(n):
        if sum(grid[i][j] for j in range(n)) != expected:
            return False
    for j in range(n):
        if sum(grid[i][j] for i in range(n)) != expected:
            return False
    if sum(grid[i][i] for i in range(n)) != expected:
        return False
    if sum(grid[i][n - 1 - i] for i in range(n)) != expected:
        return False
    return True
