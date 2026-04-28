"""docs/TEST_CASES_MagicSquare_4x4.md · PRD §9.1 TP-01 ~ TP-07."""

from __future__ import annotations

import copy
from unittest.mock import patch

import pytest

from magic_square.boundary.api import (
    CompletionError,
    CompletionSuccess,
    complete_magic_square,
)
from magic_square.entity.constants import MAGIC_CONSTANT
from magic_square.prd_messages import (
    MSG_E_DOMAIN,
    MSG_E_DUPLICATE,
    MSG_E_EMPTY_COUNT,
    MSG_E_SIZE,
    MSG_E_VALUE_RANGE,
)

# --- §9.3 시드 (문서·단위 테스트 단일 출처)

SEED_A: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

EXPECTED_SEED_A: tuple[int, int, int, int, int, int] = (3, 3, 6, 4, 4, 1)

# 시도 1 실패·시도 2 성공 — PRD 시드 B (FULL 마방진 기반, Seed A와 다른 행렬)
SEED_B: list[list[int]] = [
    [16, 0, 0, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

EXPECTED_SEED_B: tuple[int, int, int, int, int, int] = (1, 2, 3, 1, 3, 2)

# 두 시도 모두 실패 — INV 만족·E_DOMAIN (무작위 탐색으로 확보한 예)
SEED_C: list[list[int]] = [
    [15, 3, 5, 8],
    [10, 2, 0, 14],
    [1, 4, 6, 7],
    [0, 9, 11, 12],
]


def _apply_solution(grid: list[list[int]], six: tuple[int, ...]) -> list[list[int]]:
    r1, c1, n1, r2, c2, n2 = six
    g = copy.deepcopy(grid)
    g[r1 - 1][c1 - 1] = n1
    g[r2 - 1][c2 - 1] = n2
    return g


def assert_principle_9_4_completed_grid(grid: list[list[int]]) -> None:
    """§9.4: 완성 그리드에서 1~16 각 한 번, 행·열·두 대각선 합 MAGIC_CONSTANT."""

    flat = [cell for row in grid for cell in row]
    assert sorted(flat) == list(range(1, 17))
    n = 4
    expected = MAGIC_CONSTANT
    for i in range(n):
        assert sum(grid[i][j] for j in range(n)) == expected
    for j in range(n):
        assert sum(grid[i][j] for i in range(n)) == expected
    assert sum(grid[i][i] for i in range(n)) == expected
    assert sum(grid[i][n - 1 - i] for i in range(n)) == expected


class TestTP01SuccessSeedA:
    """TP-01 — 정상 완성."""

    def test_returns_expected_int6_and_preserves_input(self) -> None:
        snapshot = copy.deepcopy(SEED_A)
        out = complete_magic_square(SEED_A)
        assert isinstance(out, CompletionSuccess)
        assert out.values == EXPECTED_SEED_A
        assert SEED_A == snapshot

    def test_empty_cells_row_major_and_missing_pair(self) -> None:
        """문서화된 관찰: 빈칸 (3,3)·(4,4), 누락 {1,6}."""

        positions: list[tuple[int, int]] = []
        for r in range(4):
            for c in range(4):
                if SEED_A[r][c] == 0:
                    positions.append((r + 1, c + 1))
        assert positions == [(3, 3), (4, 4)]
        missing = sorted(x for x in range(1, 17) if x not in {c for row in SEED_A for c in row})
        assert missing == [1, 6]

    def test_completed_grid_satisfies_section_9_4(self) -> None:
        filled = _apply_solution(SEED_A, EXPECTED_SEED_A)
        assert_principle_9_4_completed_grid(filled)

    def test_input_grid_not_mutated_nfr04(self) -> None:
        """NFR-04: 호출 전후 동일 원소."""

        grid = copy.deepcopy(SEED_A)
        before = copy.deepcopy(grid)
        complete_magic_square(grid)
        assert grid == before


class TestTP02TryTwoOnlySeedB:
    """TP-02 — 시도 2 성공·역순 규칙 (n1=n_large, n2=n_small)."""

    def test_expected_tuple_and_reverse_rule(self) -> None:
        out = complete_magic_square(SEED_B)
        assert isinstance(out, CompletionSuccess)
        assert out.values == EXPECTED_SEED_B
        r1, c1, n1, r2, c2, n2 = out.values
        present = {c for row in SEED_B for c in row if c != 0}
        missing = sorted(x for x in range(1, 17) if x not in present)
        assert missing == [2, 3]
        n_small, n_large = missing[0], missing[1]
        assert (n1, n2) == (n_large, n_small)

    def test_completed_magic_properties(self) -> None:
        filled = _apply_solution(SEED_B, EXPECTED_SEED_B)
        assert_principle_9_4_completed_grid(filled)


class TestTP03DomainFailureSeedC:
    """TP-03 — E_DOMAIN."""

    def test_domain_error_exact_message(self) -> None:
        out = complete_magic_square(SEED_C)
        assert isinstance(out, CompletionError)
        assert out.code == "E_DOMAIN"
        assert out.message == MSG_E_DOMAIN


class TestTP04SizeError:
    """TP-04 — E_SIZE 및 도메인 미호출."""

    def test_wrong_row_count(self) -> None:
        bad = [[16, 2, 3], [5, 11, 10]]
        out = complete_magic_square(bad)
        assert isinstance(out, CompletionError)
        assert out.code == "E_SIZE"
        assert out.message == MSG_E_SIZE

    def test_jagged_rows_domain_not_called(self) -> None:
        """열 길이 불균일."""
        bad = [[16, 2, 3, 13], [5, 11, 10, 8], [9, 7, 0], [4, 14, 15, 0]]
        with patch("magic_square.entity.solver.solve_valid_grid") as mocked:
            out = complete_magic_square(bad)
            mocked.assert_not_called()
        assert isinstance(out, CompletionError)
        assert out.code == "E_SIZE"


class TestTP05EmptyCount:
    """TP-05 — E_EMPTY_COUNT."""

    def test_single_empty_cell(self) -> None:
        grid = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 0, 12],
            [4, 14, 15, 1],
        ]
        out = complete_magic_square(grid)
        assert isinstance(out, CompletionError)
        assert out.code == "E_EMPTY_COUNT"
        assert out.message == MSG_E_EMPTY_COUNT

    def test_three_empty_cells_domain_not_called(self) -> None:
        grid = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 0, 0, 12],
            [4, 0, 15, 1],
        ]
        with patch("magic_square.entity.solver.solve_valid_grid") as mocked:
            out = complete_magic_square(grid)
            mocked.assert_not_called()
        assert isinstance(out, CompletionError)
        assert out.code == "E_EMPTY_COUNT"


