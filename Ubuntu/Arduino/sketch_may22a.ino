
#include <ros.h>
#include <std_msgs/Int64.h>
#include <std_msgs/String.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Float64MultiArray.h>

//------5----LIBRARY--------------------------------//
#include <SPI.h>
#include <digitalWriteFast.h>
//------------------PIN--ARDUINO-------------------//
#define FORWARDIN    A1
#define BACKWARDIN   A2
#define SAFTYIN      A3
#define SPEEDIN      A0

#define FORWARDOUT   38
#define BACKWARDOUT  37
#define SAFTYOUT     36

#define CONTROLSPEED  53

//-------------PARAMETER--TIME---------------------//
long previousMillis = 0;
long currentMillis = 0;

int interval = 200;

//------------------PARAMETER--FUNCTION------------------//
int value;
byte address = 0x11;
//----------------PARAMETER-PID--------------------------//

long currenttime = 0;

float Kp = 0.0;

float Ki = 0.0;

float Kd = 0.0;

float derivative = 0;
float prevadjust;
float sigmaerror=0, dT,preverror=0;
float prev=0;
float preave=0;
float adjust1;
//-------------------------------------------------------//

//------------ROS--TOPIC--------------------------//
ros::NodeHandle  nh;

std_msgs::Float64 FORWARD,BACKWARD,PADEL,SPEED_adjust,SPEED_error;

ros::Publisher direc1("direction_F",&FORWARD);
ros::Publisher direc2("direction_B",&BACKWARD);
ros::Publisher direc3("direction_P",&PADEL);

ros::Publisher Speedadjust("Speedadjust",&SPEED_adjust);
ros::Publisher Speederror("Speederror",&SPEED_error);




 
   
  

//-----------ROS---SUBSCRIBER-----------------------//
void messageCb( const std_msgs::Float64MultiArray& msg)
{    
  float Time_oprate = msg.data[0]; 
  float velocity_GNSS = msg.data[1]; // sub data 
  float Speed_direction = msg.data[2];
  
float Kp = 7.9;

float Ki = 1.6;

float Kd = 3.8;
     
  SpeedControl(velocity_GNSS,Speed_direction ,Time_oprate,Kp,Ki,Kd);
    
    
  

  
}     

 ros::Subscriber<std_msgs::Float64MultiArray> subspeed("Velocity", &messageCb);

void setup()
{
  
//----CREATE--ROS--TOPIC---------------//  
  nh.initNode();
  nh.advertise(direc1);       //ROS  PUBLISH
  nh.advertise(direc2);       //ROS  PUBLISH
  nh.advertise(direc3);       //ROS  PUBLISH
  
  nh.advertise(Speedadjust);    //ROS  PUBLISH
  nh.advertise(Speederror);    //ROS  PUBLISH
  
  nh.subscribe(subspeed);          //ROS  SUBSCRIBER

//------------PINMODE------------------//
pinMode (FORWARDIN, INPUT);
pinMode (BACKWARDIN, INPUT);
pinMode (SAFTYIN, INPUT);

pinMode (FORWARDOUT, OUTPUT);
pinMode (BACKWARDOUT, OUTPUT);
pinMode (SAFTYOUT, OUTPUT); 

pinMode (53,OUTPUT);


SPI.begin();
Serial.begin(57600);


}
void loop()
{
 
//-----------publish--direction--forward --backward--padel------------ //

        float state1 = analogRead(FORWARDIN);
        float state2 = analogRead(BACKWARDIN);
        float state3 = analogRead(SAFTYIN);
        float state4 = analogRead(SPEEDIN);
          FORWARD.data = state1;
            direc1.publish(&FORWARD);
          BACKWARD.data = state2;
            direc2.publish(&BACKWARD);
          PADEL.data = state3;
            direc3.publish(&PADEL);
          nh.spinOnce();
          delay(1000);
//-------------------------------------------------------------------//
    
      float adjust = adjust1;
      
     
     
      runSpeed( state1, state2, state3, adjust ); //call runspeed function close loop
    
}
void runSpeed (float state1,float state2,float state3,float value)
{  

  if ((state1 > 1000) & (state2 < 1000))                  //Forward
    {
      Serial.print(" || Forward...");
      digitalWrite(FORWARDOUT,HIGH);
      digitalWrite(BACKWARDOUT,LOW);
      digitalPotWrite(value);

    }

  if ((state1 < 1000) & (state2 > 1000))                  //Backwad
    {
      Serial.print(" || Backward...");
      digitalWrite(FORWARDOUT,LOW);
      digitalWrite(BACKWARDOUT,HIGH);
      digitalPotWrite(value);

    }

  if ((state1 < 1000) & (state2 < 1000))                  //None
    { 
      value = 0;
      Serial.print(" || None...");
      digitalWrite(FORWARDOUT,LOW);
      digitalWrite(BACKWARDOUT,LOW);
      digitalPotWrite(value);

    }

  if ((state1 > 1000) & (state2 > 1000))                  //ERROR
    { 
      value = 0;
      Serial.print(" || ERROR...");
      digitalWrite(FORWARDOUT,LOW);
      digitalWrite(BACKWARDOUT,LOW);
      digitalPotWrite(value);

    }
}


float SpeedControl(float velocity_GNSS,float set,float Time_oprate,float Kp,float Ki,float Kd)
{
    float time_now = Time_oprate;
    dT = time_now - prev;
    prev = time_now;
    float error = set-velocity_GNSS ;  
    if (set == 1.0)
    {
      sigmaerror = sigmaerror + (error*dT);
      float adjust1km = (error*Kp)+(Ki*sigmaerror)+(Kd*((error-preverror)/dT)) ;
      adjust1 = adjust1km;
      
      if (adjust1 > 213)
      {
        adjust1 = 213;
      }
    }
    
    if (set == 3.0)
    {
      sigmaerror = sigmaerror + (error*dT);
      float adjust3km = (error*Kp)+(Ki*sigmaerror)+(Kd*((error-preverror)/dT)) ;
      adjust1 = adjust3km;
      
      if (adjust1 > 230)
      {
        adjust1 = 230;
      }
    }
     

   SPEED_error.data =  error;  // and pud
   Speederror.publish(&SPEED_error);
   
   SPEED_adjust.data =  adjust1; // and pud
   Speedadjust.publish(&SPEED_adjust);    
    
     preverror = error;
     prevadjust = adjust1;
     return adjust1; 
        
}
int digitalPotWrite(float value)  
{
  Serial.print(" || Value = ");
  Serial.println(value);
  digitalWrite(53, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(53, HIGH);
}
