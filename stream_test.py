#%%
import cv2
from ultralytics import YOLO
from flask_opencv_streamer.streamer import Streamer

# Initialize YOLO model
yolo = YOLO('yolov8s.pt')

# Set up input stream (e.g., webcam)
input_stream = cv2.VideoCapture(0)

# Set up output stream
port = 3000
require_login = False
streamer = Streamer(port, require_login)

# Function to get class colors
def get_colors(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] * (cls_num // len(base_colors)) for i in range(3)]
    return tuple(max(0, min(255, c)) for c in color)

# Main loop for object detection
while True:
    ret, frame = input_stream.read()
    if not ret:
        break

    # Perform object detection
    results = yolo.track(frame, stream=True)

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

    # Stream the processed frame
    streamer.update_frame(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
input_stream.release()
cv2.destroyAllWindows()
# %%
