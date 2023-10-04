import serial

# Define the serial port and baud rate for your GPS module
serial_port = "com7"  # Adjust the port name as needed
baud_rate = 115200

# Open the serial port
ser = serial.Serial(serial_port, baud_rate)

try:
    while True:
        # Read a line of data from the GPS module
        line = ser.readline().decode('utf-8').strip()
        
        # Check if the line starts with '$GPGGA' (a common NMEA sentence)
        if line.startswith("$GPGGA"):
            # Split the NMEA sentence into fields
            data = line.split(',')
            
            # Extract latitude and longitude (assuming they are in the 2nd and 4th fields)
            latitude = data[2]
            longitude = data[4]
            
            print(f"Latitude: {latitude}, Longitude: {longitude}")
        
        # Check if the line starts with '$GPVTG' (another common NMEA sentence for course and speed)
        elif line.startswith("$GPVTG"):
            # Split the NMEA sentence into fields
            data = line.split(',')
            
            # Extract True Course (TC) and Ground Speed (GS) (assuming they are in the 1st and 7th fields)
            course = data[1]  # True Course in degrees
            speed_knots = float(data[7])  # Ground Speed in knots
            
            # Convert speed from knots to mph
            speed_mph = speed_knots * 1.15078
            
            print(f"Course: {course} degrees, Speed: {speed_mph:.2f} mph")
            
except KeyboardInterrupt:
    # Close the serial port when the program is interrupted
    ser.close()
    print("GPS reading terminated.")
