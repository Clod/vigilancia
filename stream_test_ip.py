# Note: This script should be executed in the curso-torch environment

# Import required libraries
# OpenCV for image processing and video capture
import cv2
# YOLO (You Only Look Once) for real-time object detection
from ultralytics import YOLO
# playsound for playing audio files
from playsound import playsound
# threading for concurrent audio playback
import threading
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

# Set up input stream to capture video from the default camera (index 0)
# This could be a webcam or the first available camera on the system
input_stream = cv2.VideoCapture(0)

# Get the frames per second (FPS) of the input stream
fps = int(input_stream.get(cv2.CAP_PROP_FPS))

# Retrieve video stream properties
# Get the width of the input frames
frame_width = int(input_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
# Get the height of the input frames
frame_height = int(input_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up VideoWriter to save the processed video
# XVID is a video codec for creating AVI video files
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# Create a VideoWriter object to save the output video
# Parameters: output filename, video codec, fps, frame size
out = cv2.VideoWriter('output.avi', fourcc, fps, (frame_width, frame_height))
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

# Function to play a beep sound when a specific object (bottle) is detected
# This function is designed to be run in a separate thread
def play_beep():
    # Play the warning sound from the specified MP3 file
    playsound('beep-warning-6387.mp3')

# Variable to track if a bottle was detected in the previous frame
# This helps prevent repeated beeping for the same bottle
bottle_detected_prev = False
# Main function to process video frames from the input stream
def process_frames():
    # Use global keyword to modify the global bottle_detected_prev variable
    global bottle_detected_prev
    
    # Continuous frame processing loop
    while True:
        # Read a frame from the input stream (webcam)
        ret, frame = input_stream.read()
        if not ret:
            # Break the loop if no frame is captured
            break

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

        # Trigger beep if a bottle is detected and wasn't detected in the previous frame
        # This prevents repeated beeping for the same bottle
        if bottle_detected and not bottle_detected_prev:
            # Start a new thread to play the beep sound
            # This prevents blocking the main processing loop
            threading.Thread(target=play_beep).start()

        # Update the bottle detection status for the next frame
        bottle_detected_prev = bottle_detected

        # Write the processed frame to the output video file
        out.write(frame)

        # Display the processed frame in a window
        cv2.imshow('Object Detection', frame)

        # Check for 'q' key press to exit the loop
        # waitKey(1) introduces a small delay and checks for key events
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# Main entry point of the script
if __name__ == '__main__':
    # Create a resizable named window for displaying object detection results
    cv2.namedWindow('Object Detection', cv2.WINDOW_NORMAL)
    
    # Start frame processing
    # This will run the object detection, video recording, and display loop
    process_frames()
    
    # Clean up resources
    # Release the video capture device
    input_stream.release()
    # Release the video writer to save the output video
    out.release()
    # Close all OpenCV windows
    cv2.destroyAllWindows()
