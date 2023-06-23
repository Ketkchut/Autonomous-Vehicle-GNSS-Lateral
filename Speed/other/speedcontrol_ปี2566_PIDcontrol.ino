

#include <ros.h>
#include <std_msgs/Int64.h>
#include <std_msgs/String.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Float64MultiArray.h>


//------------ROS--TOPIC--------------------------//
ros::NodeHandle  nh;

std_msgs::Float64 FORWARD,BACKWARD,PADEL,SPEED,SPEED_GNSS;
ros::Publisher direc1("direction_F",&FORWARD);
ros::Publisher direc2("direction_B",&BACKWARD);
ros::Publisher direc3("direction_P",&PADEL);
ros::Publisher SpeedGNSS("SpeedGNSS",&SPEED_GNSS);

//-----------ROS---SUBSCRIBER-----------------------//
void messageCb( const std_msgs::Float64& msg)
{
   float  velocity_GNSS = msg.data; // sub data
   SPEED_GNSS.data = velocity_GNSS;  // and pub
   SpeedGNSS.publish(&SPEED_GNSS);   
}
 ros::Subscriber<std_msgs::Float64> sub("Velocity", &messageCb );
   

//----------LIBRARY--------------------------------//
#include <SPI.h>
#include <digitalWriteFast.h>
//------------------PIN--ARDUINO-------------------//
#define FORWARD_IN    A3
#define BACKWARD_IN   A5
#define SAFTY_IN      A4
#define SPEED_IN      A0

#define FORWARD_OUT   38
#define BACKWARD_OUT  37
#define SAFTY_OUT     36

#define CONTROLSPEED  53
#define ENC_IN        2
#define ENC_IN2       3
#define ENC_COUNT_REV 52
//-------------PARAMETER--TIME---------------------//
long previousMillis = 0;
long currentMillis = 0;
int interval = 100;
//------------------PARAMETER--FUNCTION------------------//
int value;
byte address = 0x11;
volatile long encoderValue = 0,encoderValue2 = 0;
float KmperHr = 0;
float DperR = 1.41/1000;
float Km = 0;
int rpm = 0;

//-------------------------------------------------------//
void setup()
{
  
//----CREATE--ROS--TOPIC---------------//  
  nh.initNode();
  nh.advertise(direc1);       //ROS  PUBLISH
  nh.advertise(direc2);       //ROS  PUBLISH
  nh.advertise(direc3);       //ROS  PUBLISH
  nh.advertise(SpeedGNSS);    //ROS  PUBLISH
  nh.subscribe(sub);          //ROS  SUBSCRIBER
  
//------------PINMODE------------------//
pinMode (FORWARD_IN, INPUT);
pinMode (BACKWARD_IN, INPUT);
pinMode (SAFTY_IN, INPUT);

pinMode (FORWARD_OUT, OUTPUT);
pinMode (BACKWARD_OUT, OUTPUT);
pinMode (SAFTY_OUT, OUTPUT); 

pinMode (53,OUTPUT);

attachInterrupt(digitalPinToInterrupt(ENC_IN),updateEncoder,RISING);  
attachInterrupt(digitalPinToInterrupt(ENC_IN2),updateEncoder2,RISING);

SPI.begin();
Serial.begin(57600);


}

void loop()
{
  currentMillis = millis();
    if(currentMillis - previousMillis> interval)
    {
       previousMillis = currentMillis; 
       
        float state1 = analogRead(FORWARD_IN);
        float state2 = analogRead(BACKWARD_IN);
        float state3 = analogRead(SAFTY_IN);
        float state4 = analogRead(SPEED_IN);
        
//-----------publish--direction--forward --backward--padel------------ //

          FORWARD.data = state1;
            direc1.publish(&FORWARD);
          BACKWARD.data = state2;
            direc2.publish(&BACKWARD);
          PADEL.data = state3;
            direc3.publish(&PADEL);
          nh.spinOnce();
          delay(1000);
//-------------------------------------------------------------------//
        runSpeed(state1,state2,state3,value); //call runspeed function
    }
}
//void messageCb (const std_msgs::Empty& msg)
//{
//  float KmpreHrGNSS = msg.data;
//}

void runSpeed(float state1,float state2,float state3,float value)
{
  if(state1 > 1000)
    {
      digitalWrite(FORWARD_OUT, HIGH);
      value = 255;
      digitalPotWrite(value);
    }
  else
    {
      digitalWrite(FORWARD_OUT, LOW);
    }
   if(state2 > 1000)
    {
      digitalWrite(BACKWARD_OUT, HIGH);
      value = 255;
      digitalPotWrite(value);
    }
  else
    {
      digitalWrite(BACKWARD_OUT, LOW);
    }
}

void updateEncoder()
{
  encoderValue++;
}

void updateEncoder2()
{
  encoderValue2++;
}

int digitalPotWrite(float value)
{
  digitalWrite(CONTROLSPEED, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(CONTROLSPEED, HIGH);

}