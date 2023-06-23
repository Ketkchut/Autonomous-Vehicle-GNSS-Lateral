
#include <stdint.h>
#include <stdlib.h>
#include <SPI.h>
#include <digitalWriteFast.h>
#define FORWARDIN A3
#define BACKWARDIN A5
#define SAFTY_IN A4
#define FORWARDOUT 38
#define BACKWARDOUT 37
#define SAFTY_OUT 36
#define SPEED_IN A0
#define ENC_IN 2
#define ENC_IN2 3
#define ENC_COUNT_REV 52
#define CSPIN 53 //Output of Digital poten
#define Volt A7
float val;
int speedIN,val2=0;

byte address = 0x11;
volatile long encoderValue ,encoderValue2 ;
long previousMillis = 0;
long previousMillis2 = 0;
long currentMillis = 0;
long currentMillis2 = 0;
int interval = 200,i=0;
int interval2 = 100;
float rpm ;
float vall[11];
int count=0;
float KmperHr ;
float DperR = 1.41/1000;
float Km = 0,KM2=0;
float value;
int n =0 ;
//int x =1023;
float currentSpeed, result;
float average=0;
float adjust;

void setup() 
{
  pinMode(FORWARDIN, INPUT);
  pinMode(BACKWARDIN, INPUT);
  pinMode (SAFTY_IN, INPUT);
  pinMode(FORWARDOUT, OUTPUT);
  pinMode(BACKWARDOUT, OUTPUT);
  pinMode (SAFTY_OUT, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode (CSPIN, OUTPUT);
  SPI.begin();
  Serial.begin(57600);
//  attachInterrupt(digitalPinToInterrupt(ENC_IN), upateEncoder, RISING);  // รูปแบบคำสั่ง attachInterrupt(interrupt, ISR, mode)
 // attachInterrupt(digitalPinToInterrupt(ENC_IN2), updateEncoder2, RISING);  
}

void loop() {
  currentMillis = millis();
  if (currentMillis - previousMillis > interval) 
  { 
    previousMillis = currentMillis;
    float state1 = analogRead(FORWARDIN);
    float state2 = analogRead(BACKWARDIN);
    float state3 = analogRead(SAFTY_IN);
    float state4  = analogRead(SPEED_IN);
    /*Serial.print("state1=");
    Serial.println(state1);
    Serial.print("state3=");
    Serial.println(state3);
    Serial.print("state4=");
    Serial.println(state4);*/
    if (state1>1000)
    {
      if (state3>1000)
      {
          value = 10;
        
          rpm = (float)(encoderValue * 60 / ENC_COUNT_REV);
          KmperHr = (float)(((rpm*60)*DperR)*5);
          Km = (float(encoderValue2)/ENC_COUNT_REV*1.41);
          currentSpeed = averagefilter(KmperHr);

          Serial.print("speed =");
          Serial.println(KmperHr);

          runSpeed(state1,state2,state3,adjust);
          
      }
      else
      {
        Serial.println("n=1");
      }      
    }
     else
      {
        Serial.println("nm=1");
      }
  }
}

void updateEncoder()
{
  // Increment value for each pulse from encoder
  encoderValue++;
}
void updateEncoder2()
{
  // Increment value for each pulse from encoder
  encoderValue2++;
}
int digitalPotWrite(float value)  // ปรับค่า PWM
{
  digitalWrite(CSPIN, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(CSPIN, HIGH);

}
void runSpeed (float state1,float state2,float state3,float value)
{
    if(state3 > 1000) 
  {
       digitalWrite(36, HIGH);
       digitalWrite(38,HIGH);
       digitalPotWrite(value);
       
  }
    if(state3<1000)
  {
        digitalWrite(36, LOW);
        digitalWrite(38,LOW);
        digitalPotWrite(0);
  }
}
float averagefilter(float rpm)
{ 
  float sum = 0;
  if(count == 11)
  {
    count = 0;
  }
  else
  {  vall[count] = rpm;
  }
  for(int i = 0; i<11;i++)
  {
    sum += vall[i];
  }    
  result = sum/10;
  count++;
  return result;
  
}


    
    
       
       
 
