#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# dx2w.py
# 2021.10.20
# by T.Nishimura @AiRRC
#
import sys, time
from r2dx2w.dx2lib import *      # dx2libをインポート
#from dx2lib import *  
#
COMPort = b'/dev/ttyAMA2'        # 任意のCOMポート名に修正の事
Baudrate = 1000000               # Dynamixelのボーレートと合わせる事
AXISNUMW = 2                     # Wheel軸数
AXISNUMA = 2                     # Arm軸数

#
def get_voltage():
  pvoltage= c_uint16()
  if DX2_ReadWordData(dev,1,144,pvoltage,None):
    vol=float(pvoltage.value*0.1)
    print('Voltage=',vol,'V')
#
def get_ArmAngles():
  pangles = (c_double * AXISNUMA)()
  print('angle='),
  if DXL_GetPresentAngles(dev, IDa, pangles, AXISNUMA):
    print((' {:7.1f},'*len(pangles)).format(*pangles)),
#
#----servo motor for mobile --------------------------
def drive_servo(a,b):
  print ("drive",a,b)
  DXL_SetGoalVelocity(dev, 1,-a)
  DXL_SetGoalVelocity(dev, 2,b)
#
def for_ward(speed):
  DXL_SetGoalVelocity(dev, 1,-speed)
  DXL_SetGoalVelocity(dev, 2,speed)
#
def back_ward(speed):
  DXL_SetGoalVelocity(dev, 1,speed)
  DXL_SetGoalVelocity(dev, 2,-speed)
# 
def stop():
  print ("stop")  
  DXL_SetGoalVelocity(dev, 1,0)
  DXL_SetGoalVelocity(dev, 2,0) 
#
def right(speed):
  DXL_SetGoalVelocity(dev, 1,speed)
  DXL_SetGoalVelocity(dev, 2,speed)
#  
def left(speed):
  DXL_SetGoalVelocity(dev, 1,-speed)
  DXL_SetGoalVelocity(dev, 2,-speed)
#
def torque_off():
  print ("torque_off")
  DXL_SetTorqueEnablesEquival(dev, IDa, AXISNUMA, False) 
#  
def torque_on():
  print ("torque_on")
  DXL_SetTorqueEnablesEquival(dev, IDa, AXISNUMA, True)
#
#----arm control--------------
def set_pos(ang1,ang2,tim):  
  DXL_SetGoalAnglesAndTime(dev, (c_uint8 * 2)(3,4), (c_double * 2)(ang1,ang2), 2, tim)
# 
#--main setup -----------------------
dev = DX2_OpenPort(COMPort, Baudrate)
pspeed = c_double()
IDs = (c_uint8 * AXISNUMW)(1,2)
IDa = (c_uint8 * AXISNUMA)(3,4)
def main():
  speed=200
#
  print('check servo')
  if dev != None:
    DX2_SetTimeOutOffset(dev, 50)
    for id in IDs:
      print(id, DXL_GetModelInfo(dev,id).contents.name)
      DXL_SetTorqueEnable(dev, id, False)
      DXL_SetOperatingMode(dev, id, 1)
      DXL_SetTorqueEnable(dev, id, True)
      DXL_SetGoalVelocity(dev, id,0)
    time.sleep(0.1)
    for id in IDa:
      print(id, DXL_GetModelInfo(dev,id).contents.name)
      DXL_SetTorqueEnable(dev, id, False)
      DXL_SetOperatingMode(dev, id, 4)
      DXL_SetTorqueEnable(dev, id, True)
    #get encorder position  
    DXL_GetPresentAngle(dev, 1, pspeed)
    lo_encoder=pspeed.value
    DXL_GetPresentAngle(dev, 2, pspeed)
    ro_encoder=pspeed.value
    print('initial=',lo_encoder,ro_encoder)
#    print('start')
    get_voltage()
    get_ArmAngles()
    print('center')
    set_pos(0,0,1)
    time.sleep(2)
    print('right')
    set_pos(90,30,1)
    time.sleep(2)
    print('left')
    set_pos(-90,-30,1)
    time.sleep(2)
    print('center')
    set_pos(0,0,1)
    time.sleep(1)  
    for_ward(speed)
    time.sleep(1)
    back_ward(speed) 
    time.sleep(1)
    right(speed)
    time.sleep(1)  
    left(speed)
    time.sleep(1)
    stop()
    time.sleep(1)
    print('off')
    #トルクイネーブルディスエーブル
    DXL_SetTorqueEnablesEquival(dev, IDa, AXISNUMA, False)
    DXL_SetTorqueEnable(dev, 1, False)
    DXL_SetTorqueEnable(dev, 2, False)
    #ポートを閉じる(必須)
    DX2_ClosePort(dev)    
  else:
    print('Could not open COM port.')
#-------------------------------  
if __name__ == "__main__":
    main()  
#-------------------------------

