"""PyQt6 screen layer for MagicSquare MVP."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from magicsquare.boundary import solve, validate
from magicsquare.constants import MATRIX_SIZE


class MagicSquareWindow(QMainWindow):
    """MVP screen for entering a 4x4 grid and solving it."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MagicSquare 4x4 Solver")
        self._inputs: list[list[QSpinBox]] = []
        self._result_label = QLabel("Result: [r1, c1, n1, r2, c2, n2]")
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        for row_idx in range(MATRIX_SIZE):
            row_inputs: list[QSpinBox] = []
            for col_idx in range(MATRIX_SIZE):
                cell = QSpinBox()
                cell.setRange(0, MATRIX_SIZE * MATRIX_SIZE)
                cell.setValue(0)
                cell.setSingleStep(1)
                grid_layout.addWidget(cell, row_idx, col_idx)
                row_inputs.append(cell)
            self._inputs.append(row_inputs)

        button_row = QHBoxLayout()
        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_solve_clicked)  # type: ignore[arg-type]
        button_row.addWidget(solve_button)

        layout.addLayout(grid_layout)
        layout.addLayout(button_row)
        layout.addWidget(self._result_label)

        root.setLayout(layout)
        self.setCentralWidget(root)

    def _read_grid(self) -> list[list[int]]:
        return [
            [self._inputs[row_idx][col_idx].value() for col_idx in range(MATRIX_SIZE)]
            for row_idx in range(MATRIX_SIZE)
        ]

    def _on_solve_clicked(self) -> None:
        grid = self._read_grid()
        try:
            validate(grid)
            values = solve(grid)
        except ValueError as exc:
            QMessageBox.warning(self, "Validation/Solve Error", str(exc))
            self._result_label.setText("Result: error")
            return

        self._result_label.setText(f"Result: {values}")


def run() -> int:
    """Run the official GUI entrypoint."""
    app = QApplication(sys.argv)
    window = MagicSquareWindow()
    window.show()
    return app.exec()
