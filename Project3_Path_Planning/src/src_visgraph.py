# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 15:59:37 2019

@author: coldhenry
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 15:22:06 2019

@author: coldh
"""

import pyvisgraph as vg
from pyvisgraph.visible_vertices import edge_in_polygon
import numpy as np
import matplotlib.pyplot as plt

output_graphfile = 'GSHHS_c_L1.graph'

sx = 78.0  # [inch]
sy = 18.0  # [inch]
mx = 48.0  # [inch]
my = 78.0  # [inch]
gx = 18.0  # [inch]
gy = 48.0  # [inch]

polys = [[vg.Point(sx,sy)],[vg.Point(mx,my)],[vg.Point(gx,gy)],[vg.Point(0.0,0.0), vg.Point(96.0,0.0), vg.Point(96.0,96.0),vg.Point(0.0,96.0)],
          [vg.Point(36.0,36.0), vg.Point(36.0,60.0), vg.Point(60.0,60.0), vg.Point(60.0,36.0)]]

cspace = [[vg.Point(sx,sy)],[vg.Point(mx,my)],[vg.Point(gx,gy)],[vg.Point(12.0,12.0), vg.Point(12.0,84.0), vg.Point(84.0,84.0),vg.Point(84.0,12.0)],
          [vg.Point(24.0,24.0), vg.Point(24.0,72.0), vg.Point(72.0,72.0), vg.Point(72.0,24.0)]]

def Obstacle_Map_Vis(polys,sx,sy,gx,gy,mx,my):
    for i in range(len(polys)):
        #print("\n",polys[i])
        x_ = []
        y_ = []
        for j in range(len(polys[i])):
            #print(polys[i][j].x,polys[i][j].y)
            x_.append(polys[i][j].x)
            y_.append(polys[i][j].y)
        x_.append(polys[i][0].x)
        y_.append(polys[i][0].y)
        #print(x_,y_)
        lines = plt.plot(x_,y_)
        plt.setp(lines, color='gray', linewidth=50)
    
    plt.plot(sx, sy, "^r")
    plt.plot(gx, gy, "^c")
    plt.plot(mx, my, "^g")
    
    plt.grid(True)
    plt.axis("equal")

def VisibilityGraph(cspace):
    g = vg.VisGraph()
    g.build(cspace)
    g.save('GSHHS_c_L1.graph')
    g2 = vg.VisGraph()
    g2.load('GSHHS_c_L1.graph')
    
    plt.plot(sx, sy, "^r", ms=15.0)
    plt.plot(gx, gy, "^c", ms=15.0)
    plt.plot(mx, my, "^g", ms=15.0)
    
    for i in range(len(cspace)):
        #print("\n",polys[i])
        for j in range(len(cspace[i])):
            pts = cspace[i][j]
            #print("now is",pts)
            for z in g2.find_visible(pts):
                #print(z)
                #print(edge_in_polygon(pts,z,k))
                line1 = plt.plot([pts.x,z.x],[pts.y,z.y],'-b')
    
    plt.setp(line1, color='black', linewidth=0.1)
    return g

def ShortestPath(g,sx,sy,mx,my,gx,gy):

    shortest1 = g.shortest_path(vg.Point(sx,sy), vg.Point(mx, my))
    print(shortest1)
    shortest2 = g.shortest_path(vg.Point(mx,my), vg.Point(gx, gy))
    print(shortest2)
    num_pts1, num_pts2 = len(shortest1), len(shortest2)
    
    for i in range(num_pts1-1):
        plt.plot([shortest1[i].x,shortest1[i+1].x],[shortest1[i].y,shortest1[i+1].y],'-r')
    for i in range(num_pts2-1):
        plt.plot([shortest2[i].x,shortest2[i+1].x],[shortest2[i].y,shortest2[i+1].y],'-r')
    
    plt.grid(True)
    plt.axis("equal")
    plt.show()
    shortest = shortest1[:2]+shortest2
    print(shortest)
    return shortest
