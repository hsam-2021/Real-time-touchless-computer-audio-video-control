# Real-time-touchless-computer-audio-video-control


## Introduction
This application can control computer audio or video just by using hand gestures that are captured using a webcam. This can be used in music 
stations, music booth etc. and can be integrated with other applications as well.

##  Libraries Used
- numpy
- OpenCV
- mediapipe
- pyautogui 
- pycaw

## Development Summary

• First, I set up the environment and installed all the required libraries and their correct 
  version because sometimes incompatible versions can give a hard time to debug the issue.
  
• After that I worked on the code to implement the above-mentioned functionality.
• Created a module named HandTrackingGlobal which has all the methods related to hand 
  gestures defined.
  
• Then created another python file which implemented HandTrackingGlobal and access the 
  computer’s webcam using OpenCV library.
  
• As soon as the webcam starts capturing two windows open will open. One is the original 
  window and other is the cropped one. Also, the image is flipped to avoid the mirror 
  effect.
  
• The module mediapipe will capture hand if it is in the frame. Also, only 1 hand will be 
  captured and all the landmarks of the hands will be displayed in blue.
  
• Also, there will be a bounding box around the detected hand. The control will take effect 
  only when the bounding box in within that area range i.e., between 100 and 1000
  
• The area is being calculated using the width and height of the bounding box.

• Additionally, the frame rate and number of fingers will be displayed as there are 
  functions written in the HandTrackingGlobal module which are used to do that.
  
• Once the webcam starts then if 5 fingers are shown then a browser tab will open and a 
  video will open up in YouTube. This is implemented using pyautogui library.
  
• Once the video is streaming then based on the hand gestures different video/audio 
  control action would be done.
  
• If all fingers are down then it will pause the video. Again, showing no fingers will play 
  the video.
  
• When index, middle and ring fingers are up then the video will forward.

• When index, middle, ring and pinky fingers are up then the video will backward.

• Volume can be increased and decreased using index and middle fingers. The distance 
  between then will be volume level as it is normalized to range 0-100 which is also shown 
  in the frame as the volume bar.
  
• After all the operation if the user wants to close, he/she can press “Esc” button to close 
  all the browser and webcam windows.
  
• Additionally, I have used a flag which will be disabled after the first time to avoid keep 
  opening new browser tabs every time 5 fingers are shown.
  
## Some Screenshots of the application

* Only one hand will be detected even though both hands are in the frame.

![image](https://user-images.githubusercontent.com/94940146/212205055-9a5deadd-0c75-4b67-b504-44bdc1bf3ebf.png)

* When hand is closed then if the video is playing then it will pause it and vice-versa. 

![image](https://user-images.githubusercontent.com/94940146/212205154-138bb542-b9f0-4a9d-8227-8d5d24597d7d.png)

* When index finger is up then just showing the number of fingers those are up in the frame.
![image](https://user-images.githubusercontent.com/94940146/212205258-607f5f36-4fa3-4b5f-a56a-f64efc52422a.png)

* Increase or decrease the volume in positive correlation with the distance between the index and middle finger.This is done using the distance between the two fingers and normalizing it to be in proportion with the computer’s volume bar levels 0 for muted effect and 100 for full volume.

** A time delay is there so that is user wants to set the volume to a particular level then as it would take a fraction of second to remove finger from the frame. 
Also, to show that the volume is set the SET VOLUME text would turn green.


![image](https://user-images.githubusercontent.com/94940146/212205297-cd3c1b55-6eb1-4dbb-9e04-cceff5f79910.png)

## Future scope

In this project I have covered mainly four major functionalities first is opening a web browser and open some video in YouTube using python library. counting the number of fingers up, second is control the computer/system’s volume and third is control the media player/YouTube control button.

However, this project can be expanded and more gesture and controls can be added which would add more feature. Some examples are capturing facial expressions, Body gestures etc. This is a really interesting field and more and more we explore this we can develop more and more interesting applications.

## References

[Hand tracking module with FPS using OpenCV](https://medium.com/@Nivitus./hand-tracking-module-with-fps-using-opencv-4c9e8928a096)

[Mediapipe: hand gesture-based volume controller in Python w/o GPU](https://medium.com/analytics-vidhya/mediapipe-hand-gesture-based-volume-controller-in-python-w-o-gpu-67db1f30c6ed)

[Murtaza's workshops](https://github.com/murtazahassan/OpenCV-Python-Tutorials-and-Projects)
