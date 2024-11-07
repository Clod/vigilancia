# Ejectutarlo en curso-torch
import cv2
from ultralytics import YOLO
from playsound import playsound
import threading

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

input_stream = cv2.VideoCapture(0)
fps = int(input_stream.get(cv2.CAP_PROP_FPS))


# Get video properties
frame_width = int(input_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(input_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, fps, (frame_width, frame_height))

# Function to get class colors
def get_colors(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] * (cls_num // len(base_colors)) for i in range(3)]
    return tuple(max(0, min(255, c)) for c in color)

# Function to play beep sound when a bottle is detected
def play_beep():
    playsound('beep-warning-6387.mp3')

# Variable to track if a bottle was detected in the previous frame
bottle_detected_prev = False

def process_frames():
    global bottle_detected_prev
    while True:
        ret, frame = input_stream.read()
        if not ret:
            break

        # Perform object detection
        results = yolo.track(frame, stream=True)

        bottle_detected = False
        for result in results:
            boxes = result.boxes.cpu().numpy()
            class_names = result.names

            for box in boxes:
                class_id = int(box.cls[0])
                confidence = box.conf[0]
                if confidence < 0.5:
                    continue

                x1, y1, x2, y2 = box.xyxy[0].astype(int)
                color = get_colors(class_id)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                label = f"{class_names[class_id]} {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Check if the detected object is a bottle
                if class_names[class_id].lower() == 'bottle':
                    bottle_detected = True

        # Trigger beep if a bottle is detected and wasn't detected in the previous frame
        if bottle_detected and not bottle_detected_prev:
            threading.Thread(target=play_beep).start()

        bottle_detected_prev = bottle_detected

        # Write the processed frame to the output video
        out.write(frame)


        # Write the processed frame to the output video
        out.write(frame)

        # Display the frame
        cv2.imshow('Object Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    # Create a named window
    cv2.namedWindow('Object Detection', cv2.WINDOW_NORMAL)
    
    # Start frame processing
    process_frames()
    
    # Release resources
    input_stream.release()
    out.release()
    cv2.destroyAllWindows()