class TestTP06ValueRange:
    """TP-06 — E_VALUE_RANGE."""

    def test_negative_and_overflow(self) -> None:
        neg = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, -1, 0, 12],
            [4, 14, 15, 0],
        ]
        out_n = complete_magic_square(neg)
        assert isinstance(out_n, CompletionError)
        assert out_n.code == "E_VALUE_RANGE"
        assert out_n.message == MSG_E_VALUE_RANGE

        high = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 17, 0, 12],
            [4, 14, 15, 0],
        ]
        out_h = complete_magic_square(high)
        assert isinstance(out_h, CompletionError)
        assert out_h.code == "E_VALUE_RANGE"


class TestTP07Duplicate:
    """TP-07 — E_DUPLICATE."""

    def test_duplicate_nonzero(self) -> None:
        grid = [
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 5, 0, 12],
            [4, 14, 15, 0],
        ]
        out = complete_magic_square(grid)
        assert isinstance(out, CompletionError)
        assert out.code == "E_DUPLICATE"
        assert out.message == MSG_E_DUPLICATE


class TestAC05DomainNotCalledOnBoundaryFailures:
    """AC-05 — 검증 실패 시 도메인 해 찾기 미호출."""

    def test_patch_solver_not_called_for_each_boundary_error(self) -> None:
        cases: list[list[list[int]]] = [
            [[1]],
            [
                [16, 2, 3, 13],
                [5, 11, 10, 8],
                [9, 7, 0, 12],
                [4, 14, 15, 1],
            ],
            [
                [16, 2, 3, 13],
                [5, 11, 10, 8],
                [9, -1, 0, 12],
                [4, 14, 15, 0],
            ],
            [
                [16, 2, 3, 13],
                [5, 11, 10, 8],
                [9, 5, 0, 12],
                [4, 14, 15, 0],
            ],
        ]
        for grid in cases:
            with patch("magic_square.entity.solver.solve_valid_grid") as mocked:
                complete_magic_square(grid)
                mocked.assert_not_called()
