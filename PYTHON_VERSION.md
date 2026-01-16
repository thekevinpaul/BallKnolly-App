# Python Version Guide

## ✅ Recommended: Python 3.11

**Best choice for this project:**
- ✅ Fully compatible with all dependencies (soccerdata, streamlit, pandas, plotly)
- ✅ Widely supported by hosting platforms (Streamlit Cloud, Render, Railway)
- ✅ Stable and well-tested
- ✅ Good performance improvements over 3.10
- ✅ Latest stable version supported by most services

### Installation
Download from: https://www.python.org/downloads/release/python-3110/
- **Windows**: Download the Windows installer (64-bit)
- **macOS**: Download macOS 64-bit installer
- **Linux**: Use your package manager or download from python.org

**Important**: During installation on Windows, check ✅ "Add Python to PATH"

---

## Alternative Options

### Python 3.10
- ✅ Very safe, widely supported
- ✅ Works with all dependencies
- ⚠️ Slightly older, missing some newer features
- **Good if**: You want maximum compatibility

### Python 3.12
- ✅ Latest features and best performance
- ✅ Works with soccerdata
- ⚠️ Some hosting platforms may not support it yet
- ⚠️ Some libraries might have compatibility issues
- **Good if**: You're running locally and want the latest features

### Python 3.9
- ✅ Minimum version that works
- ⚠️ Older, missing modern features
- ⚠️ Not recommended for new projects

---

## ❌ Don't Use

- **Python 3.8 or older**: May have compatibility issues
- **Python 2.x**: Not supported (deprecated)

---

## Verify Your Installation

After installing Python, verify it:

```bash
python --version
# Should show: Python 3.11.x

python -m pip --version
# Should show pip version
```

---

## For Streamlit Cloud Deployment

Streamlit Cloud supports:
- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11 (recommended)

**Note**: Streamlit Cloud will automatically detect your Python version from `requirements.txt` or use Python 3.11 by default.

---

## Quick Setup After Installing Python

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```
