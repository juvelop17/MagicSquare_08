"""공개 API — 테스트·CLI 공통 진입점."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from magic_square.boundary.validator import validate_grid_structure
from magic_square.control.completion import run_domain_completion


@dataclass(frozen=True)
class CompletionSuccess:
    """성공 시 int[6] — BR-07 좌표 1-index."""

    values: tuple[int, int, int, int, int, int]


@dataclass(frozen=True)
class CompletionError:
    """계약 오류 또는 E_DOMAIN."""

    code: str
    message: str


def complete_magic_square(grid: list[list[int]]) -> Union[CompletionSuccess, CompletionError]:
    """부분 4×4 격자를 완성 규칙에 따라 처리한다."""

    err = validate_grid_structure(grid)
    if err is not None:
        code, msg = err
        return CompletionError(code=code, message=msg)

    raw = run_domain_completion(grid)
    if len(raw) == 2:
        code, msg = raw
        return CompletionError(code=code, message=msg)
    return CompletionSuccess(values=tuple(raw))
