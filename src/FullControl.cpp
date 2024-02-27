#include <Arduino.h>
#include "MemoryFree.h" // only for debug

// Pin definition for stem motor X (SM15L)
#define InX1 2
#define InX3 3
#define InX2 4
#define InX4 5
// Pin definition for stem motor Y (SM15L)
#define InY1 7
#define InY3 8
#define InY2 9
#define InY4 10
// Pin definition for stem motor Z (SG90)
#define SERVO_PIN 6
// Pin definition for Fan cooling
#define Fan 11 


// Variable definitions
int check = 12;         // Temporary check key input for rotate Fan
boolean status = false; // SerialPort status
int XYdelay = 12;       // Delay for end motor rotate (5 | 12)
int penMaxUP = 35;      // To max high pen = small number
int penMaxDOWN = 55;    // To max low pen = more number
  // Sterring matrix
int plate_matrix_x = 0;
int plate_matrix_y = 0;
int plate_matrix_x_max = 55;
int plate_matrix_y_max = 60;
int current_x = 0;
int current_y = 0;
String komenda= "";
const int MAX_SUBCOMMANDS = 20; // default=5, max=20
String podkomendy[MAX_SUBCOMMANDS];
int param1 = 0;
int param2 = 0;
int coutSubcommands;


// Function definitions
void StepXmotorX(int steps);
void StepYmotorX(int steps);
void StepXmotorY(int steps);
void StepYmotorY(int steps);
void writeServo(int angle);
void stepForwardX();
void stepBackwardX();
void stepForwardY();
void stepBackwardY();
void penUP();
void penDOWN();
void MoveTo(int x, int y);
void rozdzielKomendy(String commands_in);


void setup() {
  // Set serial port
  Serial.begin(9600);

  // Set output pins
  pinMode(InX1, OUTPUT);
  pinMode(InX2, OUTPUT);
  pinMode(InX3, OUTPUT);
  pinMode(InX4, OUTPUT);
  pinMode(InY1, OUTPUT);
  pinMode(InY2, OUTPUT);
  pinMode(InY3, OUTPUT);
  pinMode(InY4, OUTPUT);
  pinMode(SERVO_PIN, OUTPUT);
  pinMode(Fan, OUTPUT);
  pinMode(check, INPUT); // temporary pins for key input

  // Setup for starting work
  penUP();             // For start pen to high position
  analogWrite(Fan, 0); // Turn off fan (Fan start (0-255))
  // MoveTo(0, 0);
  

}


void loop() {
  status = false;
  if(digitalRead(check) == LOW){
    analogWrite(Fan, 0); //cooling=0;
  }else{
    analogWrite(Fan, 230); //cooling
  }

  if(Serial.available() > 0){
    while(Serial.available() > 0 && status != true){
      komenda = Serial.readStringUntil('\n');
      komenda.trim();
      rozdzielKomendy(komenda);
      for (int i = 0; i < coutSubcommands; i++) {
        // Serial.println(podkomendy[i]);
        // Serial.print("Free RAM: ");
        Serial.println(freeMemory());
        if(podkomendy[i].startsWith("M")) { // Check if the command starts with "M"
            int pozycjaPrzecinka = podkomendy[i].indexOf(','); // Find the position of the comma
          if(pozycjaPrzecinka != -1 && podkomendy[i].length() > pozycjaPrzecinka + 1) { // Make sure the comma is found and there are characters after it
            String parametr1_str = podkomendy[i].substring(2, pozycjaPrzecinka); // Get first parameter
            String parametr2_str = podkomendy[i].substring(pozycjaPrzecinka + 1); // Get second parameter

            param1 = parametr1_str.toInt(); // Convert the first parameter to a number
            param2 = parametr2_str.toInt(); // Convert the second parameter to a number

            // analogWrite(Fan, 230);
            MoveTo(param1,param2);
            // analogWrite(Fan, 0);
            //delay(500);
            Serial.println(podkomendy[i]);
            
            status = true;
          }
        }else if (podkomendy[i].equals("penUP")){
          penUP();
        }else if (podkomendy[i].equals("penDOWN")) {
          penDOWN();
        }
      }
      status = true;
    }
    coutSubcommands = 0;
    komenda = "";
    Serial.println("OK");
  }

}

// Functions to move motors by n steps
void StepXmotorX(int steps){
  // Make a full turn in one direction
  for (int i = 0; i < steps; i++) {
    stepForwardX();
  }
}
void StepYmotorX(int steps){
  // Make a full turn in the opposite direction
  for (int i = 0; i < steps; i++) {
    stepBackwardX();
  }
}
void StepXmotorY(int steps){
  // Make a full turn in one direction
  for (int i = 0; i < steps; i++) {
    stepForwardY();
  }
}
void StepYmotorY(int steps){
  // Make a full turn in the opposite direction
  for (int i = 0; i < steps; i++) {
    stepBackwardY();
  }
}

