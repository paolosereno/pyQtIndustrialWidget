"""
SevenSegmentDisplay - Industrial Widget in Pure Python (PySide6 / PyQt6)
Author: Ported from QtIndustrialWidgets
"""

import sys

try:
    from PySide6.QtCore import Qt, QPointF, Property, Signal
    from PySide6.QtGui import QPainter, QColor, QPolygonF, QBrush, QPen
    from PySide6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout,
        QDoubleSpinBox, QLabel, QCheckBox, QComboBox
    )
except ImportError:
    from PyQt6.QtCore import Qt, QPointF, pyqtProperty as Property, pyqtSignal as Signal
    from PyQt6.QtGui import QPainter, QColor, QPolygonF, QBrush, QPen
    from PyQt6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout,
        QDoubleSpinBox, QLabel, QCheckBox, QComboBox
    )

# Segment layout:
#       A
#     +---+
#   F |   | B
#     +-G-+
#   E |   | C
#     +---+
#       D    (DP)
# Mask: [A, B, C, D, E, F, G]
SEGMENT_MAP = {
    '0': (1, 1, 1, 1, 1, 1, 0),
    '1': (0, 1, 1, 0, 0, 0, 0),
    '2': (1, 1, 0, 1, 1, 0, 1),
    '3': (1, 1, 1, 1, 0, 0, 1),
    '4': (0, 1, 1, 0, 0, 1, 1),
    '5': (1, 0, 1, 1, 0, 1, 1),
    '6': (1, 0, 1, 1, 1, 1, 1),
    '7': (1, 1, 1, 0, 0, 0, 0),
    '8': (1, 1, 1, 1, 1, 1, 1),
    '9': (1, 1, 1, 1, 0, 1, 1),
    '-': (0, 0, 0, 0, 0, 0, 1),
    ' ': (0, 0, 0, 0, 0, 0, 0),
    'E': (1, 0, 0, 1, 1, 1, 1),
    'r': (0, 0, 0, 0, 1, 0, 1),
    'o': (0, 0, 1, 1, 1, 0, 1),
}


class SevenSegmentDisplay(QWidget):
    valueChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = "123.4"
        self._num_digits = 5
        self._on_color = QColor(255, 140, 0)       # Default industrial amber
        self._off_color = QColor(45, 25, 0, 70)    # Ghost segment (unlit)
        self._bg_color = QColor(15, 15, 18)        # Dark matte background
        self._show_ghost_segments = True
        self._slant_angle = 8.0                     # Industrial italic slant angle (degrees)

        self.setMinimumSize(160, 60)

    # --- Getter/setter properties ---
    def getText(self) -> str:
        return self._text

    def setText(self, val: str):
        val_str = str(val)
        if self._text != val_str:
            self._text = val_str
            self.valueChanged.emit(self._text)
            self.update()

    text = Property(str, getText, setText)

    def setOnColor(self, color: QColor):
        self._on_color = QColor(color)
        # Automatically calculate unlit ghost color
        self._off_color = QColor(self._on_color.red() // 5,
                                 self._on_color.green() // 5,
                                 self._on_color.blue() // 5, 55)
        self.update()

    def setShowGhostSegments(self, show: bool):
        self._show_ghost_segments = show
        self.update()

    def setNumDigits(self, count: int):
        self._num_digits = max(1, count)
        self.update()

    # --- QPainter rendering ---
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # 1. Frame & Background
        painter.fillRect(self.rect(), self._bg_color)
        pen = QPen(QColor(50, 50, 55), 1.5)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))

        w = self.width()
        h = self.height()

        # 2. Parse characters and decimal points
        tokens = []
        i = 0
        s = self._text.strip()
        while i < len(s):
            char = s[i]
            has_dot = False
            if i + 1 < len(s) and s[i + 1] == '.':
                has_dot = True
                i += 1
            tokens.append((char, has_dot))
            i += 1

        # Right alignment with spaces
        display_slots = max(self._num_digits, len(tokens))
        padding = display_slots - len(tokens)
        full_tokens = [(' ', False)] * padding + tokens

        digit_width = w / display_slots
        digit_height = h * 0.85
        top_offset = (h - digit_height) / 2

        # 3. Draw each digit
        for idx, (ch, dot) in enumerate(full_tokens):
            x_offset = idx * digit_width
            self._draw_digit(painter, x_offset, top_offset, digit_width, digit_height, ch, dot)

    def _draw_digit(self, painter: QPainter, x: float, y: float, w: float, h: float, char: str, dot: bool):
        margin_x = w * 0.18
        margin_y = h * 0.08
        dw = w - (margin_x * 2)
        dh = h - (margin_y * 2)
        dx = x + margin_x
        dy = y + margin_y

        sw = dw * 0.15  # Segment thickness
        mask = SEGMENT_MAP.get(char, (0, 0, 0, 0, 0, 0, 0))

        painter.save()
        # Slight shear typical of 7-segment displays
        painter.translate(dx + dw / 2, dy + dh / 2)
        painter.shear(-0.10, 0.0)
        painter.translate(-(dx + dw / 2), -(dy + dh / 2))

        x0, x2 = dx, dx + dw
        y0, y1, y2 = dy, dy + dh / 2, dy + dh

        # Hexagonal-ended polygons for industrial realism
        segments = [
            # A (Top)
            QPolygonF([QPointF(x0 + sw, y0), QPointF(x2 - sw, y0),
                       QPointF(x2 - 1.5 * sw, y0 + sw), QPointF(x0 + 1.5 * sw, y0 + sw)]),
            # B (Top-Right)
            QPolygonF([QPointF(x2, y0 + sw), QPointF(x2, y1 - sw * 0.5),
                       QPointF(x2 - sw, y1 - sw), QPointF(x2 - sw, y0 + 1.5 * sw)]),
            # C (Bottom-Right)
            QPolygonF([QPointF(x2, y1 + sw * 0.5), QPointF(x2, y2 - sw),
                       QPointF(x2 - sw, y2 - 1.5 * sw), QPointF(x2 - sw, y1 + sw)]),
            # D (Bottom)
            QPolygonF([QPointF(x0 + 1.5 * sw, y2 - sw), QPointF(x2 - 1.5 * sw, y2 - sw),
                       QPointF(x2 - sw, y2), QPointF(x0 + sw, y2)]),
            # E (Bottom-Left)
            QPolygonF([QPointF(x0, y1 + sw * 0.5), QPointF(x0 + sw, y1 + sw),
                       QPointF(x0 + sw, y2 - 1.5 * sw), QPointF(x0, y2 - sw)]),
            # F (Top-Left)
            QPolygonF([QPointF(x0, y0 + sw), QPointF(x0 + sw, y0 + 1.5 * sw),
                       QPointF(x0 + sw, y1 - sw), QPointF(x0, y1 - sw * 0.5)]),
            # G (Middle)
            QPolygonF([QPointF(x0 + sw, y1), QPointF(x0 + 1.4 * sw, y1 - sw * 0.45),
                       QPointF(x2 - 1.4 * sw, y1 - sw * 0.45), QPointF(x2 - sw, y1),
                       QPointF(x2 - 1.4 * sw, y1 + sw * 0.45), QPointF(x0 + 1.4 * sw, y1 + sw * 0.45)]),
        ]

        painter.setPen(Qt.PenStyle.NoPen)

        # Draw segments A-G
        for is_active, poly in zip(mask, segments):
            if is_active:
                painter.setBrush(QBrush(self._on_color))
                painter.drawPolygon(poly)
            elif self._show_ghost_segments:
                painter.setBrush(QBrush(self._off_color))
                painter.drawPolygon(poly)

        # Draw decimal point (DP)
        dp_size = sw * 1.15
        dp_x = x2 + sw * 0.2
        dp_y = y2 - dp_size
        dp_color = self._on_color if dot else (self._off_color if self._show_ghost_segments else None)
        if dp_color:
            painter.setBrush(QBrush(dp_color))
            painter.drawEllipse(QPointF(dp_x, dp_y), dp_size / 2, dp_size / 2)

        painter.restore()


