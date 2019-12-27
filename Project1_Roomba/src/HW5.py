#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 00:17:18 2019

@author: coldhenry
"""
import cv2
import picar
import numpy as np
from time import sleep, clock
import matplotlib.pyplot as plt
from picar import front_wheels, back_wheels
# self-defined function
from src_motor import Straight, Motor_turn
from src_QRcode import QR_DistanceDetect, QR_Find_Detect, LR_Cali, destroy

motor_speed = 50
real_world_speed = 4.3 # unit[inch]motor speed 50
rotation_speed = 19 # degree/s when turn angle 60 + speed 50
rotation_speed_2 = 23 # degree/s when turn angle 60 + speed 50

#PiCar Setting
bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
picar.setup()
bw.speed = 0
fw.turn(90)

#camera = cv2.VideoCapture(0)

sleep(2)
print(__file__ + " start!!")

def LineSweep(dis0,QRtarget,t_scan,dis1,dis2,Cali_FLAG=False,angle=63):
    Straight(dis0)
    dis, diff_x, QR = QR_DistanceDetect(t_scan,QRtarget)
    if dis==0:
        Straight(-3)
        dis, diff_x, QR = QR_DistanceDetect(t_scan,QRtarget)
    total_time = 0
    while dis<dis1 or dis>(dis1+2):
        print("now dis:",dis)
        t_0 = clock();
        Straight(dis-(dis+1))
        dis, diff_x, QR = QR_Find_Detect(t_scan,QRtarget)
        total_time = total_time + (clock()-t_0)
        if total_time > 10:
            print("***timeout***")
            break
    LR_Cali(dis, diff_x,QRtarget)
    dis, diff_x, QR = QR_Find_Detect(5,QRtarget)
    while dis<dis2 or dis>(dis2+2):
        print("now dis:",dis)
        t_0 = clock();
        Straight(dis-(dis2+1))
        dis, diff_x, QR = QR_Find_Detect(5,QRtarget)
        total_time = total_time + (clock()-t_0)
        if total_time > 10:
            print("***timeout***")
            break
    if Cali_FLAG == True:
        LR_Cali(dis, diff_x,QRtarget)
    diff_deg = 90
    t_turn = abs(diff_deg) / rotation_speed
    Motor_turn('forward',angle,motor_speed,t_turn)
    
    

# 1-1
LineSweep(28,'Landmark 1',5,24,23)
# 1-2
LineSweep(15,'GOAL',5,26,25)
# 1-3
LineSweep(18,'Landmark 1',5,26,26)
# 1-4
LineSweep(7,'Landmark 1',5,41,30,Cali_FLAG=True)
# 2-1
LineSweep(7,'Landmark 3',5,41,30)
# 2-2
LineSweep(10,'Landmark 2',5,36,30)
# 2-3
LineSweep(10,'Landmark 2',5,36,28)
# 2-4
LineSweep(10,'Landmark 2',7,47,40)
# 3-1
LineSweep(0,'Landmark 3',5,42,39)
# 3-2
LineSweep(0,'Landmark 3',5,42,39)
# 3-3
LineSweep(0,'GOAL',5,42,39)
Motor_turn('forward',50,motor_speed,90.0/rotation_speed)

destroy()

"""
Straight(58-30)
dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 1')
if dis==0:
    Straight(-3)
    dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 1')
total_time = 0
while dis<27 or dis>29:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-28)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 1')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'Landmark 1')
dis, diff_x, QR = QR_Find_Detect(5,'Landmark 1')
while dis<26 or dis>27:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-26.5)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 1')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
diff_deg = 90
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',63,motor_speed,t_turn)
#%% 2nd edge
LR_Cali(dis, diff_x,'GOAL')
Straight(58-14-11-5-3-10)
dis, diff_x, QR = QR_DistanceDetect(5,'GOAL')
if dis==0:
    Straight(-5)
    dis, diff_x, QR = QR_DistanceDetect(5,'GOAL')
total_time = 0
while dis<26 or dis>27:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-26.5)
    dis, diff_x, QR = QR_Find_Detect(5,'GOAL')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'GOAL')
dis, diff_x, QR = QR_Find_Detect(5,'GOAL')
while dis<25 or dis>26:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-25.5)
    dis, diff_x, QR = QR_Find_Detect(5,'GOAL')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
