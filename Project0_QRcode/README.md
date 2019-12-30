# Project 0: Perception using QR code

## Objective

The objective of this exercise is to use the on-board camera to drive to
speciﬁc locations in your environment. Using feedback from the detected
landmarks you should be able to improve your localization performance and
through this drive more eﬀectively. The general structure of the anticipated
system is shown below.

<img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project0_QRcode/pic/objective.png" alt="layout" width="375" />

We will use QR markers as landmarks. A number of unique QR codes
was uploaded with the homework description. The tasks are

1. Drive to position (1,0,0) place a QR marker at an appropriate location
to assist with localization
2. Continue onwards to location (1,2,π) again with the assistance of QR
markers for localization
3. Return to location (0,0,0).
4. For each position estimate your localization error



## Algorithms

### Concept

   In this assignment, I break down the whole process into three parts, which represent three paths from the start point to the destination. The main control strategy is to let the PiCar detect QR code as many times as possible so that it could tell where it is and update its position during most of the time. 

### QR code Placement

<img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project0_QRcode/pic/Map.png" alt="layout" width="375" />

 From the map below, each QR code is placed near the target point and face different directions. They are all about 50~60 cm away from the point since I found that this is the minimal distance that ensures the normal operation of the camera. Except for the first QR code, the rest of them are placed parallel to the desired direction. The thought is to guide the PiCar drive to a suitable spot for making a turn.

<img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project0_QRcode/pic/environ.png" alt="layout" width="375" />

 

### Solutions

   In general, while going through each path, the PiCar would process following commands to complete the task:

1)  Calculate the displacement between the target and the current position.

2)  Derive the motor command through the info and drive.

3)  Stop. Detect the QR code to update the information between the PiCar and QR code. 

4)  If QR code isn’t in the middle of the screen, adjust the car position.

5)  Derive the QR code information again and get to a suitable position for turning into the target point.

6)  Make a turn and reach the point.

   For a specific path, the process might change. Take the path 3 (from (1,2, pi) to the origin point) as an example, since that I place two QR codes on this path, the PiCar could update the information from different sources.

### Function Design

   There are several functions in this assignment, which are basically for vision and motion. While designing algorithms, I have encountered some specific problems and come up with some of these functions below:

#### Q1: What to do when the PiCar should detect QR code but it cannot see any of it?

**Function *QR_Find_Detect* **

   The reasons that PiCar can’t detect are either too far/close/left/right, and therefore the first action I take is to go backward and scan again. If it’s not working, turn left or right a bit and check again. Repeat the whole process if it fails again.

#### Q2: The PiCar can detect QR code, but the information isn’t continuous.

**Function *QR_DistanceDetect* **

   As I collect the data from zbar.decode(), it turns out that even put the QR code in a perfect distance, the data would mix with plenty of blanks into it and cause trouble while processing on other functions. 

   To solve this problem, I choose to output the data every given period of time instead of output instantaneously. On each collected data, I choose the mode of it and set it as the output. Also, if the blank(presented as ‘0’ in data) is the mode, it would be selected if the time it appears in the data is bigger than half of the data size. By doing this, I can stabilize the output of detection.

#### Q3: The QR code icon is not in the middle of the camera

**Function *LR_Cali* ** 

  To let the PiCar face the QR code more accurate, the first move is to go backward, turn a bit left, and check what the QR code is. And do it again for the right turn. Since the displacement in the view is sensitive to the movements, each move is slower compared to other commands.

 

##   Achieved Results and Discussion

### Demo

<img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project0_QRcode/pic/QR.gif" alt="layout" width="540" />

### Description and Discussion:

1)  As shown below, this sketch shows the path the PiCar goes. The final path, which is the brown dashed line in the graph, is like a rectangle shape. I set the QR codes on each corner of the rectangle so that the only task the PiCar does is to keep the assigned distance with signs and make a turn on suitable timing. The four red circles in the graph is the time when the PiCar makes a turn.

<img src="https://github.com/coldhenry/PiCar_Robotics/blob/master/Project0_QRcode/pic/Picture1.png" alt="layout" width="540" />

2)  Whenever the PiCar meets a new sign, the first thing is to make sure the sign is in the middle of the view. By doing this, it won’t get lost with the direction and keep updating the information.

3)  Compared to the last assignment, the performance of the PiCar improves a lot. The distance error between the sign and the car is always no more than 5 cm. And since that the car can keep the distance with a sign. It can easily make a turn and change the orientation while reaching the point.

4)  As mentioned in the last assignment, there are plenty of hardware issues, such as the loose assembly on the wheel and sticks, that could result in great error even on walking a straight line. However, this problem can be solved this time since we could see the road. Therefore, it takes less effort to calibrate the angle of servo just to make it walk on lines.

5)  The problems that remain are the accurate pose estimation between the camera and the QR code. I have tried to implement the algorithms regarding this issue. (using intrinsic matrix, rotation and translation matrix and compute with OpenCV solvePnP function). But the problem is that the code runs so slowly that I can’t implement it into my main program. Besides, the performance of the PiCar without this technique works fairly well, so I might revise my code and implement it in the next assignment.

​    

 

 

 

 