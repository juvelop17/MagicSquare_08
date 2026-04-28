"""U-RED-01: reject non-4x4 inputs at boundary."""

from __future__ import annotations

import pytest

from magicsquare.boundary import validate


def test_validate_raises_when_grid_is_not_4x4() -> None:
    bad_grid = [
        [16, 2, 3],
        [5, 11, 10],
    ]

    with pytest.raises(ValueError, match="4x4"):
        validate(bad_grid)
