import serial
import tkinter as tk
from tkinter.font import Font
import threading

# Define the serial port and baud rate for your A9G GPS module
serial_port = "COM7"  # Adjust the port name as needed
baud_rate = 115200

# Open the serial port
try:
    ser = serial.Serial(serial_port, baud_rate)
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()  # Exit the script if the serial port cannot be opened

# Create a Tkinter window
root = tk.Tk()
root.title("GPS Data")
root.geometry("400x300")  # Set window dimensions

# Create a large font
large_font = Font(family="Helvetica", size=20)

# Create labels for displaying data
lat_label = tk.Label(root, text="Latitude:", font=large_font)
long_label = tk.Label(root, text="Longitude:", font=large_font)
speed_label = tk.Label(root, text="Speed:", font=large_font)
direction_label = tk.Label(root, text="Direction:", font=large_font)

# Create StringVar variables to update labels
lat_var = tk.StringVar()
long_var = tk.StringVar()
speed_var = tk.StringVar()
direction_var = tk.StringVar()

# Create label widgets using StringVar
lat_value_label = tk.Label(root, textvariable=lat_var, font=large_font)
long_value_label = tk.Label(root, textvariable=long_var, font=large_font)
speed_value_label = tk.Label(root, textvariable=speed_var, font=large_font)
direction_value_label = tk.Label(root, textvariable=direction_var, font=large_font)

# Pack the labels in a grid with evenly spaced widgets
lat_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
lat_value_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")
long_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
long_value_label.grid(row=1, column=1, padx=10, pady=10, sticky="e")
speed_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
speed_value_label.grid(row=2, column=1, padx=10, pady=10, sticky="e")
direction_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
direction_value_label.grid(row=3, column=1, padx=10, pady=10, sticky="e")

# Function to continuously update GPS data
def update_gps_data():
    try:
        while True:
            # Read a line of data from the A9G GPS module
            line = ser.readline().decode('utf-8').strip()
            
            # Check if the line starts with '$GNGGA' (NMEA sentence for latitude and longitude)
            if line.startswith("$GNGGA"):
                # Split the NMEA sentence into fields
                data = line.split(',')
                
                # Extract Latitude (assuming it's in the 2nd field)
                latitude = data[2]
                
                # Extract Longitude (assuming it's in the 4th field)
                longitude = data[4]
                
                # Update the labels for latitude and longitude
                lat_var.set(f"Latitude: {latitude}")
                long_var.set(f"Longitude: {longitude}")
            
            # Check if the line starts with '$GPVTG' (NMEA sentence for course and speed)
            if line.startswith("$GPVTG"):
                # Split the NMEA sentence into fields
                data = line.split(',')
                
                # Extract Ground Speed (GS) in knots (assuming it's in the 7th field)
                speed_knots = data[7]
                
                # Convert speed from knots to mph
                speed_mph = float(speed_knots) * 1.15078
                
                # Extract Course (assuming it's in the 1st field)
                course = data[1]
                
                # Calculate the direction based on the course value
                direction_index = int((float(course) + 22.5) / 45) % 8
                directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
                direction = directions[direction_index]
                
                # Update the labels for speed and direction
                speed_var.set(f"Speed: {speed_mph:.2f} mph")
                direction_var.set(f"Direction: {direction}")
                
    except KeyboardInterrupt:
        # Close the serial port when the program is interrupted
        ser.close()

# Create a thread for updating GPS data and pass the ser variable
gps_thread = threading.Thread(target=update_gps_data)

# Start updating GPS data in a separate thread
gps_thread.start()

# Start the Tkinter mainloop
root.mainloop()
