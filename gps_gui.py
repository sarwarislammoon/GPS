import serial
import tkinter as tk
from tkinter.font import Font
import threading

# Define the serial port and baud rate for your GPS module
serial_port = "COM8"  # Adjust the port name as needed
baud_rate = 9600

# Create a Tkinter window
root = tk.Tk()
root.title("GPS Data")
root.geometry("400x200")  # Set window dimensions

# Create a large font
large_font = Font(family="Helvetica", size=20)

# Create labels for displaying data
speed_label = tk.Label(root, text="Speed:", font=large_font)
direction_label = tk.Label(root, text="Direction:", font=large_font)
lat_label = tk.Label(root, text="LAT:", font=large_font)
long_label = tk.Label(root, text="Long:", font=large_font)

# Create StringVar variables to update labels
speed_var = tk.StringVar()
direction_var = tk.StringVar()
lat_var = tk.StringVar()
long_var = tk.StringVar()

# Create label widgets using StringVar
speed_value_label = tk.Label(root, textvariable=speed_var, font=large_font)
direction_value_label = tk.Label(root, textvariable=direction_var, font=large_font)
lat_value_label = tk.Label(root, textvariable=lat_var, font=large_font)
long_value_label = tk.Label(root, textvariable=long_var, font=large_font)

# Pack the labels in a grid with evenly spaced widgets
speed_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
speed_value_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")
direction_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
direction_value_label.grid(row=1, column=1, padx=10, pady=10, sticky="e")
lat_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
lat_value_label.grid(row=2, column=1, padx=10, pady=10, sticky="e")
long_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
long_value_label.grid(row=3, column=1, padx=10, pady=10, sticky="e")

# Open the serial port
try:
    ser = serial.Serial(serial_port, baud_rate)
except Exception as e:
    print(f"Error opening serial port: {e}")
    root.destroy()

# Function to continuously update GPS data
def update_gps_data(ser):
    try:
        while True:
            # Read a line of data from the GPS module
            line = ser.readline().decode('utf-8').strip()
            
            # Check if the line starts with '$GPVTG' (NMEA sentence for course and speed)
            if line.startswith("$GPVTG"):
                # Split the NMEA sentence into fields
                data = line.split(',')
                
                # Extract True Course (TC) in degrees (assuming it's in the 1st field)
                course = data[1]
                
                # Extract Ground Speed (GS) in knots (assuming it's in the 7th field)
                speed_knots = data[7]
                
                # Convert speed from knots to mph
                speed_mph = float(speed_knots) * 1.15078
                
                # Calculate the direction based on the course value
                directions = ["North", "North-Northeast", "Northeast", "East-Northeast",
                              "East", "East-Southeast", "Southeast", "South-Southeast",
                              "South", "South-Southwest"]
                direction_index = int((float(course) + 22.5) / 45) % 10
                direction = directions[direction_index]
                
                # Update the labels
                speed_var.set(f"{speed_mph:.2f} mph")
                direction_var.set(direction)
                
    except KeyboardInterrupt:
        # Close the serial port when the program is interrupted
        ser.close()

# Create a thread for updating GPS data and pass the ser variable
gps_thread = threading.Thread(target=update_gps_data, args=(ser,))

# Start updating GPS data in a separate thread
gps_thread.start()

# Start the Tkinter mainloop
root.mainloop()
