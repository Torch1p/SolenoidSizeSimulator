#include <Servo.h>

Servo myServo;

// Define pins for 4 sensors
const int sensor1Pin = A0;
const int sensor2Pin = A1;
const int sensor3Pin = A2;
const int sensor4Pin = A3;
const int servoPin = 9;

// Define thresholds for each sensor
const int threshold1 = 50;
const int threshold2 = 20;
const int threshold3 = 20;
const int threshold4 = 20;

// Timing variables
unsigned long sensor1Time = 0;
unsigned long sensor2Time = 0;
unsigned long sensor3Time = 0;
unsigned long sensor4Time = 0;

// Time differences
unsigned long time1to2 = 0;
unsigned long time2to3 = 0;
unsigned long time3to4 = 0;
unsigned long totalTime = 0;

// Trigger flags
bool sensor1Triggered = false;
bool sensor2Triggered = false;
bool sensor3Triggered = false;
bool sensor4Triggered = false;

// Control variables
unsigned long lastReadTime = 0;
const unsigned long readInterval = 1;

// Servo control variables
int currentServoPos = 110;
int targetServoPos = 110;
unsigned long lastServoMove = 0;
const int servoMoveDelay = 20;
bool isMovingDown = false;
bool isWaiting = false;
unsigned long waitStartTime = 0;
const unsigned long waitDuration = 1000;

// Measurement counter
int measurementCount = 0;

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  myServo.write(currentServoPos);
  
  // Print CSV header
  Serial.println("Measurement,Time1to2(ms),Time2to3(ms),Time3to4(ms),TotalTime(ms)");
}

void loop() {
  unsigned long currentTime = millis();
  
  // Servo control
  if (Serial.available() > 0) {
    char input = Serial.read();
    if (input == 'y' && currentServoPos == 110) {
      targetServoPos = 60;
      isMovingDown = true;
    }
  }

  // Handle servo movement
  if (currentTime - lastServoMove >= servoMoveDelay) {
    lastServoMove = currentTime;
    
    if (isMovingDown && !isWaiting) {
      if (currentServoPos > targetServoPos) {
        currentServoPos--;
        myServo.write(currentServoPos);
      } else {
        isWaiting = true;
        waitStartTime = currentTime;
      }
    } else if (isWaiting && (currentTime - waitStartTime >= waitDuration)) {
      isWaiting = false;
      isMovingDown = false;
      targetServoPos = 110;
    } else if (!isMovingDown && !isWaiting) {
      if (currentServoPos < targetServoPos) {
        currentServoPos++;
        myServo.write(currentServoPos);
      }
    }
  }

  // Sensor reading and timing logic
  if (currentTime - lastReadTime >= readInterval) {
    lastReadTime = currentTime;

    int sensor1Value = analogRead(sensor1Pin);
    int sensor2Value = analogRead(sensor2Pin);
    int sensor3Value = analogRead(sensor3Pin);
    int sensor4Value = analogRead(sensor4Pin);
    
    // Sensor 1 (now first sensor)
    if (!sensor1Triggered && sensor1Value < threshold1) {
      sensor1Time = currentTime;
      sensor1Triggered = true;
    }
    
    // Sensor 2
    if (sensor1Triggered && !sensor2Triggered && sensor2Value < threshold2) {
      sensor2Time = currentTime;
      sensor2Triggered = true;
      time1to2 = sensor2Time - sensor1Time;
    }
    
    // Sensor 3
    if (sensor2Triggered && !sensor3Triggered && sensor3Value < threshold3) {
      sensor3Time = currentTime;
      sensor3Triggered = true;
      time2to3 = sensor3Time - sensor2Time;
    }
    
    // Sensor 4 (final sensor)
    if (sensor3Triggered && !sensor4Triggered && sensor4Value < threshold4) {
      sensor4Time = currentTime;
      sensor4Triggered = true;
      time3to4 = sensor4Time - sensor3Time;
      totalTime = sensor4Time - sensor1Time;  // Total time now from sensor 1 to 4
      
      // Increment measurement counter
      measurementCount++;
      
      // Print final results
      Serial.println("\n=== FINAL RESULTS ===");
      Serial.print("Time 1->2: "); Serial.print(time1to2); Serial.println(" us");
      Serial.print("Time 2->3: "); Serial.print(time2to3); Serial.println(" us");
      Serial.print("Time 3->4: "); Serial.print(time3to4); Serial.println(" us");
      Serial.print("Total time (1->4): "); Serial.print(totalTime); Serial.println(" us");
      Serial.println("===================\n");
      
      // Reset all triggers for next measurement
      sensor1Triggered = false;
      sensor2Triggered = false;
      sensor3Triggered = false;
      sensor4Triggered = false;
    }
  }
}