import cv2
import numpy as np
import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust the serial port based on your setup
time.sleep(2)  # Allow the connection to establish

def send_position_to_tvc(x, y):
    """Send detected object's position to the Arduino."""
    data = f"{x},{y}\n"
    arduino.write(data.encode())
    print(f"Sent: {data}")

# Initialize video capture (USB webcam or Raspberry Pi Camera)
cap = cv2.VideoCapture(0)  # Use 0 for default USB webcam, use 1 for Raspberry Pi camera module

if not cap.isOpened():
    print("Camera not found!")
    exit()

# Initialize time tracking
last_update_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame!")
        break

    # Check if 3 seconds have passed since the last update
    if time.time() - last_update_time >= 3:
        # Convert frame to grayscale and apply Gaussian blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply binary threshold
        _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Debugging: Print number of contours detected
        print(f"Found {len(contours)} contours")

        # Process contours
        for contour in contours:
            # Filter small objects based on contour area
            if cv2.contourArea(contour) > 500:
                # Get the bounding box
                x, y, w, h = cv2.boundingRect(contour)
                center_x, center_y = x + w // 2, y + h // 2

                # Draw bounding box and center point
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                # Send position to TVC (Arduino)
                send_position_to_tvc(center_x, center_y)

        # Update last update time
        last_update_time = time.time()

    # Display the video feed (video continuously updates)
    cv2.imshow("Object Detection", frame)

    # Break loop on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
arduino.close()
