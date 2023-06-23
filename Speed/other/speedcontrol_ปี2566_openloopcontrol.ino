#include <stdint.h>
#include <stdlib.h>
#include <digitalWriteFast.h>  //For Write PWM
#include <SPI.h>               //For Transfer value PWM

//Define Pinmode
#define FORWARDIN A1           //Input from F Switch
#define BACKWARDIN A2          //Input form R Switch
#define SAFTYIN A3            //Input from Trigger Switch Before Wheel Rot
#define FORWARDOUT 38          //Step-up to Car Controller
#define BACKWARDOUT 37         //Step-up to Car Controller 
#define SAFTYOUT 36           //Step-up to Car Controller
#define SPEEDIN A0            //Input from Padel when press
#define ENC_IN 2               //Input Intrr form ENC
#define ENC_IN2 3
#define ENC_COUNT_REV 52        
#define CSPIN    53            //Output of Digital poten



//Define Parameter
long previousMillis = 0;          //For delay
long currentMillis = 0;           //For delay
int interval = 100;             //For delay
float state1 = 0;                 //Value from ang F Switch A3 (Digital 0,1023)
float state2 = 0;                 //Value from ang R Switch A5 (Digital 0,1023)
float state3 = 0;                 //Value from ang Trigger Switch A4 (Digital 0,1023)
float state4 = 0;                 //Value from ang Padel when press (Analog 0-1023)
float value = 0;                  //Speed Setpoint (0-255)
float rpm = 0;                    //Speed Round per min of motor
float KmperHr = 0;                //Speed of car
float currentSpeed = 0;           //Speed of car after filter
float DperR = 1.31/1000;          //Dimeter of wheel
volatile long encoderValue =0;   //ENC Value when Intrr for Func1
volatile long encoderValue2 = 0;  ////ENC Value when Intrr for Func2
float Km = 0;                     //Distance when car moving
byte address = 0x11;              //Address of Digital poten (From Example)

void setup() {
  // put your setup code here, to run once:
  pinMode(FORWARDIN, INPUT);
  pinMode(BACKWARDIN, INPUT);
  pinMode (SAFTYIN, INPUT);

  pinMode(FORWARDOUT, OUTPUT);
  pinMode(BACKWARDOUT, OUTPUT);
  pinMode (SAFTYOUT, OUTPUT);
  
 
 
  pinMode (53, OUTPUT);
  SPI.begin();
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(ENC_IN), updateEncoder, RISING );
  attachInterrupt(digitalPinToInterrupt(ENC_IN2), updateEncoder2, RISING  );

}
void updateEncoder()
{
 encoderValue++;
}
void updateEncoder2()
{
  encoderValue2++;

}
void loop() {
  
currentMillis = millis();
  if (currentMillis - previousMillis > interval) 
  { 
    previousMillis = currentMillis;

    float state1 = analogRead(FORWARDIN);
    float state2 = analogRead(BACKWARDIN);
    float state3 = analogRead(SAFTYIN);
    float state4 = analogRead(SPEEDIN);           

    Serial.print("State1 = ");
    Serial.print(state1);
    Serial.print(" || State2 = ");
    Serial.print(state2);
    Serial.print(" || State3 = ");
    Serial.print(state3);
  
    value = 20;                                        // Change Value here
    runSpeed(state1,state2,state3,value); 

  } 
}

void runSpeed (float state1,float state2,float state3,float value)
{  

  if ((state1 > 1000) & (state2 < 1000))                  //Forward
  {
    Serial.print(" || Forward...");
    digitalWrite(FORWARDOUT,HIGH);
    digitalWrite(BACKWARDOUT,LOW);
    digitalPotWrite(value);

    // if (state3 > 1000)
    // {
    //   Serial.println(" || Press Padel...");
    //   digitalWrite(SAFTYOUT,HIGH);
    // }
    // if (state3 < 1000)
    // {
    //   Serial.println(" || Dont Press Padel...");
    //   digitalWrite(SAFTYOUT,LOW); 
    // }

  }

  if ((state1 < 1000) & (state2 > 1000))                  //Backwad
  {
    Serial.print(" || Backward...");
    digitalWrite(FORWARDOUT,LOW);
    digitalWrite(BACKWARDOUT,HIGH);
    digitalPotWrite(value);

    // if (state3 > 1000)
    // {
    //   Serial.println(" || Press Padel...");
    //   digitalWrite(SAFTYOUT,HIGH);
    // }
    // if (state3 < 1000)
    // {
    //   Serial.println(" || Dont Press Padel...");
    //   digitalWrite(SAFTYOUT,LOW);       
    // }

  }

  if ((state1 < 1000) & (state2 < 1000))                  //None
  { 
    value = 0;
    Serial.print(" || None...");
    digitalWrite(FORWARDOUT,LOW);
    digitalWrite(BACKWARDOUT,LOW);
    digitalPotWrite(value);

    // if (state3 > 1000)
    // {
    //   Serial.println(" || Press Padel...");
    //   digitalWrite(SAFTYOUT,HIGH);
    // }
    // if (state3 < 1000)
    // {
    //   Serial.println(" || Dont Press Padel...");
    //   digitalWrite(SAFTYOUT,LOW);       
    // }
    
  }

  if ((state1 > 1000) & (state2 > 1000))                  //ERROR
  { 
    value = 0;
    Serial.print(" || ERROR...");
    digitalWrite(FORWARDOUT,LOW);
    digitalWrite(BACKWARDOUT,LOW);
    digitalPotWrite(value);

    // if (state3 > 1000)
    // {
    //   Serial.println(" || Press Padel...");
    //   digitalWrite(SAFTYOUT,HIGH);
    // }
    // if (state3 < 1000)
    // {
    //   Serial.println(" || Dont Press Padel...");
    //   digitalWrite(SAFTYOUT,LOW);       
    // }
    
  }


}

int digitalPotWrite(float value)  // ปรับค่า PWM
{
  Serial.print(" || Value = ");
  Serial.println(value);
  digitalWrite(53, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(53, HIGH);
}








