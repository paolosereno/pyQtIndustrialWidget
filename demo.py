#!/usr/bin/env python3
"""
Interactive demonstration and visual test for pyQtIndustrialWidget.

This script instantiates several industrial instrumentation widgets,
arranges them in a control panel layout, and interconnects their signals
and slots (e.g. rotating the knob simultaneously updates the radial dial,
the linear bar gauge, the digital seven-segment display, and triggers
the high-threshold alarm LED).
"""

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

# Import widgets from pyQtIndustrialWidget
from pyQtIndustrialWidget import (
    IndustrialKnob,
    LedIndicator,
    LinearGauge,
    RadialGauge,
    SevenSegmentDisplay,
)


class IndustrialControlPanel(QMainWindow):
    """Main window displaying an interactive industrial instrument panel."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("pyQtIndustrialWidget - Interactive Showcase")
        self.resize(750, 520)

        # Central widget and main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Header title and instructions
        header_label = QLabel(
            "<h2>Industrial Instrumentation Showcase</h2>"
            "<p style='color: #888;'>Rotate the control knob below to observe real-time "
            "synchronization across instruments.</p>"
        )
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        # Instrumentation display area
        instruments_group = QGroupBox("Instruments Readout")
        instruments_layout = QGridLayout(instruments_group)
        instruments_layout.setSpacing(16)

        # 1. Radial Dial Gauge
        self.radial_gauge = RadialGauge()
        self.radial_gauge.setRange(0.0, 100.0)
        self.radial_gauge.setUnit("BAR")
        self.radial_gauge.setValue(25.0)
        instruments_layout.addWidget(self.radial_gauge, 0, 0)

        # 2. Linear Bar Gauge
        self.linear_gauge = LinearGauge()
        self.linear_gauge.setRange(0.0, 100.0)
        self.linear_gauge.setValue(25.0)
        instruments_layout.addWidget(self.linear_gauge, 0, 1)

        # 3. Seven Segment Digital Display
        self.segment_display = SevenSegmentDisplay()
        self.segment_display.setDigitCount(5)
        self.segment_display.setDecimalPlaces(1)
        self.segment_display.setValue(25.0)
        instruments_layout.addWidget(self.segment_display, 0, 2)

        main_layout.addWidget(instruments_group, stretch=2)

        # Operator Controls area
        controls_group = QGroupBox("Operator Controls & Status")
        controls_layout = QHBoxLayout(controls_group)
        controls_layout.setSpacing(24)

        # 4. Industrial Control Knob
        self.knob = IndustrialKnob()
        self.knob.setRange(0.0, 100.0)
        self.knob.setValue(25.0)
        controls_layout.addWidget(self.knob, stretch=1)

        # 5. Threshold Alarm LED Indicator
        self.alarm_led = LedIndicator()
        self.alarm_led.setLabelText("HIGH THRESHOLD (> 75 BAR)")
        self.alarm_led.setOnColor(QColor(240, 40, 40))   # Bright warning red
        self.alarm_led.setOffColor(QColor(50, 15, 15))  # Dark standby red
        self.alarm_led.setOn(False)
        controls_layout.addWidget(self.alarm_led, stretch=1)

        main_layout.addWidget(controls_group, stretch=1)

        # Connect signals and slots for interactive feedback
        self._connect_signals()

    def _connect_signals(self):
        """Wire widget signals to update all connected displays simultaneously."""
        self.knob.valueChanged.connect(self._on_knob_value_changed)

    def _on_knob_value_changed(self, value: float):
        """Handle setpoint changes from the rotary control knob."""
        # Synchronize gauge instruments
        self.radial_gauge.setValue(value)
        self.linear_gauge.setValue(value)
        self.segment_display.setValue(value)

        # Illuminate high-pressure warning LED when value exceeds 75.0
        is_alarm_triggered = value > 75.0
        self.alarm_led.setOn(is_alarm_triggered)


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    window = IndustrialControlPanel()
    window.show()
    print("Application launched successfully.")
    print("Rotate the knob with your mouse to interact with the widgets.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
