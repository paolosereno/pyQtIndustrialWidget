# pyQtIndustrialWidget

Python bindings (**PySide6 / Qt 6**) for the C++ [QtIndustrialWidgets](https://github.com/paolosereno/QtIndustrialWidgets) library, built using **Shiboken6**, **CMake**, and **scikit-build-core**.

> [!WARNING]
> ### ⚠️ EXPERIMENTAL & WORK IN PROGRESS
> **This project is currently in an early, experimental stage.**
> - Features, bindings coverage, and build pipelines are undergoing active development.
> - Unexpected behaviors, bugs, or ABI/API breaking changes may occur.
> - **Use exclusively for evaluation, experimentation, and testing purposes.** It is **not** recommended for production use.
> - Bug reports, feedback, and contributions are welcome via [GitHub Issues](https://github.com/paolosereno/pyQtIndustrialWidget/issues).

---

## 📦 Included Widgets (12)

The library exposes high-performance instrumentation widgets designed for test benches, SCADA systems, telemetry displays, and automation dashboards:

| Widget | Description |
|---|---|
| `RadialGauge` | Circular dial instrument with colored threshold warning arcs, needle pointer, and digital readout |
| `LinearGauge` | Horizontal or vertical linear bar gauge with configurable graduation ticks and scales |
| `IndustrialKnob` | Precision rotary control knob for setpoint adjustment |
| `SevenSegmentDisplay` | Multi-digit electronic seven-segment LED readout |
| `LedIndicator` | Multi-state LED indicator with configurable colors, flashing support, and shapes |
| `StripChart` | High-frequency real-time scrolling oscilloscope chart powered by M4 decimation |
| `IndustrialSwitch` | Industrial toggle and multi-position rotary selector switch |
| `LevelMeter` | Tank liquid level / peak audio VU-meter indicator |
| `AnnunciatorPanel` | Multi-cell alarm annunciator panel with ISA-compliant sequence states |
| `Compass` | Circular compass rose for heading, bearing, and navigational orientation |
| `CircularBargraph` | Segmented circular arc bar display with value threshold states |
| `AnalysisChart` | Diagnostic and spectrum analysis chart with dual measurement cursors |

---

## 🛠 Prerequisites & Requirements

- **Python**: `>= 3.9`
- **PySide6**: `>= 6.6.0`
- **shiboken6** & **shiboken6-generator**: `>= 6.6.0`
- **CMake**: `>= 3.20`
- **C++17 compliant compiler** (GCC 11+, Clang 13+, MSVC 2019+)
- **Ninja** (recommended build generator)

---

## 🚀 Installation & Local Development

### Editable Development Install

1. Clone the repository:
   ```bash
   git clone https://github.com/paolosereno/pyQtIndustrialWidget.git
   cd pyQtIndustrialWidget
   ```

2. Create and activate a clean virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Upgrade pip and install build prerequisites:
   ```bash
   pip install --upgrade pip
   pip install "scikit-build-core>=0.9.0" "ninja" "PySide6>=6.6.0" "shiboken6>=6.6.0" "shiboken6-generator>=6.6.0"
   ```

4. Build and install the bindings in editable mode:
   ```bash
   pip install --no-build-isolation -e .
   ```

> [!NOTE]
> The original C++ upstream source code (`QtIndustrialWidgets`) is automatically fetched by CMake via `FetchContent` during the build process; no manual cloning or local copy of the C++ source is needed.

---

## 💻 Quick Start Example

Here is an example demonstrating `RadialGauge` connected to an `IndustrialKnob`:

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyQtIndustrialWidget import RadialGauge, IndustrialKnob

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pyQtIndustrialWidget Demo")
        self.resize(400, 500)

        container = QWidget(self)
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        # Instantiate a RadialGauge
        self.gauge = RadialGauge()
        self.gauge.setRange(0.0, 100.0)
        self.gauge.setUnit("BAR")
        self.gauge.setValue(25.0)

        # Instantiate an IndustrialKnob
        self.knob = IndustrialKnob()
        self.knob.setRange(0.0, 100.0)
        self.knob.setValue(25.0)

        # Connect the knob signal to the gauge slot
        self.knob.valueChanged.connect(self.gauge.setValue)

        layout.addWidget(self.gauge)
        layout.addWidget(self.knob)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec())
```

---

## 🧪 Running Tests

To run the test suite in a headless environment:

```bash
python -m unittest discover -s tests
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Upstream C++ library copyright (c) Paolo Sereno / QtIndustrialWidgets Contributors.
