#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 23:21:50 2019

@author: coldhenry
"""
from picar import front_wheels, back_wheels
from time import sleep, clock
import cv2
import math
import numpy as np
import getch
# self design packages
from QRcode import distance_to_camera, QR_DistanceDetect, QR_Find_Detect, LR_Cali, destroy
from Motor import Motor_turn, Straight, PiCar_Init

#%% Parameters

width_img = 640
height_img = 480
KNOWN_DISTANCE = 50*0.3937
KNOWN_WIDTH = 15*0.3937
KNOWN_HEIGHT = 15*0.3937
focalLength = 201.77682240804037

motor_speed = 70
real_world_speed = 0.165 # motor speed 70

# Flag for count a period of time
TIMER = False
# three tasks
TARGET_1 = False
TARGET_2 = False
TARGET_3 = False

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
camera = cv2.VideoCapture(0)
#%% Initialization

#PiCar Setting
PiCar_Init()

#%% PiCar Information

def PosUpdate(x_cur, y_cur, theta_cur, time_step, dis, diff_x):
    x_cur = 1.62 - (dis/100)
    diff_x = distance_to_camera(KNOWN_WIDTH, focalLength, diff_x, 3)
    #y_cur = y_cur - diff_x
    print("Current Position: (%.2f,%.2f,%.2f)"%(x_cur,y_cur,theta_cur))
    return x_cur, y_cur, theta_cur 

def PosUpdate2(x_cur, y_cur, theta_cur, dis, diff_x):
    x_cur = 1
    diff_x = distance_to_camera(KNOWN_WIDTH, focalLength, diff_x, 3)
    y_cur = 2.45 - dis/100
    #y_cur = y_cur - diff_x
    print("Current Position: (%.2f,%.2f,%.2f)"%(x_cur,y_cur,theta_cur))
    return x_cur, y_cur, theta_cur 

def PosUpdate3(x_cur, y_cur, theta_cur, dis, diff_x):
    y_cur = 2
    diff_x = distance_to_camera(KNOWN_WIDTH, focalLength, diff_x, 3)
    x_cur = -0.8 + dis/100
    #y_cur = y_cur - diff_x
    print("Current Position: (%.2f,%.2f,%.2f)"%(x_cur,y_cur,theta_cur))
    return x_cur, y_cur, theta_cur 

def PosUpdate4(x_cur, y_cur, theta_cur, dis, diff_x):
    x_cur = -0.5
    diff_x = distance_to_camera(KNOWN_WIDTH, focalLength, diff_x, 3)
    y_cur = -0.6 + dis/100
    #y_cur = y_cur - diff_x
    print("Current Position: (%.2f,%.2f,%.2f)"%(x_cur,y_cur,theta_cur))
    return x_cur, y_cur, theta_cur 


#%% Process part
    
def main(TARGET_1, TARGET_2, TARGET_3):
    
    target = np.array([[1,0,0],[1,2,math.pi],[0,0,0]])
    QR_pos = np.array([[1.89,0],[1,2.45],[-0.8,2],[-0.1,-0.6]])
    x_cur, y_cur, theta_cur = 0, 0, 0
    thresh1 = 0.0225
    thresh2 = 0.6
    thresh3 = 0.7
    thresh4 = 0.58
    
    print("//////////TARGET 1 PROCESSING//////////")
    while TARGET_1 != True:
        time_0 = clock()
        tar = target[0]
        delta_x, delta_y, delta_theta = tar[0]-x_cur, tar[1]-y_cur, tar[2]-theta_cur
        error1 = np.square(tar[0]-x_cur) + np.square(tar[1]-y_cur)
        #error1 = abs(tar[0]-x_cur)
        print(tar[0])
        print("error1:", error1)
        
        if error1 < thresh1:
            print("//////////TARGET 1 arrived!//////////")
            bw.stop()
            TARGET_1 = True
            sleep(3)
            break
        
        sleep(3)
        Straight(delta_x)
        sleep(3)
        dis, diff_x, QR_1 = QR_DistanceDetect(4)
        time_step = clock()-time_0
        x_cur, y_cur, theta_cur = PosUpdate(x_cur, y_cur, theta_cur, time_step, dis, diff_x)
        
        if ord(getch.getch()) in [68,100]:
            break
              
    print("//////////TARGET 2 PROCESSING//////////")
    # Turn to target 2
    Motor_turn('forward',55,70,3)
    # straight walk
    Motor_turn('forward',90,70,7)
    while TARGET_2 != True:
        tar = target[1]
        QR2 = QR_pos[1]
        QR3 = QR_pos[2]
        error2 = np.square(QR2[0]-x_cur) + np.square(QR2[1]-y_cur)
        #error2 = abs(QR2[1]-y_cur)
        error3 = np.square(QR3[0]-x_cur) + np.square(QR3[1]-y_cur)
        #error3 = abs(QR3[0]-x_cur)
        
        if error3 < thresh3:
            print("//////////TARGET 2 arrived!//////////")
            bw.stop()
            TARGET_2 = True
            sleep(3)
            break        
        
        while error2 > thresh2:            
            dis, diff_x, QR_1 = QR_Find_Detect(10)
            LR_Cali(dis,diff_x)
            Straight((dis-55)/100)           
            x_cur, y_cur, _ = PosUpdate2(x_cur, y_cur, theta_cur, dis, diff_x)
            #error2 = np.square(QR2[0]-x_cur) + np.square(QR2[1]-y_cur)
            error2 = abs(QR2[1]-y_cur)
            print("error2:", error2)
            
        print("////Checkpoint////")
        Motor_turn('forward',60,70,3)         
        Motor_turn('forward',93,70,6)
        while error3 > thresh3:            
            dis, diff_x, QR_1 = QR_Find_Detect(10)
            LR_Cali(dis,diff_x)
            Straight((dis-70)/100)           
            x_cur, y_cur, _ = PosUpdate3(x_cur, y_cur, theta_cur, dis, diff_x)
            #error3 = np.square(QR3[0]-x_cur) + np.square(QR3[1]-y_cur)
            error3 = abs(QR3[0]-x_cur)
            print("error3:", error3)                                           
            
    
    print("//////////TARGET 3 PROCESSING//////////")
    # Turn to target 2
    Motor_turn('forward',55,70,2.5)
    # straight walk
    Motor_turn('forward',90,70,9)
    while TARGET_3 != True:
        tar = target[2]
        QR4 = QR_pos[3]
        error4 = np.square(QR4[0]-x_cur) + np.square(QR4[1]-y_cur)
        #error4 = abs(QR4[1]-y_cur)
        
        if error4 < thresh4:
            print("//////////TARGET 3 arrived!//////////")
            bw.stop()
            TARGET_3 = True
            sleep(3)
            break        
        
        while error4 > thresh4:            
            dis, diff_x, QR_1 = QR_Find_Detect(10)
            LR_Cali(dis,diff_x)
            Straight((dis-50)/100)           
            x_cur, y_cur, _ = PosUpdate4(x_cur, y_cur, theta_cur, dis, diff_x)
            #error4= np.square(QR4[0]-x_cur) + np.square(QR4[1]-y_cur)
            error4 = abs(QR4[0]-x_cur)
            print("error4:", error4)
        
        Motor_turn('forward',60,70,3)
    


if __name__ == '__main__':
    try:
        main(TARGET_1, TARGET_2, TARGET_3)
        destroy()
    except KeyboardInterrupt:
        destroy()