diff_deg = 90
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',63,motor_speed,t_turn)
#%% 3rd edge
LR_Cali(dis, diff_x,'Landmark 1')
Straight(58-14-11-5-10)
dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 1')
if dis==0:
    Straight(-5)
    dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 1')
total_time = 0
while dis<26 or dis>27:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-26.5)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 1')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'Landmark 1')
dis, diff_x, QR = QR_Find_Detect(5,'Landmark 1')
while dis<26 or dis>28:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-27)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 1')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
diff_deg = 90
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',65,motor_speed,t_turn)
#%% 4th edge
Straight(58-14-11-5-6-5-10)
dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 1')
if dis==0:
    Straight(-5)
    dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 1')
total_time = 0
while dis<41 or dis>43:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-42)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 1')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'Landmark 1')
dis, diff_x, QR = QR_Find_Detect(5,'Landmark 1')
while dis<33 or dis>35:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-34)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 1')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'Landmark 1')
diff_deg = 90
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',65,motor_speed,t_turn)
#%% 2-1th edge
LR_Cali(dis, diff_x,'Landmark 3')
Straight(58-14-11-5-6-5-10)
dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 3')
if dis==0:
    Straight(-5)
    dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 3')
total_time = 0
while dis<41 or dis>43:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-42)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 3')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'Landmark 3')
dis, diff_x, QR = QR_Find_Detect(5,'Landmark 3')
while dis<33 or dis>35:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-34)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 3')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
diff_deg = 90
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',65,motor_speed,t_turn)
#%% 2-2th edge
LR_Cali(dis, diff_x,'Landmark 3')
Straight(10)
dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 2')
if dis==0:
    Straight(-5)
    dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 2')
total_time = 0
while dis<36 or dis>38:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-37)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 2')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'Landmark 3')
dis, diff_x, QR = QR_Find_Detect(5,'Landmark 2')
while dis<32 or dis>34:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-33)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 2')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
diff_deg = 90
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',65,motor_speed,t_turn)
#%% 2-3th edge
Straight(10)
dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 2')
if dis==0:
    Straight(-5)
    dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 2')
total_time = 0
while dis<36 or dis>38:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-37)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 2')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'Landmark 2')
dis, diff_x, QR = QR_Find_Detect(5,'Landmark 2')
while dis<30 or dis>32:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-31)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 2')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
diff_deg = 90
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',65,motor_speed,t_turn)
#%% 2-4th edge
Straight(0)
dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 2')
if dis==0:
    Straight(-5)
    dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 2')
total_time = 0
while dis<47 or dis>49:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-48)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 2')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'Landmark 2')
dis, diff_x, QR = QR_Find_Detect(5,'Landmark 2')
while dis<40 or dis>42:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-41)
    dis, diff_x, QR = QR_Find_Detect(5,'Landmark 2')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
diff_deg = 90
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',65,motor_speed,t_turn)
#%% 3-1th edge
Straight(0)
dis, diff_x, QR = QR_DistanceDetect(5,'GOAL')
if dis==0:
    Straight(-5)
    dis, diff_x, QR = QR_DistanceDetect(5,'GOAL')
total_time = 0
while dis<42 or dis>44:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-43)
    dis, diff_x, QR = QR_Find_Detect(5,'GOAL')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'GOAL')
dis, diff_x, QR = QR_Find_Detect(5,'GOAL')
while dis<36 or dis>38:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-37)
    dis, diff_x, QR = QR_Find_Detect(7,'GOAL')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
diff_deg = 90
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',65,motor_speed,t_turn)
#%% 3-2th edge
Straight(0)
dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 3')
if dis==0:
    Straight(-5)
    dis, diff_x, QR = QR_DistanceDetect(5,'Landmark 3')
total_time = 0
while dis<42 or dis>44:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-43)
    dis, diff_x, QR = QR_Find_Detect(7,'Landmark 3')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
LR_Cali(dis, diff_x,'Landmark 3')
dis, diff_x, QR = QR_Find_Detect(5,'Landmark 3')
while dis<36 or dis>38:
    print("now dis:",dis)
    t_0 = clock();
    Straight(dis-37)
    dis, diff_x, QR = QR_Find_Detect(7,'Landmark 3')
    total_time = total_time + (clock()-t_0)
    if total_time > 10:
        print("***timeout***")
        break
diff_deg = 90
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',65,motor_speed,t_turn)
#%% 3-4th edge
t_turn = abs(diff_deg) / rotation_speed
Motor_turn('forward',65,motor_speed,t_turn)
"""