# --- Interactive demo with controls ---
def run_demo():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("QtIndustrialWidgets - SevenSegmentDisplay (Python)")
    window.resize(460, 240)
    window.setStyleSheet("background-color: #24252A; color: #E0E0E0; font-family: Segoe UI, sans-serif;")

    layout = QVBoxLayout(window)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)

    # 1. The Display
    display = SevenSegmentDisplay()
    layout.addWidget(display)

    # 2. Interactive controls
    controls_layout = QHBoxLayout()

    # Value spinner
    lbl_val = QLabel("Value:")
    spinner = QDoubleSpinBox()
    spinner.setRange(-9999.0, 99999.0)
    spinner.setValue(123.40)
    spinner.setDecimals(2)
    spinner.setStyleSheet("QDoubleSpinBox { background-color: #33353D; color: white; padding: 4px; border: 1px solid #555; }")
    spinner.valueChanged.connect(lambda v: display.setText(f"{v:.2f}"))
    controls_layout.addWidget(lbl_val)
    controls_layout.addWidget(spinner)

    # Color palette
    lbl_color = QLabel("Color:")
    color_combo = QComboBox()
    color_combo.addItems(["Amber (Industrial)", "Red (Classic LED)", "Green (Phosphor)", "Cyan (Futuristic)"])
    color_combo.setStyleSheet("QComboBox { background-color: #33353D; color: white; padding: 4px; border: 1px solid #555; }")

    color_map = {
        0: QColor(255, 140, 0),    # Amber
        1: QColor(255, 30, 30),    # Red
        2: QColor(50, 255, 80),    # Green
        3: QColor(0, 230, 255),    # Cyan
    }
    color_combo.currentIndexChanged.connect(lambda idx: display.setOnColor(color_map[idx]))
    controls_layout.addWidget(lbl_color)
    controls_layout.addWidget(color_combo)

    layout.addLayout(controls_layout)

    # Additional options
    options_layout = QHBoxLayout()
    ghost_chk = QCheckBox("Show unlit segments (Ghost)")
    ghost_chk.setChecked(True)
    ghost_chk.toggled.connect(display.setShowGhostSegments)
    options_layout.addWidget(ghost_chk)

    layout.addLayout(options_layout)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_demo()
