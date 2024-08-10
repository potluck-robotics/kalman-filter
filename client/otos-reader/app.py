import serial
import serial.tools.list_ports
from key import Key

key = Key()

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

# loop
while True:
    # Read 24 bytes from serial port
    data = ser.read(24)

    # flush left over data
    ser.flushInput()

    # save first 2 bytes of data to variable deltaRRaw as int16
    deltaRRaw = int.from_bytes(data[0:2], byteorder='little', signed=True)
    deltaPRaw = int.from_bytes(data[2:4], byteorder='little', signed=True)
    deltaHRaw = int.from_bytes(data[4:6], byteorder='little', signed=True)
    accelXRaw = int.from_bytes(data[6:8], byteorder='little', signed=True)
    accelYRaw = int.from_bytes(data[8:10], byteorder='little', signed=True)
    accelZRaw = int.from_bytes(data[10:12], byteorder='little', signed=True)
    deltaXRaw = int.from_bytes(data[14:16], byteorder='little', signed=True)
    deltaYRaw = int.from_bytes(data[16:18], byteorder='little', signed=True)

    # print in one line with fixed width
    print(f'deltaR: {deltaRRaw:5d} deltaP: {deltaPRaw:5d} deltaH: {deltaHRaw:5d} accelX: {accelXRaw:5d} accelY: {accelYRaw:5d} accelZ: {accelZRaw:5d} deltaX: {deltaXRaw:5d} deltaY: {deltaYRaw:5d}')
    
    # Read key from keyboard and quit if 'q' is pressed
    c = key.read()
    if c == 'q':
        break

# Close serial port
ser.close()

