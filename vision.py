import cv2
import numpy as np
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

rval, frame = vc.read()
pink = (255, 153, 255)

while True:
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   lower_red = np.array([30,150,50])
   upper_red = np.array([255,255,180])
    
   mask = cv2.inRange(hsv, lower_red, upper_red)
   res = cv2.bitwise_and(frame,frame, mask= mask)

   if frame is not None:
     cv2.imshow("preview", frame)
     cv2.imshow('mask',mask)
     cv2.imshow('res',res)
   rval, frame = vc.read()

   if cv2.waitKey(1) & 0xFF == ord('q'):
     break


#pink 255, 153, 255