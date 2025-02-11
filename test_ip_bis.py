# Note: This script should be executed in the curso-torch environment

# Import required libraries
# OpenCV for image processing and display
import cv2
# YOLO (You Only Look Once) for real-time object detection
from ultralytics import YOLO
# playsound for playing audio files
from playsound import playsound
# threading for concurrent audio playback
import threading
# requests for making HTTP requests to fetch images
import requests
# NumPy for numerical array operations
import numpy as np
# Function to play the startup sound MP3 file
# This function is designed to be run in a separate thread
# to prevent blocking the main script execution
def play_startup_sound() -> None:
    """
    Play the startup sound MP3 file.

    This function is called once when the script starts and plays the
    startup sound MP3 file. The function is called in a separate
    thread to prevent blocking the main thread.
    """
    # Play the startup sound from the specified MP3 file
    # The sound file is located in the current directory
    playsound('beep-warning-6387.mp3')

# Start playing the startup sound in a separate thread
# This ensures the sound plays without interrupting the main script
threading.Thread(target=play_startup_sound).start()
# Initialize YOLO model with pre-trained weights (YOLOv8 small version)
# The model is loaded from 'yolov8s.pt' which contains pre-trained object detection weights
yolo = YOLO('yolov8s.pt')

# URL of the IP webcam streaming service
# Replace this URL with the specific IP address and port of your Android device's IP webcam
# The "/shot.jpg" endpoint typically provides a single frame from the camera stream
# Works with apps like IP Webcam from the Google Play Store
url = "http://192.168.0.100:8080/shot.jpg"
# Main function to process frames from the IP camera stream
def process_frames():
    """
    Process frames from the input stream.

    This function runs in an infinite loop and performs the following steps:
    1. Captures a frame from the IP camera using HTTP requests
    2. Converts the frame to a NumPy array
    3. Decodes the frame to OpenCV format
    4. Performs object detection using YOLO
    5. Draws bounding boxes and labels for detected objects
    6. Triggers a beep sound if a bottle is detected
    7. Displays the processed frame
    8. Allows exiting the loop by pressing 'q'

    This function is designed to run continuously and process live video stream.
    """
    while True: 
        try:
            # Send a GET request to fetch the current frame from the IP camera
            img_resp = requests.get(url) 
            
            # Convert the image response content to a NumPy array
            # bytearray converts the image data to a byte array
            # np.uint8 specifies unsigned 8-bit integer data type for image pixel values
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
            
            # Decode the image array into an OpenCV compatible image format
            # -1 parameter preserves the original image color
            frame = cv2.imdecode(img_arr, -1) 
            
            # Perform object detection using YOLO tracking
            # stream=True allows processing multiple frames
            results = yolo.track(frame, stream=True)

            # Flag to track if a bottle is detected in the current frame
            bottle_detected = False
            
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

                    # Check if the detected object is a bottle
                    # Convert class name to lowercase for case-insensitive comparison
                    if class_names[class_id].lower() == 'bottle':
                        bottle_detected = True

            # Trigger beep if a bottle is detected
            # Start a new thread to play the beep sound to prevent blocking
            if bottle_detected:
                threading.Thread(target=play_beep).start()

            # Display the processed frame in a window
            cv2.imshow('Object Detection', frame)

            # Check for 'q' key press to exit the loop
            # waitKey(1) introduces a small delay and checks for key events
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            print(f"Network error: {e}")
            break
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error: {e}")
            break
# Function to generate unique colors for different object classes
# This helps in visually distinguishing between different detected objects
# Parameters:
#   - cls_num: The class number of the detected object
# Returns: A unique RGB color tuple for drawing bounding boxes
def get_colors(cls_num):
    """
    Generate a color based on the provided class number.

    Args:
        cls_num (int): The class number for which the color is generated.

    Returns:
        tuple: A tuple representing the RGB color, with values clamped between 0 and 255.
    """
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

# Function to play a beep sound when a specific object (bottle) is detected
# This function is designed to be run in a separate thread
def play_beep():
    """
    Play a beep sound.

    This function plays a beep sound from the specified MP3 file
    when called. It is intended to be used in a separate thread
    to avoid blocking the main thread.
    """
    # Play the warning sound from the specified MP3 file
    playsound('beep-warning-6387.mp3')
# Main entry point of the script
if __name__ == '__main__':
    # Create a resizable named window for displaying object detection results
    cv2.namedWindow('Object Detection', cv2.WINDOW_NORMAL)
    
    # Start frame processing
    # This will run the object detection and display loop
    process_frames()
    
    # Close all OpenCV windows when the loop is terminated
    cv2.destroyAllWindows()
