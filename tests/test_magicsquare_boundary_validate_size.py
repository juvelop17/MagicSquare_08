"""U-RED-01: reject non-4x4 inputs at boundary."""

from __future__ import annotations

import pytest

from magic_square.boundary.api import CompletionError
from magicsquare.boundary import solve, validate


def test_validate_raises_when_grid_is_not_4x4() -> None:
    bad_grid = [
        [16, 2, 3],
        [5, 11, 10],
    ]

    with pytest.raises(ValueError, match="4x4"):
        validate(bad_grid)


def test_validate_raises_when_grid_row_length_is_not_4() -> None:
    bad_grid = [
        [16, 2, 3, 13],
        [5, 11, 10],
        [9, 7, 6, 12],
        [4, 14, 15, 1],
    ]

    with pytest.raises(ValueError, match="Grid must be 4x4."):
        validate(bad_grid)


def test_solve_raises_value_error_when_boundary_api_returns_completion_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_complete_magic_square(_: list[list[int]]) -> CompletionError:
        return CompletionError(code="E_DOMAIN", message="no solution")

    monkeypatch.setattr("magicsquare.boundary.complete_magic_square", fake_complete_magic_square)

    with pytest.raises(ValueError, match="no solution"):
        solve([[0, 0, 3, 13], [5, 11, 10, 8], [9, 7, 6, 12], [4, 14, 15, 1]])
