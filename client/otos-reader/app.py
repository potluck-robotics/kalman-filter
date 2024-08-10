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

# print header in one line with fixed width and separated by comma
print(f'deltaR, deltaP, deltaH, accelX, accelY, accelZ, deltaX, deltaY')

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
    #print(f'deltaR: {deltaRRaw:5d} deltaP: {deltaPRaw:5d} deltaH: {deltaHRaw:5d} accelX: {accelXRaw:5d} accelY: {accelYRaw:5d} accelZ: {accelZRaw:5d} deltaX: {deltaXRaw:5d} deltaY: {deltaYRaw:5d}')

    # convert sensor data to proper units

    # paa scale factor: 20k dpi
    # Set PAA5160 resolution to max (20k dpi)
    # Compute the raw to inch and meter conversion factors
    resX = 199.0
    resY = 199.0
    _rawToInchX = 1.0 / ((resX + 1.0) * 100.0)
    _rawToInchY = 1.0 / ((resY + 1.0) * 100.0)
    _rawToMeterX = _rawToInchX * 0.0254
    _rawToMeterY = _rawToInchY * 0.0254

    # lsm scale factor: gyro 16g and accel 2000dps
    # Convert from degrees to radians (pi/180 = 0.01745329252)
    kLsm6dsoRawToDps2000 = 70e-3
    kLsm6dsoRawToG16g = 0.488e-3

    _rawToDps = kLsm6dsoRawToDps2000
    _rawToG = kLsm6dsoRawToG16g

    _rawToRps = _rawToDps * 0.01745329252 # 0.01745329252 = pi/180
    _rawToMps2 = _rawToG * 9.80665 # 9.80665 m/s^2 = 1G
    
    # raw data to proper units
    deltaR = deltaRRaw * _rawToRps
    deltaP = deltaPRaw * _rawToRps
    deltaH = deltaHRaw * _rawToRps
    accelX = accelXRaw * _rawToMps2
    accelY = -(accelYRaw * _rawToMps2)
    accelZ = accelZRaw * _rawToMps2
    deltaX = deltaXRaw * _rawToMeterX
    deltaY = deltaYRaw * _rawToMeterY


    # print in one line with fixed width and only values separated by comma the decimal point is fixed to 5.5
    print(f'{deltaR:5.5f}, {deltaP:5.5f}, {deltaH:5.5f}, {accelX:5.5f}, {accelY:5.5f}, {accelZ:5.5f}, {deltaX:5.5f}, {deltaY:5.5f}')

    # Read key from keyboard and quit if 'q' is pressed
    c = key.read()
    if c == 'q':
        break

# Close serial port
ser.close()