// Function to rotate the stepper motor one step to the right for motor X
void stepForwardX() {
  digitalWrite(InX1, HIGH);
  digitalWrite(InX2, HIGH);
  digitalWrite(InX3, LOW);
  digitalWrite(InX4, LOW);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InX1, LOW);
  digitalWrite(InX2, HIGH);
  digitalWrite(InX3, HIGH);
  digitalWrite(InX4, LOW);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InX1, LOW);
  digitalWrite(InX2, LOW);
  digitalWrite(InX3, HIGH);
  digitalWrite(InX4, HIGH);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InX1, HIGH);
  digitalWrite(InX2, LOW);
  digitalWrite(InX3, LOW);
  digitalWrite(InX4, HIGH);
  delay(XYdelay); // Time for stabilization
}
// Function to rotate the stepper motor one step to the left for motor X
void stepBackwardX() {
  digitalWrite(InX1, HIGH);
  digitalWrite(InX2, LOW);
  digitalWrite(InX3, LOW);
  digitalWrite(InX4, HIGH);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InX1, LOW);
  digitalWrite(InX2, LOW);
  digitalWrite(InX3, HIGH);
  digitalWrite(InX4, HIGH);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InX1, LOW);
  digitalWrite(InX2, HIGH);
  digitalWrite(InX3, HIGH);
  digitalWrite(InX4, LOW);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InX1, HIGH);
  digitalWrite(InX2, HIGH);
  digitalWrite(InX3, LOW);
  digitalWrite(InX4, LOW);
  delay(XYdelay); // Time for stabilization
}

// Function to rotate the stepper motor one step to the right for the Y motor
void stepForwardY() {
  digitalWrite(InY1, HIGH);
  digitalWrite(InY2, HIGH);
  digitalWrite(InY3, LOW);
  digitalWrite(InY4, LOW);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InY1, LOW);
  digitalWrite(InY2, HIGH);
  digitalWrite(InY3, HIGH);
  digitalWrite(InY4, LOW);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InY1, LOW);
  digitalWrite(InY2, LOW);
  digitalWrite(InY3, HIGH);
  digitalWrite(InY4, HIGH);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InY1, HIGH);
  digitalWrite(InY2, LOW);
  digitalWrite(InY3, LOW);
  digitalWrite(InY4, HIGH);
  delay(XYdelay); // Time for stabilization
}
// Function to rotate the stepper motor one step to the left for the Y motor
void stepBackwardY() {
  digitalWrite(InY1, HIGH);
  digitalWrite(InY2, LOW);
  digitalWrite(InY3, LOW);
  digitalWrite(InY4, HIGH);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InY1, LOW);
  digitalWrite(InY2, LOW);
  digitalWrite(InY3, HIGH);
  digitalWrite(InY4, HIGH);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InY1, LOW);
  digitalWrite(InY2, HIGH);
  digitalWrite(InY3, HIGH);
  digitalWrite(InY4, LOW);
  delay(XYdelay); // Time for stabilization
  digitalWrite(InY1, HIGH);
  digitalWrite(InY2, HIGH);
  digitalWrite(InY3, LOW);
  digitalWrite(InY4, LOW);
  delay(XYdelay); // Time for stabilization
}

void penUP(){
  for (int angle = penMaxDOWN; angle >= penMaxUP; angle--) {
    writeServo(angle); // Set the engine angle
    delay(10);         // Wait for the movement to complete
  }
}

void penDOWN(){
  for (int angle = penMaxUP; angle <= penMaxDOWN; angle++) {
    writeServo(angle); // Set the engine angle
    delay(10);         // Wait for the movement to complete
  }
}

void writeServo(int angle) {
  // Calculate the PWM value based on the angle
  int duty_cycle = map(angle, 0, 180, 544, 2400);
  // Send a PWM signal to the pin to which the motor is connected
  digitalWrite(SERVO_PIN, HIGH);
  delayMicroseconds(duty_cycle);
  digitalWrite(SERVO_PIN, LOW);
  // Wait for the PWM cycle to complete (typical period is 20 ms)
  delayMicroseconds(20000 - duty_cycle);
}

void MoveTo(int x, int y) {
  // Check if the coordinates are within the allowed range
  if (x >= 0 && x <= plate_matrix_x_max && y >= 0 && y <= plate_matrix_y_max) {
    // Calculate the difference between your current location and your target location
    int dx = x - current_x;
    int dy = y - current_y;

    // Make a shift in the X axis
    if (dx > 0) {
      StepXmotorX(dx); // Swipe right
    } else if (dx < 0) {
      StepYmotorX(abs(dx)); // Swipe left
    }

    // Perform a Y-axis shift
    if (dy > 0) {
      StepYmotorY(dy); // Shift down
    } else if (dy < 0) {
      StepXmotorY(abs(dy)); // Shift up
    }

    // Update your current location
    current_x = x;
    current_y = y;
  } else {
    Serial.println("Współrzędne poza zakresem!");
  }
}

void rozdzielKomendy(String commands_in) {
    coutSubcommands = 1; // The number of subcommands starts from 1 because there will always be 1 more than the number of ';' characters
    int index = 0;
    int startIndex = 0;
    // Split the command into subcommands
    for (int i = 0; i < commands_in.length(); i++) {
        if (commands_in.charAt(i) == ';') {
            podkomendy[index++] = commands_in.substring(startIndex, i);
            startIndex = i + 1;
        }
    }
    // Add the last subcommand (left after the last semicolon)
    podkomendy[index] = commands_in.substring(startIndex);
    coutSubcommands = index + 1; // Set the number of subcommands to index + 1
}