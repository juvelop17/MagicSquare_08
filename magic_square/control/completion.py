"""도메인 완성만 조율 — 입력은 이미 FR-01 통과한 것만 받는다."""

from __future__ import annotations

import copy
from typing import Union

from magic_square.prd_messages import MSG_E_DOMAIN
from magic_square.entity.solver import solve_valid_grid


def run_domain_completion(grid: list[list[int]]) -> Union[tuple[str, str], tuple[int, int, int, int, int, int]]:
    """검증된 그리드만 처리. 성공 시 6튜플, 도메인 불가 시 (E_DOMAIN, message)."""

    snapshot = copy.deepcopy(grid)
    outcome = solve_valid_grid(snapshot)
    if outcome is None:
        return ("E_DOMAIN", MSG_E_DOMAIN)
    return outcome
