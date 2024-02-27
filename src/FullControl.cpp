#include <Arduino.h>


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
int penMaxUP = 35;      //To max high pen = small number
int penMaxDOWN = 55;    // To max low pen = more number
  // Sterring matrix
int plate_matrix_x = 0;
int plate_matrix_y = 0;
int plate_matrix_x_max = 55;
int plate_matrix_y_max = 60;
int current_x = 0;
int current_y = 0;
String komenda= "";


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

int parametr1 = 0;
int parametr2 = 0;

void loop() {

  if(digitalRead(check) == LOW){
    analogWrite(Fan, 0); //cooling=0;
  }else{
    analogWrite(Fan, 230); //cooling
  }

  // penDOWN();
  // StepXmotorX(10);
  // StepYmotorY(10);
  // StepYmotorX(10);
  // StepXmotorY(10);
  // penUP();
  // delay(1000);


  if(Serial.available() > 0){
    while(Serial.available() > 0 && status != true){
      komenda = Serial.readStringUntil('\n');
      komenda.trim();
        
      if(komenda.startsWith("M")) { // Sprawdź czy komenda zaczyna się od "M"
        int pozycjaPrzecinka = komenda.indexOf(','); // Znajdź pozycję przecinka
        if(pozycjaPrzecinka != -1 && komenda.length() > pozycjaPrzecinka + 1) { // Upewnij się, że znaleziono przecinek i są znaki po nim
          String parametr1_str = komenda.substring(2, pozycjaPrzecinka); // Pobierz pierwszy parametr
          String parametr2_str = komenda.substring(pozycjaPrzecinka + 1); // Pobierz drugi parametr

          parametr1 = parametr1_str.toInt(); // Konwertuj pierwszy parametr na liczbę
          parametr2 = parametr2_str.toInt(); // Konwertuj drugi parametr na liczbę

          komenda = "MoveTo";
          status = true;
        }

      }else if (komenda.equals("penUP") || komenda.equals("penDOWN")) {
        status = true;
      }
      }
      status = false;

      // Sprawdzenie czy komenda to "wlacz" i wykonanie odpowiednich działań
      if (komenda == "penUP") {
        penUP();
        Serial.println("OK");
      }

      if (komenda == "penDOWN") {
        penDOWN();
        Serial.println("OK");
      }

      // Sprawdzenie czy komenda to "MoveTo" i wykonanie odpowiednich działań
      if (komenda == "MoveTo") {
        MoveTo(parametr1,parametr2);
        Serial.println("OK");
      }

      // Wyzerowanie komendy po przetworzeniu
      komenda = "";
    }

}

// Funkcje do przesunięcia silników o n kroków
void StepXmotorX(int steps){
  // Wykonaj pełny obrót w jednym kierunku
  for (int i = 0; i < steps; i++) {
    stepForwardX();
  }
}
void StepYmotorX(int steps){
  // Wykonaj pełny obrót w przeciwnym kierunku
  for (int i = 0; i < steps; i++) {
    stepBackwardX();
  }
}
void StepXmotorY(int steps){
  // Wykonaj pełny obrót w jednym kierunku
  for (int i = 0; i < steps; i++) {
    stepForwardY();
  }
}
void StepYmotorY(int steps){
  // Wykonaj pełny obrót w przeciwnym kierunku
  for (int i = 0; i < steps; i++) {
    stepBackwardY();
  }
}

// Funkcja do obrotu silnika krokowego o jeden krok w prawo dla silnika X
void stepForwardX() {
  digitalWrite(InX1, HIGH);
  digitalWrite(InX2, HIGH);
  digitalWrite(InX3, LOW);
  digitalWrite(InX4, LOW);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InX1, LOW);
  digitalWrite(InX2, HIGH);
  digitalWrite(InX3, HIGH);
  digitalWrite(InX4, LOW);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InX1, LOW);
  digitalWrite(InX2, LOW);
  digitalWrite(InX3, HIGH);
  digitalWrite(InX4, HIGH);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InX1, HIGH);
  digitalWrite(InX2, LOW);
  digitalWrite(InX3, LOW);
  digitalWrite(InX4, HIGH);
  delay(XYdelay); // Czas na stabilizację
}
// Funkcja do obrotu silnika krokowego o jeden krok w lewo dla silnika X
void stepBackwardX() {
  digitalWrite(InX1, HIGH);
  digitalWrite(InX2, LOW);
  digitalWrite(InX3, LOW);
  digitalWrite(InX4, HIGH);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InX1, LOW);
  digitalWrite(InX2, LOW);
  digitalWrite(InX3, HIGH);
  digitalWrite(InX4, HIGH);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InX1, LOW);
  digitalWrite(InX2, HIGH);
  digitalWrite(InX3, HIGH);
  digitalWrite(InX4, LOW);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InX1, HIGH);
  digitalWrite(InX2, HIGH);
  digitalWrite(InX3, LOW);
  digitalWrite(InX4, LOW);
  delay(XYdelay); // Czas na stabilizację
}

