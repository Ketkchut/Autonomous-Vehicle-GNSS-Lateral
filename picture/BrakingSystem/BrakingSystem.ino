#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int pos = 0;    // variable to store the servo position
int val = 0;

void setup() {
  myservo.write(pos); //set initial
  myservo.attach(5);  // attaches the servo on pin 5 to the servo object
  Serial.print("Pos = ");
  Serial.print(pos);
  Serial.print("\n");
  delay(15);
}

void loop() {
  val = analogRead(A1);
  Serial.print("Val = ");
  Serial.print(val);
  Serial.print("\t");
  Serial.print("Pos = ");
  Serial.print(pos);
  Serial.print("\n");
  if (val == 0 && pos <= 0) { // goes from 0 degrees to 180 degrees in steps of 1 degree
    for (pos = 0; pos <= 180; pos += 1) { 
      myservo.write(pos);              // tell servo to go to position in variable 'pos'myservo.write(pos);              // tell servo to go to position in variable 'pos'
      Serial.print(pos);
      Serial.print("\n");
      delay(10);
    }
  }    else if (val == 1023 && pos >= 180) { // goes from 180 degrees to 0 degrees
    for (pos = 180; pos >= 0; pos -= 1) { 
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      Serial.print(pos);
      Serial.print("\n");
      delay(10);                       // waits 15ms for the servo to reach the position
    }
  }
  delay(1000);
}
