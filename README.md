# ⚡ Pulsemon

**Pulsemon** is a modern, high-performance terminal system monitor built with Python. It provides real-time insights into your system's "pulse," including CPU usage, memory consumption, and active processes, all wrapped in a beautiful, responsive CLI interface.

![Pulsemon UI Experience](https://img.shields.io/badge/UI-Modern--Rich-blueviolet?style=for-the-badge)
![Dependencies](https://img.shields.io/badge/built%20with-psutil%20%7C%20rich-green?style=for-the-badge)

## ✨ Features

- 🚀 **Real-time Monitoring**: Smooth, flicker-free updates using multi-threaded data collection.
- 📊 **Process Management**: View active processes with their PID, CPU, and RAM consumption.
- ⚡ **Interactive Controls**:
  - **Sort**: Instantly toggle between CPU and RAM-heavy processes.
  - **Filter**: Find specific processes using live search.
  - **Kill**: Terminate unresponsive processes safely with user confirmation.
- ⚠️ **Smart Alerts**: Dynamic visual warnings when CPU or RAM usage exceeds safety thresholds.
- ⚙️ **Persistent Config**: Customize refresh rates, thresholds, and default settings via `config.json`.
- 🎨 **Premium Aesthetics**: Clean, color-coded layout powered by the [Rich](https://github.com/Textualize/rich) library.

## 🛠️ Installation

### 1. Prerequisites
- Python 3.8+
- pip

### 2. Setup
Clone the repository and install the dependencies:

```bash
git clone https://github.com/Gansputra/pulsemon.git
cd pulsemon
pip install -r requirements.txt
```

### 3. Developer Install (Optional)
If you want to use the `pulsemon` command globally:
```bash
pip install -e .
```

## ⌨️ Dashboard Shortcuts

| Key | Action |
| :--- | :--- |
| `S` | **Toggle Sort** (Switch between CPU and RAM) |
| `F` | **Filter** (Search processes by name) |
| `K` | **Kill** (Terminate process by PID) |
| `X` | **Clear** (Reset all filters) |
| `Q` | **Quit** (Exit gracefully) |

## ⚙️ Configuration

Pulsemon generates a `config.json` file in the root directory upon first run. You can manually edit it to tune the app:

```json
{
    "refresh_rate": 1.0,
    "cpu_threshold": 85.0,
    "ram_threshold": 85.0,
    "default_sort": "cpu",
    "max_processes": 15
}
```

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Created with ❤️ by **Gansputra**
