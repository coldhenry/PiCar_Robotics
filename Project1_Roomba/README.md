

## Objective

Design a “Roomba” like system. The robot should be able to navigate an environment and provide a level of coverage of the area.

## Architecture

In this assignment, we design a Roomba-like robot and let it navigate the environment and provide a level of coverage of given area. To see which architecture fits our robot, we first analyze the properties of a Roomba-like robot.

<img src="C:\Users\coldhenry\Desktop\Fall 2019\CSE_276(PC)\HW\HW5\SA.png" alt="img" style="zoom:60%;" />

For a Roomba-like system, it should consist of several basic functions. First of all, it should be able to detect walls since that these are the boundaries could not be ignored. Secondly, the robot should know where it is to understand how many areas it has already covered. According to functions we request, the Roomba-like robot needs sweeping strategies, boundaries detection, and localization. Based on these, we choose to use the subsumption architecture as my framework. The diagram of the structure is shown below [1]:

In our case, we use 3 levels to describe the Roomba-like robot:

* Level 0: Straight walk.
* Level 1: Avoid.
  Since that we set a boundary for the robot. It should detect the wall periodically and keep a distance from the wall.
* Level 2: Turn: 
  As the robot detect the QR code, if the distance is applicable for a turn. The robot would make a turn.
* Level 3: Shrink the desired distance. 
  There is an initial distance we give that tell the robot to keep with the landmark. Whenever the robot encounters the 4th landmark in particular round, which means that the robot have already gone through 4 edges, it would trigger this state, change the desired distance, and then start another round of sweeping.

More details would be presented in the following sections.

## Coverage Behavior

<img src="C:\Users\coldhenry\Desktop\Fall 2019\CSE_276(PC)\HW\HW5\type1.jpg" alt="imgk" style="zoom:33%;" /> 

As shown in the figure above, the left side is the type 1; and the right side is type 2

We first consider the trajectory the PiCar goes. In the beginning, I tried the trajectories like Type 1. However, this type of path results in some problems. The main problem is that since our car is bi-cycle model, it is not capable of making a turn without using extra space, which means it needs a circular area to turn around and bypasses lots of area that haven’t covered. Thus, it is crucial not to make unnecessary turns to reduce the chance that we need to make another turn so that we can cover the area that ignored due to the previous turn. Also, using this trajectory to sweep the floor make the computation of coverage more difficult. As a result, I choose the type-2 trajectory to avoid the problems.

In this trajectory, the PiCar walks though the boundaries of given area, as one complete rectangular-like trajectory is made. It moves on to another round of sweeping that has a smaller size. Repeat the steps until it reaches the limit. In this type of trajectory, the PiCar walks mostly on line sections instead of curves, which makes the localization easier and stabilizes the performance. 

## Map Arrangement

<img src="C:\Users\coldhenry\Desktop\Fall 2019\CSE_276(PC)\HW\HW5\Picture2.png" alt="img3" style="zoom:48%;" />

To achieve this target, we rearrange the layout of QRcodes on the walls. The new version layout is shown on the right.

The size of the environment is as same as the previous one, which shrinks from 10*10 (ft) to 8*8(ft) due to the limitation of the space. And the QR code placement is shown.

<img src="C:\Users\coldhenry\Desktop\Fall 2019\CSE_276(PC)\HW\HW5\Picture1.png" alt="img5" style="zoom:48%;" />

The real environment is presented below. Note that the black dash lines indicate the visualized trajectory that the PiCar should go.

As you can see, in this version, the landmarks gather at each side. Instead of giving a general version of a map layout, which separate the landmarks uniformly to represent the wall, we emphasize on the four corners of the trajectory. Our localization happens only when the PiCar is going to make a turn, not go straight. Therefore, we want to make sure the PiCar is on the right path before and after it makes a turn.

## Control

After deriving the layout, the algorithm of sweeping is simple. The PiCar walks through rectangular-like trajectories one by one. As it detects the QRcode that shows that the first round of sweeping is done. It would raise the distance between the QRcode and do the second round of sweeping, and so on. 

Based on these thoughts, the control flow is shown:

<img src="C:\Users\coldhenry\Desktop\Fall 2019\CSE_276(PC)\HW\HW5\Picture3.png" alt="img6" style="zoom:48%;" /> 

The target is defined as the distance between the landmark and the PiCar in each round. The distance varies to change the sweeping path the car goes. The PiCar moves first, then it would use the sensor (in our cases, the sensor we have is the camera) to detect the QR code. After deriving the information, we turn to the feedback section. Two information we need to feedback are: whether the PiCar needs to adjust its orientation and whether the PiCar is too far or too close to the landmark. Whenever these decisions are made, the command would be sent back to the hardware section and executed by the motor again. 

## Performance Evaluation 

To compute the area that the PiCar covers, we break down the path it goes. In our strategy, the PiCar goes through three rounds, and the path consists of 11 straight lines and 12 turns. Ideally, each two lines or curves are not overlapped. 

\-    The size of the PiCar is 

\-   The total length of straight lines is 

\-   The sweep area of each turn 

\-   Total estimated sweep area 

\-   Estimated performance 

Therefore, if the PiCar stays in the given area and do the strategy, it can at least achieve 54.9% coverage.

 

## Reference

[1] A Robust Layered Control System for a Mobile Robot, 1985

 

 

 



