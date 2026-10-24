# PyQtIndustrialWidget

A pure-Python collection of industrial-grade widgets and instruments for **PySide6** and **PyQt6**, inspired by and ported from classical Qt industrial controls (`QtIndustrialWidgets`).

> [!WARNING]
> ### ⚠️ Project Status: Experimental / Not Fully Maintained
> This repository is currently **in an early experimental / proof-of-concept stage** and is used for testing and prototyping. It is **not yet fully maintained**, tested for production environments, or guaranteed to have a stable API. Breaking changes may occur at any time.

---

## 🛠 Features

### `SevenSegmentDisplay`
A vector-rendered 7-segment digital display designed with industrial instrument aesthetics:
- **Realistic Geometry**: Hexagonal-ended segments modeled after genuine LED/LCD display dies.
- **Ghost (Unlit) Segments**: Configurable faint background illumination for unlit segments to mimic physical displays.
- **Custom Color Palettes**: Preset industrial themes including Amber, Classic Red, Green Phosphor, and Cyan, or arbitrary `QColor` values.
- **Hardware-style Tilt**: Realistic italic shear angle (slanted digits).
- **Format Flexibility**: Automatic parsing of decimal points, right-aligned digit padding, and configurable digit counts.
- **Dual Compatibility**: Works seamlessly with both **PySide6** and **PyQt6**.
- **Pure Vector Graphics**: Drawn dynamically using `QPainter`, scaling cleanly to high-DPI and Retina displays without raster artifacts.
- **Built-in Interactive Demo**: Standalone runner with live controls to test colors, values, and ghost segment toggles.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- PySide6 (recommended) or PyQt6

### 2. Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/paolosereno/pyQtIndustrialWidget.git
cd pyQtIndustrialWidget

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Demo
Launch the interactive test application:
```bash
python seven_segment_display.py
```

---

## 💻 Example Usage

```python
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide6.QtGui import QColor
from seven_segment_display import SevenSegmentDisplay

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout(window)

# Create and customize display
display = SevenSegmentDisplay()
display.setNumDigits(6)
display.setOnColor(QColor(255, 140, 0))  # Industrial Amber
display.setShowGhostSegments(True)
display.setText("123.45")

layout.addWidget(display)
window.show()

sys.exit(app.exec())
```

---

## 🗺 Roadmap / Planned Widgets
- [ ] Analog Gauges (Circular & Arc Meters)
- [ ] LED Status Indicators & Bargraphs
- [ ] Industrial Sliders & Knobs
- [ ] Multi-character Alphanumeric 14/16-segment Displays
- [ ] Packaging & distribution as a reusable PyPI package

---

## 📄 License
This project is open-source. A formal license will be added as the project matures.
