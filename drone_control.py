import serial
import cv2
import time
import numpy as np

# Initialize serial connection to Arduino
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)  # Adjust the port to your system
    time.sleep(2)  # Allow time for Arduino to initialize
except serial.SerialException as e:
    print(f"Error connecting to Arduino: {e}")
    exit(1)

# Setup for Camera (OpenCV for detecting drones)
cap = cv2.VideoCapture(0)  # Use camera 0 (first available camera)

# Function to detect drones (using Haar Cascade)
def detect_drones(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    drone_cascade = cv2.CascadeClassifier('C:/Users/Sujeet K/Desktop/tvc/drone_cascade.xml')
    if drone_cascade.empty():
        print("Error: Unable to load drone_cascade.xml")
        exit(1)
    drones = drone_cascade.detectMultiScale(gray, 1.1, 4)
    return drones

# Function to send coordinates to Arduino to control the servo motors
def aim_weapon(x, y):
    try:
        arduino.write(f"{x},{y}\n".encode())  # Send x, y as a string to Arduino
    except serial.SerialException as e:
        print(f"Error sending data to Arduino: {e}")

def main():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video frame")
            break
        
        # Detect drones in the camera frame
        drones = detect_drones(frame)
        for (x, y, w, h) in drones:
            # Calculate the center coordinates of the detected drone
            center_x = x + w // 2
            center_y = y + h // 2

            # Print drone coordinates and send them to Arduino for servo control
            print(f"Drone detected at coordinates: {center_x}, {center_y}")
            aim_weapon(center_x, center_y)

            # Read distance from Arduino's ultrasonic sensor
            if arduino.in_waiting > 0:
                try:
                    distance = arduino.readline().decode('utf-8').strip()
                    print(f"Distance to target: {distance} cm")
                except Exception as e:
                    print(f"Error reading distance: {e}")

        # Show the video feed
        cv2.imshow('Drone Detection', frame)
        
        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()

if drone_cascade.empty(): # type: ignore
    print("Error: Unable to load drone_cascade.xml")
    exit(1)
