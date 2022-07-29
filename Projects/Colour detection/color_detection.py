import pandas as pd
import numpy as np
import argparse
import cv2

clicked = False
r = g = b = xpos = ypos =0

# taking image from the desktop or user
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image',required=True, help='image path')
args = vars(ap.parse_args())
img_path = args['image']

# Reading image with opencv
img = cv2.imread(img_path)

# Reading csv file from path with pandas
index = ['colour','colour_name','hex','r','g','b']
data = pd.read_csv("G:\python\colour detection\colors.csv",names=index,header=None)

# here is the dr = draw function

def dr(event,x, y,flags,params):
    if event == cv2.EVENT_LBUTTONUP:
        global b,g,r,xpos, ypos,clicked
        clicked= True
        xpos= x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

# creat mouse callback event on a windows
cv2.namedWindow('image')
cv2.setMouseCallback('image',dr )
            
# get colour name
def get_colour_name(r,g,b):
    minimum = 10000
    for i in range(len(data)):
        d = abs(r-int(data.loc[i,'r'])) + abs(g-int(data.loc[i,'g'])) + abs(b-int(data.loc[i,'b']))
        if(d <= minimum):
            minimum=d
            cname=data.loc[i,'colour_name']
    return cname

# display image on the widows and granting the permissio for the showing results
while (1):
    cv2.imshow('image', img)
    if (clicked):
        cv2.rectangle(img,(20,20),(750,60),(b,g, r),-1)
        text = get_colour_name(r,g,b) + '  R =' + str(r) + '  G =' + str(g) + '  B =' + str(b)
        cv2.putText(img,text,(50,50),2,0.7,(255,255,255),1,cv2.LINE_AA)
        if (r+g+b>=600):
            cv2.putText(img,text,(50,50),2,0.7,(0,0,0),1,cv2.LINE_AA)
    if cv2.waitKey(20) & 0xFF == 27 :
        break
    
cv2.destroyAllWindows()