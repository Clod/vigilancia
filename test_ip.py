# Import essential libraries for network image streaming
# requests for making HTTP requests to fetch images
import requests 
# OpenCV for image processing and display
import cv2 
# NumPy for numerical array operations
import numpy as np 

# URL of the IP webcam streaming service
# Replace this URL with the specific IP address and port of your Android device's IP webcam
# The "/shot.jpg" endpoint typically provides a single frame from the camera stream
url = "http://192.168.0.100:8080/shot.jpg"

# Continuous loop to fetch and display live video from the IP camera
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
        img = cv2.imdecode(img_arr, -1) 
        
        # Optional: Resize the image (commented out)
        # Uncomment and adjust width/height as needed
        # img = imutils.resize(img, width=1000, height=1800) 
        
        # Display the image in a window named "Android_cam"
        cv2.imshow("Android_cam", img) 

        # Wait for a key press and check for the Escape (27) key to exit
        # 1 ms delay between frames to allow smooth video-like display
        if cv2.waitKey(1) == 27: 
            break
    
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        print(f"Network error: {e}")
        break
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")
        break

# Close all OpenCV windows when the loop is terminated
cv2.destroyAllWindows()
