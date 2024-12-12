import serial  # For GPS and microcontroller communication
from mfrc522 import SimpleMFRC522  # For RFID
import pynmea2  # For parsing GPS data

# Initialize RFID reader
reader = SimpleMFRC522()

# Initialize GPS (Serial port for GPS module)
gps_port = "/dev/ttyUSB0"  # Adjust based on your system
gps_baud_rate = 9600
gps_serial = serial.Serial(gps_port, gps_baud_rate, timeout=1)

# Function to read RFID and confirm handshake
def rfid_handshake():
    try:
        print("Waiting for RFID tag...")
        id, text = reader.read()
        print(f"RFID Tag ID: {id}, Data: {text}")
        return id, text
    except Exception as e:
        print(f"RFID Read Error: {e}")
        return None, None

# Function to acquire GPS position
def acquire_gps_position():
    try:
        while True:
            gps_data = gps_serial.readline().decode("ascii", errors="replace")
            if gps_data.startswith("$GPGGA"):  # GPS fix data
                msg = pynmea2.parse(gps_data)
                latitude = msg.latitude
                longitude = msg.longitude
                print(f"Latitude: {latitude}, Longitude: {longitude}")
                return latitude, longitude
    except Exception as e:
        print(f"GPS Error: {e}")
        return None, None

# Main function for TVC system
def main():
    print("Initializing RFID and GPS system...")
    
    # Perform RFID Handshake
    id, data = rfid_handshake()
    if id is not None:
        print("RFID Handshake Successful!")
    else:
        print("RFID Handshake Failed!")
        return

    # Acquire Target Position
    latitude, longitude = acquire_gps_position()
    if latitude is not None and longitude is not None:
        print(f"Target Position Acquired: Latitude={latitude}, Longitude={longitude}")
    else:
        print("Failed to acquire target position!")

if __name__ == "__main__":
    main()
