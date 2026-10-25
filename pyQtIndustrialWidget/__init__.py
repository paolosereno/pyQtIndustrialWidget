"""
pyQtIndustrialWidget - Python bindings for QtIndustrialWidgets.

A high-performance collection of 12 industrial instrumentation widgets for PySide6 / Qt 6.
"""

import os
import sys
import ctypes

# Initialize PySide6 runtime
try:
    import PySide6
    from PySide6 import QtCore, QtGui, QtWidgets  # noqa: F401
except ImportError:
    pass

# Ensure QtIndustrialWidgets and PySide6 libraries can be resolved
_pkg_dir = os.path.dirname(os.path.abspath(__file__))

if sys.platform == "win32":
    if hasattr(os, "add_dll_directory"):
        for _p in (_pkg_dir, os.path.abspath(os.path.join(_pkg_dir, "..", "lib"))):
            if os.path.isdir(_p):
                os.add_dll_directory(_p)
        try:
            import PySide6
            _pyside_dir = os.path.dirname(PySide6.__file__)
            os.add_dll_directory(_pyside_dir)
        except Exception:
            pass
else:
    # Linux / macOS library preloading
    _candidates = [
        os.path.join(_pkg_dir, "libQtIndustrialWidgets.so.2"),
        os.path.join(_pkg_dir, "libQtIndustrialWidgets.so"),
        os.path.join(_pkg_dir, "..", "lib", "libQtIndustrialWidgets.so.2"),
        os.path.join(_pkg_dir, "..", "lib", "libQtIndustrialWidgets.so"),
        os.path.join(_pkg_dir, "libQtIndustrialWidgets.2.dylib"),
        os.path.join(_pkg_dir, "libQtIndustrialWidgets.dylib"),
        os.path.join(_pkg_dir, "..", "lib", "libQtIndustrialWidgets.2.dylib"),
        os.path.join(_pkg_dir, "..", "lib", "libQtIndustrialWidgets.dylib"),
    ]
    for _cand in _candidates:
        if os.path.isfile(_cand):
            try:
                ctypes.CDLL(_cand, mode=ctypes.RTLD_GLOBAL)
                break
            except Exception:
                pass

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
