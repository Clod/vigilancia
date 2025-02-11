#%% Import required libraries
# OpenCV for image processing and video capture
import cv2
# YOLO (You Only Look Once) for real-time object detection
from ultralytics import YOLO
# Flask-based OpenCV streamer for broadcasting video stream
from flask_opencv_streamer.streamer import Streamer
# Initialize YOLO model with pre-trained weights (YOLOv8 small version)
# The model is loaded from 'yolov8s.pt' which contains pre-trained object detection weights
yolo = YOLO('yolov8s.pt')

# Set up input stream to capture video from the default camera (index 0)
# This could be a webcam or the first available camera on the system
input_stream = cv2.VideoCapture(0)

# Configure video streaming server
# Port 3000 will be used to broadcast the video stream
# require_login is set to False, meaning no authentication is needed to view the stream
port = 3000
require_login = False
streamer = Streamer(port, require_login)
# Function to generate unique colors for different object classes
# This helps in visually distinguishing between different detected objects
# Parameters:
#   - cls_num: The class number of the detected object
# Returns: A unique RGB color tuple for drawing bounding boxes
def get_colors(cls_num):
    # Define base colors (Red, Green, Blue)
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    
    # Cycle through base colors for different classes
    color_index = cls_num % len(base_colors)
    
    # Define color increments to create variations
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    
    # Generate a unique color by modifying base colors
    color = [base_colors[color_index][i] + increments[color_index][i] * (cls_num // len(base_colors)) for i in range(3)]
    
    # Ensure color values are within 0-255 range
    return tuple(max(0, min(255, c)) for c in color)
# Main processing loop for real-time object detection and streaming
while True:
    # Read a frame from the input stream (webcam)
    ret, frame = input_stream.read()
    if not ret:
        # Break the loop if no frame is captured
        break

    # Perform object detection using YOLO tracking
    # stream=True allows processing multiple frames
    results = yolo.track(frame, stream=True)

    # Process each detection result
    for result in results:
        # Convert bounding boxes to numpy array for easier processing
        boxes = result.boxes.cpu().numpy()
        # Get the dictionary of class names
        class_names = result.names

        # Iterate through detected objects
        for box in boxes:
            # Extract class ID of the detected object
            class_id = int(box.cls[0])
            # Get confidence score of the detection
            confidence = box.conf[0]
            
            # Skip detections with low confidence (less than 50%)
            if confidence < 0.5:
                continue

            # Extract bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0].astype(int)
            
            # Generate a unique color for the object's class
            color = get_colors(class_id)
            
            # Draw rectangle around the detected object
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Create label with class name and confidence score
            label = f"{class_names[class_id]} {confidence:.2f}"
            
            # Put text label above the bounding box
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Update the streaming server with the processed frame
    streamer.update_frame(frame)

    # Check for 'q' key press to exit the loop
    # waitKey(1) introduces a small delay and checks for key events
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up resources
# Release the video capture device
input_stream.release()
# Close all OpenCV windows
cv2.destroyAllWindows()
# %%
