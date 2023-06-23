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
#define CSPIN 53
#define Volt A7

#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Int32.h>
#include <sensor_msgs/Joy.h>
#include <stdint.h>
#include <stdlib.h>
#include <SPI.h>
#include <digitalWriteFast.h>

ros::NodeHandle nh;
float val;
int speedIN,val2=0;

byte address = 0x11;
volatile long encoderValue = 0,encoderValue2 = 0;
long previousMillis = 0;
long previousMillis2 = 0;
long currentMillis = 0;
long currentMillis2 = 0;
float currentSpeed, result;
float setSpeedd= 5.0;
int interval = 200,i=0;
int interval2 = 100;
int rpm = 0;
float vall[11];
int count=0;
float Kprop =6.3,adjust,prevadjust,Kintegral = 0.0047,Kderiv =4;
float sigmaerror=0, dT,preverror,prev=0;
float preave=0;
float average=0;
float KmperHr = 0;
float DperR = 1.41/1000;
float Km = 0,KM2=0;
float adjust1;
int mode = 1;
bool stateC;
void setup() {
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
  attachInterrupt(digitalPinToInterrupt(ENC_IN), updateEncoder, RISING);
  attachInterrupt(digitalPinToInterrupt(ENC_IN2), updateEncoder2, RISING);

}

void loop() {
 
    
  currentMillis = millis();
  if (currentMillis - previousMillis> interval) {
    previousMillis = currentMillis;
    
  float state1 = analogRead(FORWARDIN);
  float state2 = analogRead(BACKWARDIN);
  float state3 = analogRead(SAFTY_IN);
  float state4  = analogRead(SPEED_IN);
    
    // Calculate RPM
    rpm = (float)(encoderValue * 60 / ENC_COUNT_REV);
 
    // Calculate Km/hr
    KmperHr = (float)(((rpm*60)*DperR)*5);
    
    Km = (float(encoderValue2)/ENC_COUNT_REV*1.41);
    
    currentSpeed = averagefilter(KmperHr);
    //currentSpeed = KmperHr;
    adjust = SpeedControl(currentSpeed,setSpeedd,currentMillis,state3);
    //Serial.print(" KmperHr : " );
   // Serial.println(currentSpeed);
   // Serial.print(" currentSpeed : " );
   // Serial.print(currentSpeed);

    if(adjust>180)
    {
      adjust = 180;
    }
    
    runSpeed(state1,state2,state3,adjust);
    Serial.println(adjust);
     encoderValue = 0;
     average = 0;
  }
 }


float SpeedControl(float current,float set,float currentTime,float state)
{
    float error = set-current ;
    dT = currentTime - prev;
    prev = currentTime;
    if(state > 1000)
    {
      sigmaerror = sigmaerror+ (error*dT);
       
     adjust1 = (error*Kprop)+(Kintegral*sigmaerror)+(Kderiv*((error-preverror)/dT)) ;
     if(error < 0.1 && error > -0.1)
     {
        adjust1 = prevadjust;
     }
    }
    else
    {
      sigmaerror = 0;
      adjust1 = 0;
      
    }
    /*Serial.print(" sigmaerror : " );
    Serial.print(sigmaerror);
    Serial.print(" dT : " );
    Serial.print(dT);
    Serial.print(" adjust1 : " );
    Serial.print(adjust1);
    Serial.print(" error : " );
    Serial.println(error);*/
    preverror = error;
    prevadjust = adjust1;
    return adjust1; 
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
int digitalPotWrite(float value)
{
  digitalWrite(CSPIN, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(CSPIN, HIGH);

}
float mapf(float val, float in_min, float in_max, float out_min, float out_max) {
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
void runSpeed(float state1,float state2,float state3,float val)
{
      if(state3 > 1000)
  {
       digitalWrite(36, HIGH);
       digitalPotWrite(val);
       
  }
  else
  {
    digitalWrite(36, LOW);
    digitalPotWrite(0);
  }
  if(state1 > 1000)
  {
     digitalWrite(38, HIGH);
  }
  else
  {
    digitalWrite(38, LOW);
  }
    if(state2 > 1000)
  {
     digitalWrite(37, HIGH);
  }
  else
  {
    digitalWrite(37, LOW);
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
