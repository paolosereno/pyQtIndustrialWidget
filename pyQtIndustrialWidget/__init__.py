"""
pyQtIndustrialWidget - Python bindings for QtIndustrialWidgets.

A high-performance collection of 12 industrial instrumentation widgets for PySide6 / Qt 6.
"""

try:
    from .pyQtIndustrialWidget import (
        AnalysisChart,
        AnnunciatorPanel,
        CircularBargraph,
        Compass,
        IndustrialKnob,
        IndustrialSwitch,
        LedIndicator,
        LevelMeter,
        LinearGauge,
        RadialGauge,
        SevenSegmentDisplay,
        StripChart,
    )
except ImportError:
    # Fallback for direct global import when installed as standalone extension module
    from pyQtIndustrialWidget import (  # type: ignore
        AnalysisChart,
        AnnunciatorPanel,
        CircularBargraph,
        Compass,
        IndustrialKnob,
        IndustrialSwitch,
        LedIndicator,
        LevelMeter,
        LinearGauge,
        RadialGauge,
        SevenSegmentDisplay,
        StripChart,
    )

__version__ = "0.1.0"

__all__ = [
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
