# Project 3: Path Planning

 ## Objective

- Design a voronoi based path planner to go from start to the 1st and
  2nd stops.

- Generate a visibility graph based planner to execute the same mission.

## Environment Setup

|                                                              |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project3_Path_Planning/pic/map.png" alt="layout" width="375" /> | <img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project3_Path_Planning/pic/realmap.png" alt="layout" width="375" /> |

The size of the environment is as same as the previous one, which shrinks from 10x10(ft) to 8x8(ft) due to the limitation of the space. And the QR code placement is shown. 

The coordinates of the start point, 1st point, and the 2nd point are marked in the picture below. The unit of the coordinate is an inch.  

 

## Map Representation

   I take the longest part of the car to build the configuration map. In the beginning, I try to make the shape of PiCar to fit in a circle. However, I change to fit in a square. One main reason is to take the practical issue into consideration. The performance of PiCar varies dramatically from time to time, so choose the map that has the biggest C-obstacle is a better choice for me. 

<img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project3_Path_Planning/pic/config.png" alt="layout" width="375" />


Therefore, the configuration map constructed by this strategy is presented below. The set of green lines is the original map and the black one is the configuration map.



## Voronoi based path planner

To construct the Voronoi graph and find the shortest path, there are several steps to go through:

a.   Turn the edges of the configuration map into points. 

b.   Find the 2D Voronoi diagram using the given points. Here I use the library function *scipy.spatial.Voronoi* to find the diagram.

c.   Construct a KDTree class to find the kth nearest neighbor for each point. Here I use the library function *scipy.spatial.cKDTree.*

d.   To find the shortest path in the Voronoi diagram, I use the Dijkstra algorithms. The implementation is referenced from AtsushiSakai_PythonRobotics[1]

e.   After finding the trajectory of the shortest path, decide how many points to be used for the run.

The result is shown on the right side of the images above. The blue lines indicate the Voronoi diagram and the right line refers to the trajectory of the shortest path.

<img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project3_Path_Planning/pic/voronoi.png" alt="layout" width="375" />

## Visibility graph based path planner

To construct the visibility graph, I go through the following steps:

a.   Construct edges from all points in the configuration map.

b.   Check through edges to see if there is an intersection.

c.   Check if each point is visible from a given point.

d.   Store all edges that are visible from each point.

e.   Use the Dijkstra algorithms to find the shortest path.

The construction is referenced from Pyvisgraph from TaipanRex [2]

<img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project3_Path_Planning/pic/visibility.png" alt="layout" width="375" />
 The result is shown below.  The blue lines indicate the visible line from each point and the red lines show the shortest path in the Visibility graph.

## Discussion

Both strategies show different properties from various perspectives. There are four ways to discuss the performance and the difference between the two methods. 

- Shortest path design

  ​	The trajectories of the two methods are very different. The path of visibility graph method is built by line sections, so it shows discontinuity on each turn. As for the path of the Voronoi diagram, we can tell that it is smoother than the previous one since that its definition takes points around the given point to generate the path and this results in a smoother trajectory if we generate sufficient points on obstacles and walls. 

- Scenario

  ​	Given the characteristic we derive from two paths, we know they are suitable in different scenarios. For the Visibility-graph path, the total distance it travels is shorter than Voronoi one since that its principle guides the path to find the shortest way whenever it is reachable in the view. However, the cost it would pay is that the mobile robot would be closer to the obstacle and therefore the error of the trajectory needs to be restricted in a smaller range compared to Voronoi one. On the other hand, the Voronoi-diagram path gives a safer way to travel through targets because it strives to stay between 

- Mobility

   Considering the PiCar into consideration is another problem. 

1. While constructing the configuration map, I expand the area of the obstacle to C-obstacle by the longest part of the PiCar (about 1 foot). Although it ensures the safety, the simplification also ignores some situations that the PiCar is in different angles (since that the C-space would be 3d if it contains every situation).

2. The PiCar becomes a point on the C-space, but how to move from one point to another point is nothing to do with the path itself. The properties of the two paths give PiCar different challenges. 

3. For the Visibility-graph path, as I mentioned in the previous section, it has discontinuities on turns, and in some cases, the turn might be too large that the PiCar is not capable to make a turn without leaving the current position too far. Because it takes extra effort to make a turn and needs additional control strategy and feedback to get it back to the track, it would be more unstable than the Voronoi-based planner.

4. As for the Voronoi-diagram, the problem mentioned above could also happen if I use the wrong number of points on the trajectory. However, it could be perfectly eliminated by choosing points wisely. More points need to be sampled while encountering a turn and fewer points on a straight line.  

* Sample points

  For the Visibility-graph path, since that it is built by line sections, the only sample points are on each end of the line section. Therefore, it doesn’t possess the flexibility to change sample points for performance enhancement. Instead, the Voronoi-graph path could be flexible in choosing sample points. However, it takes extra effort to choose the points manually to show dramatically better performance.

## Video demo

- Visibility-graph-based Path planner demo 

  <img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project3_Path_Planning/pic/visibility.gif" alt="layout" width="540" />

- Voronoi-based path planner demo

   <img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project3_Path_Planning/pic/voronoi.gif" alt="layout" width="540" />

 

## Reference

[1] https://github.com/AtsushiSakai/PythonRobotics

[2] https://github.com/TaipanRex/pyvisgraph

 

 