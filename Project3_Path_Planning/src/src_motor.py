# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:43:40 2019

@author: coldh
"""
import math
import picar
import numpy as np
from picar import front_wheels, back_wheels
from time import sleep
from src_QRcode import QR_Find_Detect

width_img = 640
height_img = 480
KNOWN_DISTANCE = 50*0.3937
KNOWN_WIDTH = 15*0.3937
KNOWN_HEIGHT = 15*0.3937
focalLength = 201.77682240804037
"""
speed 50 angle 60 : 4.3 inches / 20 degree/s
speed 30 angle __ : 2.2 inches / __ degree/s

"""
motor_speed = 50
real_world_speed = 4.3 # unit[inch]motor speed 50
rotation_speed = 18 # degree/s when turn angle 60 + speed 50

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
picar.setup()
#%% Motion functions

#bw.backward(); bw.speed = 50; sleep(3); bw.stop()
#Motor_turn('forward',45,50,5)   

def Straight(delta_x):
    print("--------Moving--------")
    time = abs(delta_x) / real_world_speed
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
    bw.speed = motor_speed
    #print("MOTOR SPEED:",motor_speed)
    sleep(time)
    bw.stop()
    print("--------Paused--------")
    return time
    
def Motor_turn(FB,turn,speed,time):
    if FB =='forward':
        fw.turn(turn); bw.backward(); bw.speed = speed; sleep(time); bw.stop(); fw.turn_straight(); sleep(1)
    if FB =='backward':
        fw.turn(turn); bw.forward(); bw.speed = speed; sleep(time); bw.stop(); fw.turn_straight(); sleep(1)
    
def LR_Cali(dis, diff_x):
    thresh = 40
    print("----------LR Calibration----------")
    while abs(diff_x) > thresh:
        if dis < 65:
            Motor_turn('backward',90,50,2)
            dis, diff_x, _ = QR_Find_Detect(5)
        if diff_x > 0 : # on the right of center
            Motor_turn('backward',90,50,2)
            Motor_turn('forward',100,50,1.5)
            dis, diff_x, _ = QR_Find_Detect(5)
        elif diff_x < 0:
            Motor_turn('backward',90,50,2)
            Motor_turn('forward',80,50,1.5)
            dis, diff_x, _ = QR_Find_Detect(5)
        else:
            break
    print("----------LR Calibration End----------")
    
def calc_input(yawrate):
    print("yawrate:",yawrate)
    v = real_world_speed  # [inch/s]
    yawrate = yawrate*0.0174532925  # [rad/s]
    u = np.array([[v], [yawrate]])
    print("u:",u)
    return u

def motion_model(x, u, DT):
    F = np.array([[1.0, 0, 0, 0],
                  [0, 1.0, 0, 0],
                  [0, 0, 1.0, 0],
                  [0, 0, 0, 0]])
    #print("DEBUG x:",math.cos(x[2,0]),math.sin(x[2,0]))
    B = np.array([[DT * math.cos(x[2, 0]), 0],
                  [DT * math.sin(x[2, 0]), 0],
                  [0.0, DT],
                  [1.0, 0.0]])

    x = F @ x + B @ u
    

    return x

def Track(pos,tar_x,tar_y):
    """
    1. calculate the orientation difference
    2. calculate the distance
    3. turn
    4. move
    """
    #FLAG= 1
    u = calc_input(0)
    threshold = 5 # unit[degree]
    #%% Open control part
    cur_x, cur_y, cur_theta = pos[0][0], pos[1][0], pos[2][0]
    dx = tar_x - cur_x
    dy = tar_y - cur_y
    deg = math.degrees(math.atan2(dy,dx))
    #print("deg",deg)
    diff_deg = math.degrees(cur_theta) - deg
    #print("angle:",diff_deg)
    t_turn = abs(diff_deg) / rotation_speed
    if dx != 0 and dy != 0:
        if diff_deg>threshold:
            print("-----Trun right-----")
            print("Estimated using time:",t_turn)
            Motor_turn('forward',120,motor_speed,t_turn)
            u = calc_input(-rotation_speed)
        elif diff_deg<0:
            print("-----Trun left-----")
            print("Estimated using time:",t_turn)
            Motor_turn('forward',60,motor_speed,t_turn)
            u = calc_input(rotation_speed)
        else: 
            print("orientation finished")
    pos = motion_model(pos,u,t_turn)
    #move
    dx1 = tar_x - pos[0]
    dy1 = tar_y - pos[1]
    dis = math.sqrt(abs(dx1)**2+abs(dy1)**2)
    t_move = Straight(dis)
    u1 = calc_input(0)
    pos = motion_model(pos,u1,t_move)
    
    
    return pos

def Prediction(pos,tar_x,tar_y):
        
    u = calc_input(0)
    threshold = 5 # unit[degree]
    #%% Open control part
    cur_x, cur_y, cur_theta = pos[0][0], pos[1][0], pos[2][0]
    dx = tar_x - cur_x
    dy = tar_y - cur_y
    deg = math.degrees(math.atan2(dy,dx))
    if deg<0: deg = deg+360
    print("deg",deg)
    diff_deg = math.degrees(cur_theta) - deg
    print("angle:",diff_deg)
    t_turn = abs(diff_deg) / rotation_speed
    if dx!=0 and dy!=0:
        if diff_deg>threshold:
            print("-----Trun right-----")
            print("Estimated using time:",t_turn)
            u = calc_input(-rotation_speed)
        elif diff_deg<0:
            print("-----Trun left-----")
            print("Estimated using time:",t_turn)
            u = calc_input(rotation_speed)
        else: 
            print("orientation finished")
    dt = 0.1
    for i in range(0,math.floor(t_turn/dt)):
        pos = motion_model(pos,u,dt) 
    print("rota_Pos be updated:",pos)
    #move
    dx1 = tar_x - pos[0]
    dy1 = tar_y - pos[1]
    dis = math.sqrt(abs(dx1)**2+abs(dy1)**2)
    t_move = dis / real_world_speed
    u1 = calc_input(0)
    pos = motion_model(pos,u1,t_move)
    print("trans_Pos be updated:",pos)
    
    
    return pos

def Vis_track1(pos,path_vis):
    #%% start to 1st point
    u = calc_input(0)
    threshold = 5 # unit[degree]
    pts1_x, pts1_y = path_vis.x, path_vis.y
    print("now is:",pts1_x,pts1_y)
    cx, cy, ctheta= pos[0][0],pos[1][0],pos[2][0]
    print("curent pts:",cx,cy)
    dx = pts1_x - cx
    dy = pts1_y- cy
    deg = math.degrees(math.atan2(dy,dx))
    if deg<0: deg = deg+360
    print("deg",deg)
    diff_deg = math.degrees(ctheta) - deg
    print("angle:",diff_deg)
    t_turn = abs(diff_deg) / rotation_speed
    if dx != 0 and dy != 0:
        if abs(diff_deg)>10:
            if diff_deg>threshold:
                print("-----Trun right-----")
                print("Estimated using time:",t_turn)
                Motor_turn('forward',120,motor_speed,t_turn)
                u = calc_input(-rotation_speed)
                pos = motion_model(pos,u,t_turn) 
            elif diff_deg<0:
                print("-----Trun left-----")
                print("Estimated using time:",t_turn)
                Motor_turn('forward',50,motor_speed,t_turn)
                u = calc_input(rotation_speed)
                pos = motion_model(pos,u,t_turn) 
            else: 
                print("orientation finished")      

    print("rota_Pos be updated:",pos)
    #move
    dx1 = pts1_x - pos[0]
    dy1 = pts1_y - pos[1]
    dis = math.sqrt(abs(dx1)**2+abs(dy1)**2)
    print("dis:",dis)
    t_move = (dis-6) / real_world_speed
    u1 = calc_input(0)
    Straight(dis-6)
    pos = motion_model(pos,u1,t_move)
    print("trans_Pos be updated:",pos)
    return pos

def Vis_track2(pos,path_vis):
    #%% start to 1st point
    u = calc_input(0)
    threshold = 5 # unit[degree]
    pts1_x, pts1_y = path_vis.x, path_vis.y
    print("<<<<<< NOW is:",pts1_x,pts1_y,">>>>>>")
    cx, cy, ctheta= pos[0][0],pos[1][0],pos[2][0]
    print("curent pts:",cx,cy)
    dx = pts1_x - cx
    dy = pts1_y- cy
    deg = math.degrees(math.atan2(dy,dx))
    if deg<0: deg = deg+360
    print("deg",deg)
    diff_deg = math.degrees(ctheta) - deg
    print("angle:",diff_deg)
    t_turn = abs(diff_deg) / rotation_speed
    if dx != 0 and dy != 0:
        if abs(diff_deg)>10:
            if diff_deg>threshold:
                print("-----Trun right-----")
                print("Estimated using time:",t_turn)
                Motor_turn('forward',120,motor_speed,t_turn)
                u = calc_input(-rotation_speed)
                pos = motion_model(pos,u,t_turn) 
            elif diff_deg<0:
                print("-----Trun left-----")
                print("Estimated using time:",t_turn)
                Motor_turn('forward',60,motor_speed,t_turn)
                u = calc_input(rotation_speed)
                pos = motion_model(pos,u,t_turn) 
            else: 
                print("orientation finished")      

    print("rota_Pos be updated:",pos)
    #move
    dx1 = pts1_x - pos[0]
    dy1 = pts1_y - pos[1]
    dis = math.sqrt(abs(dx1)**2+abs(dy1)**2)
    print("dis:",dis)
    t_move = (dis-6) / real_world_speed
    u1 = calc_input(0)
    Straight(dis-6)
    pos = motion_model(pos,u1,t_move)
    print("trans_Pos be updated:",pos)
    return pos

def Vis_track3(pos,path_vis):
    #%% start to 1st point
    u = calc_input(0)
    threshold = 5 # unit[degree]
    pts1_x, pts1_y = path_vis.x, path_vis.y
    print("now is:",pts1_x,pts1_y)
    cx, cy, ctheta= pos[0][0],pos[1][0],pos[2][0]
    print("curent pts:",cx,cy)
    dx = pts1_x - cx
    dy = pts1_y- cy
    deg = math.degrees(math.atan2(dy,dx))
    if deg<0: deg = deg+360
    print("deg",deg)
    diff_deg = math.degrees(ctheta) - deg
    print("angle:",diff_deg)
    t_turn = abs(diff_deg) / rotation_speed
    if dx != 0 and dy != 0:
        if abs(diff_deg)>10:
            if diff_deg>threshold:
                print("-----Trun right-----")
                print("Estimated using time:",t_turn)
                Motor_turn('forward',120,motor_speed,t_turn)
                u = calc_input(-rotation_speed)
                pos = motion_model(pos,u,t_turn) 
            elif diff_deg<0:
                print("-----Trun left-----")
                print("Estimated using time:",t_turn)
                Motor_turn('forward',60,motor_speed,t_turn)
                u = calc_input(rotation_speed)
                pos = motion_model(pos,u,t_turn) 
            else: 
                print("orientation finished")      

    print("rota_Pos be updated:",pos)
    #move
    dx1 = pts1_x - pos[0]
    dy1 = pts1_y - pos[1]
    dis = math.sqrt(abs(dx1)**2+abs(dy1)**2)
    print("dis:",dis)
    t_move = (dis) / real_world_speed
    u1 = calc_input(0)
    #Straight(dis)
    pos = motion_model(pos,u1,t_move)
    print("trans_Pos be updated:",pos)
    return pos

def Vor_track(pos,vor_x,vor_y):
    #%% start to 1st point
    u = calc_input(0)
    threshold = 5 # unit[degree]
    pts1_x, pts1_y = vor_x, vor_y
    print("now is:",pts1_x,pts1_y)
    cx, cy, ctheta= pos[0][0],pos[1][0],pos[2][0]
    print("curent pts:",cx,cy)
    dx = pts1_x - cx
    dy = pts1_y- cy
    deg = math.degrees(math.atan2(dy,dx))
    if deg<0: deg = deg+360
    print("deg",deg)
    diff_deg = math.degrees(ctheta) - deg
    print("angle:",diff_deg)
    t_turn = abs(diff_deg) / rotation_speed
    if dx != 0 and dy != 0:
        if abs(diff_deg)>10:
            if diff_deg>threshold:
                print("-----Trun right-----")
                print("Estimated using time:",t_turn)
                Motor_turn('forward',120,motor_speed,t_turn)
                u = calc_input(-rotation_speed)
            elif diff_deg<0:
                print("-----Trun left-----")
                print("Estimated using time:",t_turn)
                Motor_turn('forward',60,motor_speed,t_turn)
                u = calc_input(rotation_speed)
            else: 
                print("orientation finished")      
    dt = 0.1
    for i in range(0,math.floor(t_turn/dt)):
        pos = motion_model(pos,u,dt) 
    print("rota_Pos be updated:",pos)
    #move
    dx1 = pts1_x - pos[0]
    dy1 = pts1_y - pos[1]
    dis = math.sqrt(abs(dx1)**2+abs(dy1)**2)
    print("dis:",dis)
    t_move = (dis) / real_world_speed
    u1 = calc_input(0)
    Straight(dis)
    pos = motion_model(pos,u1,t_move)
    print("trans_Pos be updated:",pos)
    return pos

def Vor_track1(pos,vor_x,vor_y):
    #%% start to 1st point
    u = calc_input(0)
    threshold = 5 # unit[degree]
    pts1_x, pts1_y = vor_x, vor_y
    print("now is:",pts1_x,pts1_y)
    cx, cy, ctheta= pos[0][0],pos[1][0],pos[2][0]
    print("curent pts:",cx,cy)
    dx = pts1_x - cx
    dy = pts1_y- cy
    deg = math.degrees(math.atan2(dy,dx))
    if deg<0: deg = deg+360
    print("deg",deg)
    diff_deg = math.degrees(ctheta) - deg
    print("angle:",diff_deg)
    t_turn = abs(diff_deg) / rotation_speed
    if dx != 0 and dy != 0:
        if abs(diff_deg)>10:
            if diff_deg>threshold:
                print("-----Trun right-----")
                print("Estimated using time:",t_turn)
                Motor_turn('forward',120,motor_speed,t_turn)
                u = calc_input(-rotation_speed)
            elif diff_deg<0:
                print("-----Trun left-----")
                print("Estimated using time:",t_turn)
                Motor_turn('forward',60,motor_speed,t_turn)
                u = calc_input(rotation_speed)
            else: 
                print("orientation finished")      
    dt = 0.01
    for i in range(0,math.floor(t_turn/dt)):
        pos = motion_model(pos,u,dt) 
    print("rota_Pos be updated:",pos)
    #move
    dx1 = pts1_x - pos[0]
    dy1 = pts1_y - pos[1]
    dis = math.sqrt(abs(dx1)**2+abs(dy1)**2)
    print("dis:",dis)
    t_move = (dis-6) / real_world_speed
    u1 = calc_input(0)
    Straight(dis-6)
    pos = motion_model(pos,u1,t_move)
    print("trans_Pos be updated:",pos)
    return pos
    
    
    
    
        


    