// Funkcja do obrotu silnika krokowego o jeden krok w prawo dla silnika Y
void stepForwardY() {
  digitalWrite(InY1, HIGH);
  digitalWrite(InY2, HIGH);
  digitalWrite(InY3, LOW);
  digitalWrite(InY4, LOW);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InY1, LOW);
  digitalWrite(InY2, HIGH);
  digitalWrite(InY3, HIGH);
  digitalWrite(InY4, LOW);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InY1, LOW);
  digitalWrite(InY2, LOW);
  digitalWrite(InY3, HIGH);
  digitalWrite(InY4, HIGH);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InY1, HIGH);
  digitalWrite(InY2, LOW);
  digitalWrite(InY3, LOW);
  digitalWrite(InY4, HIGH);
  delay(XYdelay); // Czas na stabilizację
}
// Funkcja do obrotu silnika krokowego o jeden krok w lewo dla silnika Y
void stepBackwardY() {
  digitalWrite(InY1, HIGH);
  digitalWrite(InY2, LOW);
  digitalWrite(InY3, LOW);
  digitalWrite(InY4, HIGH);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InY1, LOW);
  digitalWrite(InY2, LOW);
  digitalWrite(InY3, HIGH);
  digitalWrite(InY4, HIGH);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InY1, LOW);
  digitalWrite(InY2, HIGH);
  digitalWrite(InY3, HIGH);
  digitalWrite(InY4, LOW);
  delay(XYdelay); // Czas na stabilizację
  digitalWrite(InY1, HIGH);
  digitalWrite(InY2, HIGH);
  digitalWrite(InY3, LOW);
  digitalWrite(InY4, LOW);
  delay(XYdelay); // Czas na stabilizację
}

void penUP(){
  for (int angle = penMaxDOWN; angle >= penMaxUP; angle--) {
    writeServo(angle);  // Ustaw kąt silnika
    delay(10);           // Poczekaj na zakończenie ruchu
  }
}

void penDOWN(){
  for (int angle = penMaxUP; angle <= penMaxDOWN; angle++) {
    writeServo(angle);  // Ustaw kąt silnika
    delay(10);           // Poczekaj na zakończenie ruchu
  }
}

void writeServo(int angle) {
  // Oblicz wartość PWM na podstawie kąta
  int duty_cycle = map(angle, 0, 180, 544, 2400);
  // Wysyłaj sygnał PWM na pin, do którego podłączony jest silnik
  digitalWrite(SERVO_PIN, HIGH);
  delayMicroseconds(duty_cycle);
  digitalWrite(SERVO_PIN, LOW);
  // Poczekaj na zakończenie cyklu PWM (typowy okres to 20 ms)
  delayMicroseconds(20000 - duty_cycle);
}

void MoveTo(int x, int y) {
  // Sprawdź, czy współrzędne znajdują się w dopuszczalnym zakresie
  if (x >= 0 && x <= plate_matrix_x_max && y >= 0 && y <= plate_matrix_y_max) {
    // Oblicz różnicę między aktualnym położeniem a docelowym położeniem
    int dx = x - current_x;
    int dy = y - current_y;

    // Wykonaj przesunięcie w osi X
    if (dx > 0) {
      StepXmotorX(dx); // Przesunięcie w prawo
    } else if (dx < 0) {
      StepYmotorX(abs(dx)); // Przesunięcie w lewo
    }

    // Wykonaj przesunięcie w osi Y
    if (dy > 0) {
      StepYmotorY(dy); // Przesunięcie w dół
    } else if (dy < 0) {
      StepXmotorY(abs(dy)); // Przesunięcie w górę
    }

    // Zaktualizuj aktualne położenie
    current_x = x;
    current_y = y;
  } else {
    Serial.println("Współrzędne poza zakresem!");
  }
}