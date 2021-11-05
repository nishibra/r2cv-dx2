#!/usr/bin/env python
#
# 2021.10.25 key_commander
# by T.Nishimura @AiRRC
#----------------------------------------
# usage
# $ ros2 run r2dx2w dx2w_key        ## terminal1
# $ ros2 topic echo /car_command    ## terminal2
# $ ros2 topic echo /cmd_vel        ## terminal3
#
import time
import sys, termios, atexit
from select import select
# ROS2
import rclpy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import QoSDurabilityPolicy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
#
cmd="Non"
mode_cont=0
x_lin=0.0
y_lin=0.0
z_lin=0.0
x_ang=0.0
y_ang=0.0
z_ang=0.0
#
# terminal settings -----------
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)
# new terminal
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)
# switch to normal
def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
# switch to new
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)
def putch(ch):
    sys.stdout.write(ch)
def getch():
    return sys.stdin.read(1)
def getche():
    ch = getch()
    putch(ch)
    return ch
def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr != []
#--------------------------------
def key_hit():
  global x_lin,y_lin,z_lin,x_ang,y_ang,z_ang
  global cmd,mode_cont
#
  msg = String()
  msg.data="Non"
#
  if kbhit():
    k = getch()
    print(k)
    if k=="d":
      msg.data="drive"
      cmd=msg.data
      mode_cont=1
    elif k=="a":
      msg.data="camc"
      cmd=msg.data
      mode_cont=1      
    elif k=="r":
      msg.data="rt90"
      mode_cont=0    
    elif k=="f":
      msg.data="fw100"
      mode_cont=0
    elif k=="l":
      msg.data="lt90"
      mode_cont=0
    elif k=="b":
      msg.data="bk100"
      cmd=msg.data
      mode_cont=0
    elif k=="u":
      msg.data="ut180"
      mode_cont=0
    elif k=="s":
      msg.data="stop"
      mode_cont=0
    elif k=="N":
      msg.data="Ton"
      mode_cont=0
    elif k=="g":
      msg.data="gangle"
      mode_cont=0
    elif k=="n":
      msg.data="Toff"
      mode_cont=0 
    elif k=="v":
      msg.data="volt"
      mode_cont=0
    elif k=="q":
      msg.data="quit"
      mode_cont=0      
#      
    elif k=="U":
      x_lin=x_lin+0.1
    elif k=="J":
      x_lin=0.0
      y_lin=0.0
    elif k=="M":
      x_lin=x_lin-0.1     
    elif k=="H":
      y_lin=y_lin-0.1    
    elif k=="K":
      y_lin=y_lin+0.1
#         
    elif k=="E":
      x_ang=x_ang+0.01
    elif k=="D":
      x_ang=0.0
      y_ang=0.0
      z_ang=0.0
    elif k=="C":
      x_ang=x_ang-0.01   
    elif k=="S":
      y_ang=y_ang-0.01    
    elif k=="F":
      y_ang=y_ang+0.01        
    elif k=="V":
      z_ang=z_ang-0.01    
    elif k=="R":
      z_ang=z_ang+0.01        
#
    if mode_cont==1:
      msg.data=cmd
      pub2.publish(msg)
      twist = Twist()
      twist.linear.x = x_lin
      twist.linear.y = y_lin
      twist.linear.z = z_lin
      twist.angular.x =x_ang
      twist.angular.y =y_ang
      twist.angular.z =z_ang
      pub1.publish(twist)
    else:
      pub2.publish(msg)
#
    return (k)
#--------------------------------
qos = QoSProfile(
    depth=1, 
    reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE,
    durability=QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL)
rclpy.init()
node = Node("key_comm")
pub1 = node.create_publisher(Twist, "/cmd_vel",qos)
pub2 = node.create_publisher(String, "/car_command",qos)
#  
def main():
  print ("Start Key commander")
  atexit.register(set_normal_term)
  set_curses_term()
  kk=' '
  while kk !='q':
    kk=key_hit()
    time.sleep(0.05)
  print (kk,'++++++++++++++++++++++++++++++++++++++')  
  set_normal_term()
  node.destroy_node()
  rclpy.shutdown()
#--------------------------------
if __name__ == "__main__":
    main()
#--------------------------------
