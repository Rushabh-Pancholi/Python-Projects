import math
from turtle import width
import hand_tracking as ht
import cv2
import numpy as np

import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))



def detection (img):
    
    lmlist = detector.findPosition(img, draw= False)
    if len(lmlist) != 0:
        pt1 = lmlist[4]
        pt2 = lmlist[8]
        ptt1 = pt1[1], pt1[2]
        ptt2 = pt2[1], pt2[2]
        
        cv2.circle(img, ptt1, 6, (255,0,255), -1)
        cv2.circle(img, ptt2, 6, (255,0,255), -1)
        cv2.line(img, ptt1, ptt2, (200,0,200), 2)
        
        mid = (ptt1[0] + ptt2[0])//2, (ptt1[1] + ptt2[1])//2
        
        lenth = math.hypot(ptt1[0] - ptt2[0], ptt1[1] - ptt2[1])
        if lenth < 20 :
            cv2.circle(img, mid, 6, (0,255,0), -1)
            
        elif lenth > 120 :
            cv2.line(img, ptt1, ptt2, (0,0,200), 5)
            
        vol = np.interp(lenth, [20, 120], [-65,0])
        volume.SetMasterVolumeLevel(vol, None)
        

width, height = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = ht.handDetector()

while True:
    sucess , img = cap.read()
    detection(cv2.flip(img, 1, img))
    cv2.imshow('result',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break