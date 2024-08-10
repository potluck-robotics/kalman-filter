import serial
import serial.tools.list_ports

# Find available serial port and save it to varialble port
def find_serial_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == 0x1b4f and port.pid == 0x9206:
            return port.device

# Get find available serial port from usb id 1b4f:9206
port = find_serial_port()

# Open serial port
ser = serial.Serial(port, 2000000)

# Write enter key to serial port
ser.write(b'\r\n')
print(ser.readline())

# Read 24 bytes from serial port
data = ser.read(24)

# print in hex
print(data.hex())
