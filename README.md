# Vigilancia Project

This project is a collection of Python scripts for video capture, object detection, and streaming. It utilizes libraries such as OpenCV, PyQt5, YOLOv8, and flask-opencv-streamer.

## Functionality

- **Video Capture Application (video_capture_app.py):**
  - A PyQt5 GUI application that captures video from a webcam.
  - Allows starting and stopping video capture using a toggle button.
  - Displays the video feed in a window.

- **Object Detection and Streaming (stream_test.py):**
  - Uses YOLOv8 for real-time object detection in video streams.
  - Integrates with flask-opencv-streamer to stream the processed video feed over a web server.
  - Detects objects in the video frames and draws bounding boxes around them with class labels and confidence scores.
  - Provides a basic color-coding for different object classes.
  - Streams the video feed on port 3000 (default).

## Technologies Used

- **OpenCV (cv2):** For video capture and image processing.
- **PyQt5:** For creating the graphical user interface of the video capture application.
- **YOLOv8 (ultralytics):** For object detection tasks.
- **flask-opencv-streamer:** For streaming video over HTTP.
- **Flask:** (implicitly used by flask-opencv-streamer) A micro web framework for Python.

## Scripts

- `video_capture_app.py`: PyQt5 application for basic video capture and display.
- `stream_test.py`: Script for real-time object detection using YOLOv8 and video streaming.
- `yolov8s.pt`: YOLOv8 small model weights (used for object detection).
- `curso_pyqt5/`: Contains various PyQt5 example applications and UI files, potentially used as learning resources or for testing PyQt5 functionalities.

## Setup and Usage

### Dependencies

Ensure you have the required libraries installed. You can install them using pip:

```bash
pip install opencv-python pyqt5 ultralytics flask flask-opencv-streamer
```

For `video_capture_app.py`:

1. Run the script: `python video_capture_app.py`
2. Click "Start Video" to begin capturing and displaying video from your webcam.
3. Click "Stop Video" to stop the video capture.

For `stream_test.py`:

1. Run the script: `python stream_test.py`
2. Open a web browser and go to `http://localhost:3000` to view the streamed video with object detection.

**Note:**  `stream_test.py` requires the `yolov8s.pt` model weights file to be in the same directory.

## Curso PyQt5 Directory

The `curso_pyqt5/` directory contains example PyQt5 applications, likely from a PyQt5 tutorial or course. These scripts demonstrate various PyQt5 widgets, layouts, and functionalities. They can be run individually to explore PyQt5 capabilities.

## Disclaimer

This project is provided as-is for educational and demonstration purposes.  Further development and refinement may be required for specific use cases.

---
*This README.md was automatically generated based on the project's code.*
