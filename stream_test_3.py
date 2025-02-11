# Import required libraries
# OpenCV for image processing and video capture
import cv2
# YOLO (You Only Look Once) for real-time object detection
from ultralytics import YOLO

# Initialize YOLO model
# Commented out default YOLOv8 small model
# yolo = YOLO('yolov8s.pt')
# Using a custom-trained model from a specific training run
yolo = YOLO("runs/detect/train12/weights/best.pt")

# Set up input stream to capture video from the default camera (index 0)
# This could be a webcam or the first available camera on the system
input_stream = cv2.VideoCapture(0)

# Retrieve video stream properties
# Get the width of the input frames
frame_width = int(input_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
# Get the height of the input frames
frame_height = int(input_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
# Get the frames per second (FPS) of the input stream
fps = int(input_stream.get(cv2.CAP_PROP_FPS))

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
# Main function to process video frames from the input stream
def process_frames():
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
