#include "SparkFun_Qwiic_OTOS_Arduino_Library.h"
#include "Wire.h"

QwiicOTOS myOtos;
byte buffer[24]; // lsm + paa registers
//byte buffer[96];  // all registers
byte lsmData[12];
byte paaData[12];

void setup() {
  // Start serial
  Serial.begin(115200);
  Serial.println("Qwiic OTOS Example 1 - Basic Readings");

  Wire.begin();

  // Attempt to begin the sensor
  while (myOtos.begin() == false) {
    Serial.println("OTOS not connected, check your wiring and I2C address!");
    delay(1000);
  }

  Serial.println("OTOS connected!");

  Serial.println("Ensure the OTOS is flat and stationary, then enter any key to calibrate the IMU");

  // Clear the serial buffer
  while (Serial.available())
    Serial.read();
  // Wait for user input
  while (!Serial.available())
    ;

  Serial.println("Calibrating IMU...");

  // Calibrate the IMU, which removes the accelerometer and gyroscope offsets
  myOtos.calibrateImu();

  // Reset the tracking algorithm - this resets the position to the origin,
  // but can also be used to recover from some rare tracking errors
  myOtos.resetTracking();

  delay(1000);
  sfe_otos_pose2d_t myPosition;
  myOtos.getPosition(myPosition);
  // Print measurement
  Serial.println();
  Serial.println("Position:");
  Serial.print("X (Inches): ");
  Serial.println(myPosition.x);
  Serial.print("Y (Inches): ");
  Serial.println(myPosition.y);
  Serial.print("Heading (Degrees): ");
  Serial.println(myPosition.h);
}

void loop() {
  int i = 0;

  Wire.beginTransmission(0x17); // 0x17 is OTOS i2c address
  Wire.write(0x44);  // from lsm gyro: https://github.com/sparkfun/SparkFun_Optical_Tracking_Odometry_Sensor/blob/737950b14e4e960c40c73ddc157a2b9d9fe7224e/Firmware/SFE/Inc/registers.h#L71C15-L71C31
  // Wire.write(0x00); // from product id
  Wire.endTransmission();

  Wire.requestFrom(0x17, 24);  // request 24 bytes of raw sensor values
  // Wire.requestFrom(0x17, 96);    // request 96 bytes of whole registers

  while (Wire.available()) {  // slave may send less than requested
    char c = Wire.read();     // receive a byte as character
    buffer[i] = c;
    i++;
  }

  // print OTOS  registers
  // for (int i = 0; i < sizeof(buffer); i++) {
  //   if (buffer[i] < 0x10) { // 한 자리 수인 경우
  //     Serial.print("0"); // 앞에 '0' 추가
  //   }
  //   Serial.print(buffer[i], HEX);
  //   Serial.print(" ");
  // }

  memcpy(lsmData, buffer, 12);
  memcpy(paaData, buffer + 12, 12);

  // ref: https://github.com/sparkfun/SparkFun_Optical_Tracking_Odometry_Sensor/blob/737950b14e4e960c40c73ddc157a2b9d9fe7224e/Firmware/SFE/Src/main.cpp#L283
  int16_t deltaRRaw = (lsmData[1] << 8) | lsmData[0];
  int16_t deltaPRaw = (lsmData[3] << 8) | lsmData[2];
  int16_t deltaHRaw = (lsmData[5] << 8) | lsmData[4];
  int16_t accelXRaw = (lsmData[7] << 8) | lsmData[6];
  int16_t accelYRaw = (lsmData[9] << 8) | lsmData[8];
  int16_t accelZRaw = (lsmData[11] << 8) | lsmData[10];
  int16_t deltaXRaw = (paaData[3] << 8) | paaData[2];
  int16_t deltaYRaw = (paaData[5] << 8) | paaData[4];

  // LSM6DSO gyro
  Serial.print(deltaRRaw);
  Serial.print(", ");
  Serial.print(deltaPRaw);
  Serial.print(", ");
  Serial.print(deltaHRaw);
  Serial.print(" ");

  // LSM6DSO accel
  Serial.print(accelXRaw);
  Serial.print(", ");
  Serial.print(accelYRaw);
  Serial.print(", ");
  Serial.print(accelZRaw);
  Serial.print(" ");

  // paa5160E1 optical flow 
  Serial.print(deltaXRaw);
  Serial.print(", ");
  Serial.print(deltaYRaw);
  Serial.println();
  
  // TODO: need to convert unit, ref: https://github.com/sparkfun/Qwiic_OTOS_Py/blob/master/qwiic_otos.py

  delay(2);
}
