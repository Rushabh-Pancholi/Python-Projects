# in exact same manner we also can detet the face and objects in the image

from operator import pos
import cv2
import mediapipe as mp
from sympy import Circle


def pose_master(img):
    

    mppose  = mp.solutions.pose
    pose = mppose.Pose()
    poseDraw = mp.solutions.drawing_utils
    draw =  poseDraw.DrawingSpec(thickness= 1, circle_radius = 1)
    
    result = pose.process(img)
    
    if result.pose_landmarks:
        # for lm in result.pose_landmarks:
        poseDraw.draw_landmarks(img, result.pose_landmarks, mppose.POSE_CONNECTIONS, draw,draw)
    return img


cap =  cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img = pose_master(img)
    cv2.imshow('result', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
