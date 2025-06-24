// Pin definitions
const int selectPins[4] = {2, 3, 4, 5}; // S0, S1, S2 pins for 74HC4051
const int analogInPin = A0;           // Analog input pin connected to Z pin of multiplexer
const int numChannels = 16;            // Number of channels (74HC4051 has 8 channels)
String prev_res = "";

// Function to select multiplexer channel (0-7)
void selectChannel(int channel) {
  for (int i = 0; i < 4; i++) {
    digitalWrite(selectPins[i], bitRead(channel, i));
  }
}

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set select pins as outputs
  for (int i = 0; i < 4; i++) {
    pinMode(selectPins[i], OUTPUT);
  }
}

void loop() {
  // Read all 8 channels
  String res = "";
  String tempChannel="";
  for (int channel = 0; channel < numChannels; channel++) {
    // Select the channel
    selectChannel(channel);
    
    // Read the analog value
    int value = analogRead(analogInPin);
    
    // Print the channel and value
    if (value != 1023) {
      res = "A" + String(channel) + ":" + String(value) + ",";
      tempChannel=String(channel);
    }

    if (tempChannel == prev_res) {
      res = "None";
    }
    
    // Small delay for stable readings
    delay(25);
  }
  if (res == "") {
    res = "None";
  }
  prev_res = tempChannel;
  Serial.println(res);
  
  // Add a delay between complete scans
  //delay(100);
}
