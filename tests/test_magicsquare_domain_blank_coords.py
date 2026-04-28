"""L-RED-01: row-major blank coordinate detection."""

from __future__ import annotations

from magicsquare.domain import find_blank_coords


def test_find_blank_coords_returns_two_blanks_in_row_major_order() -> None:
    grid = [
        [16, 2, 0, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 0, 15, 1],
    ]

    assert find_blank_coords(grid) == ((1, 3), (4, 2))
