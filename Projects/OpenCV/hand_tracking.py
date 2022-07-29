import cv2
from cv2 import waitKey
from joblib import PrintTime
import mediapipe as mp
from sqlalchemy import true

# I have created the modul for the hand detection which can be import for diffrent use

class handDetector():
    def __init__(self, mode = False , maxHand = 2 , detectionCon = 0.5 , trackCon = 0.5):
        self.mode = mode
        self.maxHand = maxHand
        self.detectionCon = detectionCon
        self.trackCon = trackCon
    
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands() # if you want to use the differnet parameters then simpely put  8 line here in ()
        self.mpDraw = mp.solutions.drawing_utils  
      
        
    def findHands(self,img):    
 
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        
        if self.result.multi_hand_landmarks:
            for handml in self.result.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handml , self.mpHands.HAND_CONNECTIONS)
                
        return img    


    def findPosition(self,img, handNo = 0 , draw = True):
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        
        lmlist = []
        if self.result.multi_hand_landmarks:
            myHands  =  self.result.multi_hand_landmarks[handNo]
            for id , lm in enumerate(myHands.landmark ):
                h,w,c = img.shape
                cx , cy = int(lm.x * w) , int(lm.y * h)
                lmlist.append([id , cx,cy])
                if draw :
                    cv2.circle(img,(cx,cy),10,(255,0,255),-1)
        return lmlist
                
    

def main():
    
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        
        flip = cv2.flip(img, 1, img)
        
        cv2.imshow('result', flip)
    
        if waitKey(1) & 0xFF == ord('q'):
            break
    
if __name__ == "__main__":
    main()