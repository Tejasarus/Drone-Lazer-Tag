#define button1 4
#define button2 5
#define button3 6

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  pinMode(button3, INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if(digitalRead(button1) == 0)
  {
    Serial.println("button1");
  }
  if(digitalRead(button2) == 0)
  {
    Serial.println("button2");
  }
  if(digitalRead(button3) == 0)
  {
    Serial.println("button3");
  }
  delay(100);
}
