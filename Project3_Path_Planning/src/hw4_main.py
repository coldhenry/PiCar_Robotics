# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 13:39:34 2019

@author: coldhenry
"""
from picar import front_wheels, back_wheels
import picar
from time import sleep, clock
import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt
from src_voronoi import *
from src_visgraph import *
import pyvisgraph as vg
from pyvisgraph.visible_vertices import edge_in_polygon
from src_motor import *

# parameter
N_KNN = 5  # number of edge from one sampled point
MAX_EDGE_LEN = 15.0  # [m] Maximum edge length

show_animation = True

#PiCar Setting
bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
picar.setup()
bw.speed = 0
fw.turn(90)

print(__file__ + " start!!")

#%% Initialization 

# start, checkpoint, and goal position
sx = 78.0  # [inch]
sy = 18.0  # [inch]
mx = 48.0  # [inch]
my = 78.0  # [inch]
gx = 18.0  # [inch]
gy = 48.0  # [inch]
robot_size = 1.0  # [inch]
v = 4.3 # [inch]
#build the map
cx, cy = Obstacle_Map(sx,sy,mx,my,gx,gy,show_animation)

#%% Path planning - Voronoi method 

rx1, ry1 = VRM_planning(sx, sy, mx, my, cx, cy, robot_size)
rx2, ry2 = VRM_planning(mx, my, gx, gy, cx, cy, robot_size)

assert rx1, 'Cannot found path'
assert rx2, 'Cannot found path'

if show_animation:  # pragma: no cover
    plt.plot(rx1, ry1, "-r")
    plt.plot(rx2, ry2, "-r")
    plt.savefig("filename.png")
    plt.show()
    
rx_vor, ry_vor = rx2+rx1, ry2+ry1
rx_vor, ry_vor = rx_vor[::-1], ry_vor[::-1]
#rx_vor1, ry_vor1 = rx1[::-1], ry1[::-1]
#rx_vor2, ry_vor2 = rx2[::-1], ry2[::-1]
    
#%% Path Planning - Visibility Graph method

cspace = [[vg.Point(sx,sy)],[vg.Point(mx,my)],[vg.Point(gx,gy)],[vg.Point(12.0,12.0), vg.Point(12.0,84.0), vg.Point(84.0,84.0),vg.Point(84.0,12.0)],
          [vg.Point(24.0,24.0), vg.Point(24.0,72.0), vg.Point(72.0,72.0), vg.Point(72.0,24.0)]]

Obstacle_Map_Vis(polys,sx,sy,gx,gy,mx,my)
g = VisibilityGraph(cspace)
path_vis = ShortestPath(g,sx,sy,mx,my,gx,gy)

#%% Track the trajectories
"""   
1. loop through every point of the trajectory
2. calculate the difference between current position and the next target point
3. write a drive function
4. wrtie a function to control when there is error
5. a measure feedback function (QR code)

"""    

#rx1 = rx_vor1
#ry1 = ry_vor1
#rx2 = rx_vor2
#ry2 = ry_vor2
cur_x = sx
cur_y = sy
cur_theta = 1.57 # start orientation : 90 degrees 
pos = np.array([[cur_x], [cur_y], [cur_theta],[v]])

pos_x = []
pos_y = []
tr_x = []
tr_y = []

FLAG_Visibility = 1
FLAG_Voronoi = 0

#%% Prediction
for pts in path_vis:
    tar_x, tar_y = pts.x, pts.y
    print("now the point is:(",tar_x,tar_y,")")
    print("current pos:",pos)
    pos = Prediction(pos,tar_x,tar_y)
    pos_x.append(pos[0][0])
    pos_y.append(pos[1][0])
    tr_x.append(tar_x)
    tr_y.append(tar_y)

plt.plot(pos_x,pos_y,'-b')
plt.plot(tr_x,tr_y,'-r')
plt.title('PiCar prediction ')
plt.axis('equal')
plt.savefig("test.png")
plt.show()    

#%% Visibility graph tracking
if FLAG_Visibility == True:    
    QRpos1 = [0,78]
    pos = Vis_track1(pos,path_vis[1])
    sleep(3)
    pos = Vis_track1(pos,path_vis[2])
    pos = LocalCali(pos,path_vis[2].x,path_vis[2].y,QRpos1)
    sleep(3)
    pos = Vis_track2(pos,path_vis[3])
    sleep(3)
    pos = Vis_track3(pos,path_vis[4])

#%% Voronoi tracking

if FLAG_Voronoi == True:
    pos = Vor_track(pos,rx_vor[0], ry_vor[0])
    pos = Vor_track(pos,rx_vor[1], ry_vor[1])
    pos = Vor_track(pos,rx_vor[2], ry_vor[2])
    sleep(3)
    pos = Vor_track1(pos,rx_vor[3], ry_vor[3])
    sleep(3)
    pos = Vor_track(pos,rx_vor[4], ry_vor[4])
    pos = Vor_track(np.array([[48], [78], [3.14],[v]]),rx_vor[5], ry_vor[5])
    sleep(3)
    pos = Vor_track1(pos,rx_vor[6], ry_vor[6])
    pos = Vor_track1(pos,rx_vor[7], ry_vor[7])
    

