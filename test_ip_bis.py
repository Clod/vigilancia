# Ejectutarlo en curso-torch
import cv2
from ultralytics import YOLO
from playsound import playsound
import threading
import requests
import numpy as np

# Play the MP3 file at the start of the script
def play_startup_sound() -> None:
    """
    Play the startup sound MP3 file.

    This function is called once when the script starts and plays the
    startup sound MP3 file. The function is called in a separate
    thread to prevent blocking the main thread.
    """
    # Play the startup sound MP3 file
    playsound('beep-warning-6387.mp3')

# Start playing the startup sound in a separate thread
threading.Thread(target=play_startup_sound).start()

# Initialize YOLO model
yolo = YOLO('yolov8s.pt')

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
# Works with app: https://play.google.com/store/apps/details?id=com.pas.webcam&pcampaignid=web_share
url = "http://192.168.0.100:8080/shot.jpg"

def process_frames():
    """
    Process frames from the input stream.

    This function runs in an infinite loop and performs the following steps:

    1. Captures a frame-by-frame from the input stream using the requests library.
    2. Converts the frame to a numpy array using the bytearray library.
    3. Decodes the frame to OpenCV format using the imdecode function.
    4. Performs object detection on the frame using the track function of the YOLO model.
    5. Iterates over the bounding boxes detected by the YOLO model and draws them on the frame.
    6. Checks if the detected object is a bottle and if so, triggers a beep sound.
    7. Displays the frame with the drawn bounding boxes.
    8. Breaks the loop if 'q' is pressed.

    This function is called in a separate thread to prevent blocking the main thread.
    """
    while True: 
        # Capture frame-by-frame
        img_resp = requests.get(url) 
        # Convert to a numpy array
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
        # Decode image to OpenCV format
        frame = cv2.imdecode(img_arr, -1) 
        
        # Perform object detection
        results = yolo.track(frame, stream=True)

        # Variable to track if a bottle was detected in the previous frame
        bottle_detected = False
        for result in results:
            # Get the bounding boxes and class names
            boxes = result.boxes.cpu().numpy()
            class_names = result.names

            # Iterate over the bounding boxes
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = box.conf[0]
                if confidence < 0.5:
                    continue

                # Get the bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].astype(int)
                color = get_colors(class_id)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                label = f"{class_names[class_id]} {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Check if the detected object is a bottle
                if class_names[class_id].lower() == 'bottle':
                    bottle_detected = True

        # Trigger beep if a bottle is detected
        if bottle_detected:
            threading.Thread(target=play_beep).start()

        # Display the frame
        cv2.imshow('Object Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Function to get class colors
def get_colors(cls_num):
    """
    Generate a color based on the provided class number.

    Args:
        cls_num (int): The class number for which the color is generated.

    Returns:
        tuple: A tuple representing the RGB color, with values clamped between 0 and 255.
    """
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] * (cls_num // len(base_colors)) for i in range(3)]
    return tuple(max(0, min(255, c)) for c in color)

# Function to play beep sound when a bottle is detected
def play_beep():
    """
    Play a beep sound.

    This function plays a beep sound from the specified MP3 file
    when called. It is intended to be used in a separate thread
    to avoid blocking the main thread.
    """
    playsound('beep-warning-6387.mp3')

if __name__ == '__main__':
    # Create a named window
    cv2.namedWindow('Object Detection', cv2.WINDOW_NORMAL)
    
    # Start frame processing
    process_frames()
    
    # Release resources
    cv2.destroyAllWindows()
