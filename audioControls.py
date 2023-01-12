import cv2
import time
import numpy as np
import HandTrackingGlobal as htg
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import pyautogui as p
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os

# camera dimensions
wCam, hCam = 650, 490

videoCap = cv2.VideoCapture(0)
videoCap.set(3, wCam)
videoCap.set(4, hCam)

# print(len(overlayList))

prevTime = 0
currTime = 0

detector = htg.handGesture(detectionCon=0.8,maxHands=1)

# initialization
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()

vol = 0
volumeBar = 400  # 0 volume
volPercentage = 0  # full volume

minVol = volRange[0]
maxVol = volRange[1]

area = 0    
colorVol = (255, 0, 0)

# function to open browser window. This can be cstomized as per the computer screen size
def automate():
    p.click(1016, 1056)
    time.sleep(2)
    p.click(208, 65)
    time.sleep(2)
    p.typewrite("Digital Signal Processing Videos")
    p.press("enter")
    time.sleep(2)
    # print(p.position())
    p.moveTo(558,544)
    p.click(558, 544)
    print("after playing video")
    time.sleep(3)
    p.moveTo(727, 665)
    p.click(727, 665)
    time.sleep(3)

# flag to disable 5 figures action to open browser tab for the second time
videoOn= True

while True:
    success, frm = videoCap.read()
    frm = cv2.flip(frm,2)
    # frm = cv2.resize(frm,(600,500))

    # Find the Hand
    frm = detector.detectHands(frm)
    handLandMarkList,bbox = detector.detectHandPosition(frm, draw=True)  # to remove the drawing set Draw = false

    # Get hand data from the rectangle sub window
    cv2.rectangle(frm, (0,1), (300,500), (0, 0, 255), 0)
    crop_image = frm[1:500, 0:300]

    # if the landmark list is not empty then
    if len(handLandMarkList) != 0:

         # Filter based on size
        wB,hB = bbox[2] - bbox[0],bbox[3] - bbox[1]
        area = (wB * hB) // 100
        fingers = []

        if 100 < area < 1000:

            # Hand range: 7 - 170
            # Find distance between the thumb and index
            length, crop_image, lineInfo = detector.calculateDistance(8, 12, crop_image)

            # volume range of my computeris : 0: -46.76 to 100: 12.0
            volumeBar = np.interp(length, [20, 120], [400, 150])
            # print("volume range:" + str(volumeBar))
            volPercentage = np.interp(length, [20, 120], [0, 100])
            # print(int(length),volumeBar)

            # reduce resolution for smoother transition
            smTransition = 10
            volPercentage = smTransition * round(volPercentage / smTransition)

            # check which finger is up
            fingers = detector.countFingers()
            # print(fingers)

            totalFingers = fingers.count(1)
            # print(totalFingers)   

            # based upon which fingers are up different actions are performed
            if totalFingers==0:
                print("no finger up")
                p.press("space") 
                cv2.putText(crop_image, "Play/Pause", (0, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                # long delay as removing the hand from the frame may take a while
                time.sleep(1)

            if totalFingers==1:
                print(" 1 finger up")
                cv2.putText(crop_image, "Volume Up/Down", (0, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                time.sleep(.25)

            if totalFingers==3 and not fingers[0] and not fingers[4]:
                print("3 fingers up")
                p.press("right")
                cv2.putText(crop_image, "Forward>>", (0, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                time.sleep(.25)

            if totalFingers==4 and not fingers[0]:
                print("4 fingers up")
                p.press("left")
                cv2.putText(crop_image, "<<Backward", (10, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                time.sleep(.25)

            if videoOn and totalFingers== 5:
                print("5 fingers up")
                automate()
                time.sleep(.25)
                videoOn= False

            elif totalFingers==2 and not fingers[0] and not fingers[3] and not fingers[4]:
                print("index and middle fingers up")
                cv2.putText(crop_image, "Volume Up/ Down", (30, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                volume.SetMasterVolumeLevelScalar(volPercentage / 100, None)
                cv2.circle(crop_image, (lineInfo[4], lineInfo[5]), 12, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
                time.sleep(.25)
            else:
                colorVol = (255, 0, 0)

            cv2.rectangle(frm, (150, 370), (300, 490), (0, 0, 255), cv2.FILLED)
            cv2.putText(frm, str(totalFingers), (200, 450), cv2.FONT_HERSHEY_PLAIN,
                        5, (255, 0, 0), 5)
    


    # Drawing the volume bar in the webcam windows
    cv2.rectangle(frm, (50, 150), (80, 400), (0, 255, 0), 2)
    cv2.rectangle(frm, (50, int(volumeBar)), (80, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(frm, f'{int(volPercentage)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN,
                1, (0, 255, 0), 2)
    cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(frm, f'SetVolume: {(int(volPercentage))}', (350, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                colorVol, 2)



    # frame rate shown in the webcam window 
    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(frm, f'FPS: {(int(fps))}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 2)

    cv2.imshow("Image Window", frm)
    cv2.imshow("Cropped Image Window", crop_image)

    key = cv2.waitKey(1)
    if key == 27 or key =='q':
        break

# close/kill all the Microsoft edge windows as well as the webcam window   
os.system("taskkill /im msedge.exe /f")
videoCap.release()
cv2.destroyAllWindows()
