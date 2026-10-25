"""
Basic test suite for pyQtIndustrialWidget.
Tests widget instantiation and property manipulation in a headless environment.
"""

import sys
import unittest
from PySide6.QtWidgets import QApplication

# Ensure offscreen platform plugin for headless testing environments
if QApplication.instance() is None:
    app = QApplication(sys.argv[:1] + ["-platform", "offscreen"])
else:
    app = QApplication.instance()

import pyQtIndustrialWidget as qiw


class TestBasicWidgets(unittest.TestCase):
    """Test importing and interacting with widgets."""

    def test_import_classes(self):
        """Verify that all 12 widgets are imported properly."""
        expected_widgets = [
            "AnalysisChart",
            "AnnunciatorPanel",
            "CircularBargraph",
            "Compass",
            "IndustrialKnob",
            "IndustrialSwitch",
            "LedIndicator",
            "LevelMeter",
            "LinearGauge",
            "RadialGauge",
            "SevenSegmentDisplay",
            "StripChart",
        ]
        for name in expected_widgets:
            self.assertTrue(hasattr(qiw, name), f"Widget class '{name}' not found in pyQtIndustrialWidget")

    def test_radial_gauge(self):
        """Test RadialGauge instantiation and property methods."""
        gauge = qiw.RadialGauge()
        self.assertIsNotNone(gauge)

        # Range and value configuration
        gauge.setRange(0.0, 150.0)
        self.assertAlmostEqual(gauge.minimum(), 0.0)
        self.assertAlmostEqual(gauge.maximum(), 150.0)

        gauge.setValue(75.5)
        self.assertAlmostEqual(gauge.value(), 75.5)

        gauge.setUnit("RPM")
        self.assertEqual(gauge.unit(), "RPM")

    def test_industrial_knob(self):
        """Test IndustrialKnob instantiation and value manipulation."""
        knob = qiw.IndustrialKnob()
        self.assertIsNotNone(knob)

        knob.setRange(0.0, 100.0)
        self.assertAlmostEqual(knob.minimum(), 0.0)
        self.assertAlmostEqual(knob.maximum(), 100.0)

        knob.setValue(45.0)
        self.assertAlmostEqual(knob.value(), 45.0)

    def test_linear_gauge(self):
        """Test LinearGauge instantiation."""
        gauge = qiw.LinearGauge()
        self.assertIsNotNone(gauge)
        gauge.setRange(-20.0, 80.0)
        gauge.setValue(25.0)
        self.assertAlmostEqual(gauge.value(), 25.0)

    def test_seven_segment_display(self):
        """Test SevenSegmentDisplay instantiation and text/value."""
        display = qiw.SevenSegmentDisplay()
        self.assertIsNotNone(display)
        display.setValue(123.45)
        self.assertAlmostEqual(display.value(), 123.45)


if __name__ == "__main__":
    unittest.main()
