#!/usr/bin/env python3
import rospy
import numpy as np
import time
from collections import deque
from tf.transformations import quaternion_from_euler,euler_from_quaternion
from nav_msgs.msg import Path,Odometry
from ackermann_msgs.msg import AckermannDrive
pid_velocity=[1,0.3,0.3]
pid_steering=[1,0,0]
L = 1.5  # [m] Wheel base of vehicle
target_speed = 0.5
max_steer = np.radians(20.0)  # [rad] max steering angle
#e_buffer = deque(maxlen=20)
e_buffer = []
_current_time = time.time
last_time = None
cx =None
cy =None
class State(object):
    def __init__(self, x=0.0, y=0.0, yaw=0.0, v=0.0):
        super(State, self).__init__()
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v
        self.x1 = x
        self.y1 = y
        self.yaw1 = yaw
        self.v1 = v

    def update(self, acceleration, delta):
        delta = np.clip(delta, -max_steer, max_steer)
        self.x1 += self.v1 * np.cos(self.yaw1) * dt
        self.y1 += self.v1 * np.sin(self.yaw1) * dt
        self.yaw1 += self.v1 / L * np.tan(delta) * dt
        self.yaw1 = normalize_angle(self.yaw1)
        self.v1 = acceleration

def callbackOdomwheel(msg):
    state.v=msg.twist.twist.linear.x

def callbackOdom(msg):
    global state
    global cx,cy,cyaw
    global pub
    
    sent=AckermannDrive()

    orientation=msg.pose.pose.orientation
    _,_,yaw = euler_from_quaternion([orientation.x,orientation.y,orientation.z,orientation.w])
    state.x = msg.pose.pose.position.x
    state.y = msg.pose.pose.position.y
    state.yaw = yaw
    if(cx  != None and cy != None):
        target_idx, _ = calc_target_index(state, cx, cy)
        ai = pid_control(target_speed, state.v)
        di, target_idx = pid_steering_control(state, cx, cy, cyaw, target_idx)
        delta = np.clip(np.degrees(di), -20,20)
        sent.steering_angle=-delta
        sent.speed=ai
        print(delta,ai)
        pub.publish(sent)

def pid_control(target, current):
    return pid_velocity[0] * (target - current)

def calc_target_index(state, cx, cy):
    fx = state.x + L * np.cos(state.yaw)
    fy = state.y + L * np.sin(state.yaw)
    dx = [fx - icx for icx in cx]
    dy = [fy - icy for icy in cy]
    d = np.hypot(dx, dy)
    target_idx = np.argmin(d)
    # Project RMS error onto front axle vector
    front_axle_vec = [-np.cos(state.yaw + np.pi / 2),
                      -np.sin(state.yaw + np.pi / 2)]
    error_front_axle = np.dot([dx[target_idx], dy[target_idx]], front_axle_vec)

    return target_idx, error_front_axle

def pid_steering_control(state, cx, cy, cyaw, last_target_idx):
    global last_time
    current_target_idx, error_front_axle = calc_target_index(state, cx, cy)
    if last_target_idx >= current_target_idx:
        current_target_idx = last_target_idx
    now = _current_time()
    if(last_time is None):
        last_time = now
    dt = now - last_time 
    e_buffer.append(error_front_axle)
    if len(e_buffer) >= 2:
        _de = (e_buffer[-1] - e_buffer[-2]) / dt
        _ie = sum(e_buffer) * dt
    else:
        _de = 0.0
        _ie = 0.0
    if(dt>0):
        throttle = (pid_steering[0] * error_front_axle) + (pid_steering[1] * _de / dt) + (pid_steering[2] * _ie * dt)
    else:
        throttle = 0
    last_time = now
    return throttle, current_target_idx

def Tracking(msg):
    global cx,cy,cyaw
    cx = []
    cy = []
    cyaw = []
    for x in msg.poses:
        cx.append(x.pose.position.x)
        cy.append(x.pose.position.y)
        _,_,yaw = euler_from_quaternion([x.pose.orientation.x,x.pose.orientation.y,x.pose.orientation.z,x.pose.orientation.w])
        cyaw.append(yaw)

   
def normalize_angle(angle):
    while angle > np.pi:
        angle -= 2.0 * np.pi

    while angle < -np.pi:
        angle += 2.0 * np.pi

    return angle
    
def Run():
    global state
    global pub
    rospy.init_node('navigation', anonymous=True)
    state = State(x=0.4170038061195659, y=-0.2844199331185601, yaw=np.radians(0.0), v=0.0)
    sub = rospy.Subscriber("/path", Path, Tracking)
    sub2 = rospy.Subscriber("/odometry/filtered_map",Odometry,callbackOdom)
    subwheel = rospy.Subscriber("/wheel/odom",Odometry,callbackOdomwheel)
    pub = rospy.Publisher('/track/cmd_vel',AckermannDrive, queue_size=1)
    odom = Odometry()
    rospy.spin()

if __name__ == '__main__':
  Run()