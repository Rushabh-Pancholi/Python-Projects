import cv2
import numpy as np
my_colour = [[255,255,255],[0,0,0]]
# color_limit = [[0,146,85,10,255,255]]
color_limit = [[0,201,79,6,255,125]]

myPoints = []

def contour(img_co):
    contur, hierarcy = cv2.findContours(img_co, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = 0,0,0,0
    for cnt in contur:
        area = cv2.contourArea(cnt)
        if area > 300:
            cv2.drawContours(img, cnt, -1, (0, 0, 255), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri , True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y


def findcolor(img):
    
    newPoints=[]
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_limit = np.array(color_limit[0][0:3])
    upper_limit = np.array(color_limit[0][3:6])
    mask = cv2.inRange(img_hsv, lower_limit, upper_limit)
    
    x,y = contour(mask)
    # cv2.circle(img,(x,y),7,my_colour[0],cv2.FILLED)
    
    if x != 0 and y != 0:
        newPoints.append([x,y])
    
    return newPoints


def drawOnCanvas(myPoints):
    for point in myPoints:
        cv2.circle(img, (point[0], point[1]), 7, my_colour[0] , cv2.FILLED)
 
   
framwidth = 640
framheight = 480

cap = cv2.VideoCapture(0)
cap.set(3, framwidth)
cap.set(4, framheight)
cap.set(10, 100)
while True:
    SUCCESS, img = cap.read()
    img_copy = img.copy()
    newPoints = findcolor(img_copy)
    
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
            
    if len(myPoints)!=0:
        drawOnCanvas(myPoints)
    
    flipimg = cv2.flip(img,1,0)
    cv2.imshow('img', flipimg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    