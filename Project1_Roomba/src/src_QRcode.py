# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:41:43 2019

@author: coldh
"""
from picar import front_wheels, back_wheels
import pyzbar.pyzbar as pyzbar
import numpy as np
import math
import cv2
from src_motor import Motor_turn, Straight
from time import clock
from random import randint

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

camera = cv2.VideoCapture(0)

#%% QRcode Functions
def decode(im):
    Objs = pyzbar.decode(im)
    """
    for obj in Objs:
        print('Type :', obj.type)
        print('Data :', obj.data.decode("utf-8"),'\n')
    """ 
    return Objs
    

def QR_display(im,Objs,QRtarget):
    QR = []    
    for obj in Objs:
        if (obj.data.decode("utf-8")) == QRtarget:
            QR = obj
            points = obj.polygon
            x = (points[0].x+points[2].x)/2
            y = (points[0].y+points[2].y)/2
            coordinate = (int(x),int(y))
            a, b = np.square(points[0].x-points[1].x), np.square(points[0].y-points[1].y)
            pixel= math.sqrt(a+b)
            #print(pixel)
            
            n = len(points) 
            for j in range(0,n):
                cv2.line(im,points[j],points[(j+1) % n], (255,0,0), 3)
            cv2.circle(im,coordinate,5,(255,255,0),3)
            #cv2.putText(im, "%.2f,%.2f" % (x,y), (int(x/2), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
            #               1.0, (0, 255, 0), 3) 
            break
        else:
            pixel = 10000000000000
            coordinate = (0,0)
            QR = []
    
    #cv2.imshow("capture2", im)
    return pixel, coordinate, QR

def find_QR(image,QRtarget):
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #(T,thresh)=cv2.threshold(gray,128,255,cv2.THRESH_BINARY)
    Objs = decode(image)
    if Objs != []:
        perWidth, pts , QR= QR_display(image,Objs,QRtarget)
    else:
        perWidth = 10000000000000
        pts = (0,0)
        QR = []
    return perWidth, pts, QR

def QR_Find_Detect(time,QRtarget):
    while camera.isOpened():
        ret, frame = camera.read()
        if ret == True:
            dis, diff_x, QR_1 = QR_DistanceDetect(time,QRtarget)
            if dis != 0 : # findQR
                print("QR code find!")
                return dis, diff_x, QR_1
            else: # make a left turn to check if theres a QR
                print("See nothing, start serching...")
                Motor_turn('backward',90,50,1) # dirve backward first
                if dis != 0 :
                    print("QR code find!")
                    return dis, diff_x, QR_1                
                else:
                    Motor_turn('forward',80,50,1)
                    dis, diff_x, QR_1 = QR_DistanceDetect(time,QRtarget)
                    if dis != 0 :
                        print("QR code find!")
                        return dis, diff_x, QR_1
                    else: # drive back and do a right check this time
                        Motor_turn('backward',80,50,1)
                        Motor_turn('forward',100,50,1)
                        if dis != 0 :
                            print("QR code find!")
                            return dis, diff_x, QR_1
                        else:
                            print("ERROR: No QR code in this view")
 
def distance_to_camera(knownWidth, focalLength, perWidth, scale):  
    # compute and return the distance from the maker to the camera
    if perWidth==0:
        cms =0
    else:
        inchs = (knownWidth * focalLength) / perWidth 
        cms = inchs * 30.48 / 12 * scale
    return cms*0.39370079    
 
def Mode(data,period): 
    counts = np.bincount(data[1:period-1])
    ind = np.argmax(counts)
    if ind==0 & counts[0]<=int(period/2):
        #print("counts:",counts[0])
        counts[0]=0
        ind = np.argmax(counts)
    #print(ind)
    return float(ind)

def QR_count(data):
    tag = max(data,key=data.count)
    if tag == "Landmark 1":
        return 1
    elif tag == "Landmark 2":
        return 2
    elif tag == "Landmark 3":
        return 3
    elif tag == "Landmark GOAL":
        return 4
    else:
        return 5

def QR_DistanceDetect(time, QRtarget):
    print("---------Estimation-----------") 
    count = 0
    dis = 0
    period = 100
    data = np.zeros(period, dtype=int)
    data_x = np.zeros(period, dtype=int)
    data_y = np.zeros(period, dtype=int)
    data_QR = []
    center_x = 0
    center_y = 0
    diff_x = 0
    QR_1 = 'NaN'
    total_time = 0
    count_QR = 0
    
    while camera.isOpened():
        #if count%5 ==0:
        #    print("Wait time:",total_time)
        t_0 = clock()
        count = count + 1      
        ret, frame = camera.read()
        
        # To count the update period
        if abs(time-total_time) < 0.5 : #or count > period
            TIMER = True
        else:
            TIMER = False       
        
        if TIMER == False: 
            # get a frame
            if ret==True:
                perWidth, points, QR = find_QR(frame, QRtarget)
                perWidth = abs(round(perWidth))
                tmp_x = abs(round(points[0]))
                tmp_y = abs(round(points[1]))
                #if count%5==0:
                #    print(perWidth)
                if perWidth > 5000:
                    data[count]=0; data_x[count]=0 ;data_y[count]=0
                    data_QR.append('NaN')
                else:
                    data[count]=int(perWidth); data_x[count]= tmp_x; data_y[count]= tmp_y
                    #print("QR:",QR)
                    tag = str(QR.data.decode("utf-8"))
                    data_QR.append(tag)
            else:
                print("ERROR: ret is False")
                break  
            
        else: # when timer is on          
            count_QR = QR_count(data_QR)
            #print("data_QR:",data_QR,", QR is:",count_QR)
            i = randint(0,100)
            cv2.imwrite('/home/coldhenry/Desktop/QR_pic/Testing/Mark'+ str(i) +'.jpg', frame)
            avg_width = Mode(data,period)
            center_x = Mode(data_x,period)
            center_y = Mode(data_y,period)
            scale = 3.0
            dis = distance_to_camera(KNOWN_WIDTH, focalLength, avg_width, scale)
            data = np.zeros(period,dtype=int)
            count = 0
        
            diff_x = center_x - width_img/2  
            if len(QR)>0:
                QR_1 = QR.data.decode("utf-8")
            print("Target:"+str(QR_1)+"; Distance: ",dis,"; Center: (%i,%i); Drift: %i"%(center_x,center_y,diff_x))
            break
        
        #cv2.putText(frame, "%.2fcm" % (dis), (frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
        #               2.0, (0, 255, 0), 3) 
        #cv2.imshow("capture", frame)
               
        
        total_time = total_time + (clock()-t_0)
        #if (cv2.waitKey(1) & 0xFF == ord('q')) : #or abs(total_time-time) < 0.5
        #    break
        
    print("---------Estimation End-----------")   
    return dis, diff_x, count_QR


def LR_Cali(dis, diff_x,QRtarget):
    thresh = 80
    print("----------LR Calibration----------")
    if abs(diff_x) < thresh:
        print('***No Calibration needed***')
    while abs(diff_x) > thresh:
        if dis < 24:
            Motor_turn('backward',90,50,1)
            dis, diff_x, _ = QR_Find_Detect(5,QRtarget)
        if diff_x > 0 : # on the right of center
            print("NOW: QR on the right")
            Motor_turn('backward',90,50,1)
            Motor_turn('forward',100,30,2)
            dis, diff_x, _ = QR_Find_Detect(5,QRtarget)
        elif diff_x < 0:
            print("NOW: QR on the left")
            Motor_turn('backward',90,50,1)
            Motor_turn('forward',80,30,2)
            dis, diff_x, _ = QR_Find_Detect(5,QRtarget)
        else:            
            break
    print("----------LR Calibration End----------")
    

def destroy():
    bw.stop()
    camera.release()
    cv2.destroyAllWindows()
    
#%% TEST CODE
""" 
camera = cv2.VideoCapture(0)

print("start!")
count = 0
while(camera.isOpened()):
    ret, frame = camera.read()
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        print("-----------Stop----------")
        break
    if ret == True:
        dis, diff_x, _ = QR_DistanceDetect(3)
        print(dis)
    elif count>500: break
    else: break
    count = count+1
print("end!")
destroy()
"""