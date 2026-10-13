# Skin Tone Detector

## Overview

Skin Tone Detector is a Streamlit-based web app that detects faces from a photo (upload or camera), then analyzes skin color to classify it into one of four categories — **Fair**, **Light**, **Medium**, or **Dark** — based on the HSV values of the detected face area. Based on the result, the app shows makeup product recommendations (blush, foundation, lipstick) that match the skin tone.

## Live URL
https://skin-tone-app.streamlit.app/

## Features

- **Skin Tone Description** — an information page explaining the characteristics of each skin tone category (Fair, Light, Medium, Dark).
- **Detection via Photo Upload** — upload a photo (jpg/png/jpeg); the system detects the face and shows a bounding box before analysis.
- **Detection via Camera** — take a photo directly from your device camera for real-time analysis.
- **Skin Tone Classification** — skin color analysis using face detection (Haar Cascade) and the median HSV value of the face area.
- **Product Recommendations** — shows blush, foundation, and lipstick recommendations based on the classified skin tone.
- **Developer Profile** — a page listing the members of the development team.

## Tech Stack

- **[Streamlit](https://streamlit.io/)** — framework for building the app's web interface and deployement.
- **[streamlit-option-menu](https://pypi.org/project/streamlit-option-menu/)** — sidebar navigation component.
- **[OpenCV](https://opencv.org/)** (`opencv-python-headless`) — face detection (Haar Cascade) and color space conversion (RGB/BGR/HSV).
- **[NumPy](https://numpy.org/)** — array/matrix operations for image pixel processing.
- **[Pillow (PIL)](https://python-pillow.org/)** — image processing and manipulation (open, convert, draw bounding box).
- **Python** 3.x

## Project Structure

```
Skin-Tone/
├── images/
│   ├── DARK/{Blush,Foundation,Lipstick}/*.png
│   ├── FAIR/{Blush,Foundation,Lipstick}/*.png
│   ├── LIGHT/{Blush,Foundation,Lipstick}/*.png
│   ├── MEDIUM/{Blush,Foundation,Lipstick}/*.png
│   └── Teams.jpg
├── mainsec.py          # application entry point
├── main_test.py         # experimental file (unstable, do not run)
└── requirements.txt
```

## Run in Dev

1. **Clone the repository and enter the project folder**
   ```bash
   git clone <repo-url>
   cd Skin-Tone
   ```

2. **Create a virtual environment** (recommended)
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```powershell
   streamlit run mainsec.py
   ```

   The app opens automatically in your browser at `http://localhost:8501`.

### Notes

- `main_test.py` is a separate experimental file and does not need to be run — use `mainsec.py` as the main entry point.
- If you get the error `AttributeError: module 'cv2' has no attribute 'CascadeClassifier'`, make sure the installed `opencv-python-headless` version is 4.x (not 5.x), because OpenCV 5.x changed its Python binding layout.
