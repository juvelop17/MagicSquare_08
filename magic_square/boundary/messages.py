"""PRD 메시지 재수출 — 외부 코드는 prd_messages 직접 사용 가능."""

from magic_square.prd_messages import (
    MSG_E_DOMAIN,
    MSG_E_DUPLICATE,
    MSG_E_EMPTY_COUNT,
    MSG_E_SIZE,
    MSG_E_VALUE_RANGE,
)

__all__ = [
    "MSG_E_DOMAIN",
    "MSG_E_DUPLICATE",
    "MSG_E_EMPTY_COUNT",
    "MSG_E_SIZE",
    "MSG_E_VALUE_RANGE",
]
