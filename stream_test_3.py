import cv2
from ultralytics import YOLO

# Initialize YOLO model
# yolo = YOLO('yolov8s.pt')
yolo = YOLO("runs/detect/train12/weights/best.pt")

# Set up input stream
input_stream = cv2.VideoCapture(0)

# Get video properties
frame_width = int(input_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(input_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(input_stream.get(cv2.CAP_PROP_FPS))

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

def process_frames():
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