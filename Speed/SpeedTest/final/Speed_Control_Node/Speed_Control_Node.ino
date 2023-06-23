

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
   float Kmperhr = velocity_GNSS;
   
   SPEED_GNSS.data = velocity_GNSS;  // and pub
   SpeedGNSS.publish(&SPEED_GNSS);   
}
 ros::Subscriber<std_msgs::Float64> sub("Velocity_test", &messageCb );
   

//----------LIBRARY--------------------------------//
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
int interval = 100;
//------------------PARAMETER--FUNCTION------------------//
int value;
byte address = 0x11;



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
  currentMillis = millis();
    if(currentMillis - previousMillis> interval)
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
        value = 20;
        
        runSpeed(state1,state2,state3,value); //call runspeed function
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



int digitalPotWrite(float value)  
{
  Serial.print(" || Value = ");
  Serial.println(value);
  digitalWrite(53, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(53, HIGH);
}
