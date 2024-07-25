//Naming to match the board
const int A_1 = A0;

void setup() 
{
  pinMode(A_1, INPUT);
  Serial.begin(9600);
}

void loop() 
{
  //Scan for resistors being placed down
  if (analogRead(A_1) != 0){
    Serial.println("A1:" + String(analogRead(A_1)));
    delay(500);
  }

  //Commands passed from Python
  if (Serial.available() > 0)
    {
      String cmd = Serial.readString();

      //if (cmd == "end")
    }
}
