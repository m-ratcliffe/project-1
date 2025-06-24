const int A_1 = A0;
const int A_2 = A1;
const int A_3 = A2;
const int A_4 = A3;
const int B_1 = A4;
const int B_2 = A5;
const int B_3 = A6;
const int B_4 = A7;
const int C_1 = A8;
const int C_2 = A9;
const int C_3 = A10;
const int C_4 = A11;
const int D_1 = A12;
const int D_2 = A13;
const int D_3 = A14;
const int D_4 = A15;

void setup() 
{
  pinMode(A_1, INPUT);
  pinMode(A_2, INPUT);
  pinMode(A_3, INPUT);
  pinMode(A_4, INPUT);
  pinMode(B_1, INPUT);
  pinMode(B_2, INPUT);
  pinMode(B_3, INPUT);
  pinMode(B_4, INPUT);
  pinMode(C_1, INPUT);
  pinMode(C_2, INPUT);
  pinMode(C_3, INPUT);
  pinMode(C_4, INPUT);
  pinMode(D_1, INPUT);
  pinMode(D_2, INPUT);
  pinMode(D_3, INPUT);
  pinMode(D_4, INPUT);
  Serial.begin(9600);
}

void loop() 
{
  //Scan for resistors being placed down
  if (analogRead(A_1) != 0){
    Serial.println("A1:" + String(analogRead(A_1)));
    delay(500);
  }
  if (analogRead(A_2) != 0){
    Serial.println("A2:" + String(analogRead(A_2)));
    delay(500);
  }
  if (analogRead(A_3) != 0){
    Serial.println("A3:" + String(analogRead(A_3)));
    delay(500);
  }
  if (analogRead(A_4) != 0){
    Serial.println("A4:" + String(analogRead(A_4)));
    delay(500);
  }
  if (analogRead(B_1) != 0){
    Serial.println("B1:" + String(analogRead(B_1)));
    delay(500);
  }
  if (analogRead(B_2) != 0){
    Serial.println("B2:" + String(analogRead(B_2)));
    delay(500);
  }
  if (analogRead(B_3) != 0){
    Serial.println("B3:" + String(analogRead(B_3)));
    delay(500);
  }
  if (analogRead(B_4) != 0){
    Serial.println("B4:" + String(analogRead(B_4)));
    delay(500);
  }
  if (analogRead(C_1) != 0){
    Serial.println("C1:" + String(analogRead(C_1)));
    delay(500);
  }
  if (analogRead(C_2) != 0){
    Serial.println("C2:" + String(analogRead(C_2)));
    delay(500);
  }
  if (analogRead(C_3) != 0){
    Serial.println("C3:" + String(analogRead(C_3)));
    delay(500);
  }
  if (analogRead(C_4) != 0){
    Serial.println("C4:" + String(analogRead(C_4)));
    delay(500);
  }
  if (analogRead(D_1) != 0){
    Serial.println("D1:" + String(analogRead(D_1)));
    delay(500);
  }
  if (analogRead(D_2) != 0){
    Serial.println("D2:" + String(analogRead(D_2)));
    delay(500);
  }
  if (analogRead(D_3) != 0){
    Serial.println("D3:" + String(analogRead(D_3)));
    delay(500);
  }
  if (analogRead(D_4) != 0){
    Serial.println("D4:" + String(analogRead(D_4)));
    delay(500);
  }

  //Commands passed from Python
  if (Serial.available() > 0)
    {
      String cmd = Serial.readString();

      //if (cmd == "end")
    }
}
