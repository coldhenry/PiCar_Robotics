# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:43:40 2019

@author: coldh
"""
from picar import front_wheels, back_wheels
import picar
from time import sleep

width_img = 640
height_img = 480
KNOWN_DISTANCE = 50*0.3937
KNOWN_WIDTH = 15*0.3937
KNOWN_HEIGHT = 15*0.3937
focalLength = 201.77682240804037

motor_speed = 70
real_world_speed = 0.165 # motor speed 70

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()

#%% Motion functions

def PiCar_Init():
    picar.setup()
    bw.speed = 0
    fw.turn(90)

def Straight(delta_x):
    print("--------Moving--------")
    time = abs(delta_x) / real_world_speed
    if time<0.5:
        func_speed = 50
        t = time + 0.3
    else:
        func_speed = 70
        t = time
    print("Estimate using time:",time)
    if delta_x >0:
        print("FORWARD")
        fw.turn(93)
        bw.backward()
    elif delta_x <0:
        print("BACKWARD")
        bw.backward()
    else:
        bw.stop()
    bw.speed = func_speed
    print("MOTOR SPEED:",motor_speed)
    sleep(t)
    bw.stop()
    print("--------Paused--------")
    
def Motor_turn(FB,turn,speed,time):
    if FB =='forward':
        fw.turn(turn); bw.backward(); bw.speed = speed; sleep(time); bw.stop(); fw.turn_straight(); sleep(1)
    if FB =='backward':
        fw.turn(turn); bw.forward(); bw.speed = speed; sleep(time); bw.stop(); fw.turn_straight(); sleep(1)
    
