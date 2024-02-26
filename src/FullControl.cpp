#include <Arduino.h>


// Definicje pinów dla silnika krokowego X
#define InX1 2
#define InX2 4
#define InX3 3
#define InX4 5
// Definicje pinów dla silnika krokowego Y
#define InY1 7
#define InY2 9
#define InY3 8
#define InY4 10

int check = 12;

int XYdelay = 12; // 5 // 12
void stepForwardX();
void stepBackwardX();
void stepForwardY();
void stepBackwardY();
void MoveTo(int x, int y);

void StepXmotorX(int steps);
void StepYmotorX(int steps);
void StepXmotorY(int steps);
void StepYmotorY(int steps);

#define SERVO_PIN 6  // Definicja pinu, do którego podłączony jest silnik SG90
int penMaxDOWN = 55; // więcej = niżej
int penMaxUP = 35; //mniej = wyżej
void writeServo(int angle);
void penUP();
void penDOWN();

// Sterowanie planszą
int plate_matrix_x = 0;
int plate_matrix_y = 0;

int plate_matrix_x_max = 55;
int plate_matrix_y_max = 60;

int current_x = 0;
int current_y = 0;

void setup() {
  Serial.println("Hello");
  pinMode(check, INPUT);

  // Ustawienie pinów jako wyjścia
  pinMode(InX1, OUTPUT);
  pinMode(InX2, OUTPUT);
  pinMode(InX3, OUTPUT);
  pinMode(InX4, OUTPUT);
  pinMode(InY1, OUTPUT);
  pinMode(InY2, OUTPUT);
  pinMode(InY3, OUTPUT);
  pinMode(InY4, OUTPUT);

  pinMode(SERVO_PIN, OUTPUT);  // Ustaw pin jako wyjście
  penUP();

  pinMode(11, OUTPUT);
  
  analogWrite(11, 0); // Fan start (0-255)
  
  // MoveTo(0, 0);
  

}


void loop() {

  if(digitalRead(check) == LOW){
    analogWrite(11, 0); //cooling=0;
  }else{
    analogWrite(11, 230); //cooling
  }

  // penDOWN();
  // StepXmotorX(10);
  // StepYmotorY(10);
  // StepYmotorX(10);
  // StepXmotorY(10);
  // penUP();
  //delay(1000);

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