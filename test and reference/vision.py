import cv2
import numpy as np
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

rval, frame = vc.read()
pink = (255, 153, 255)

while True:
  #define frame
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  
  #define color range (high and low)
  lower_pink = np.array([140, 50, 50])
  upper_pink = np.array([180, 255, 255])

  #draw frame with only color, black and white
  mask = cv2.inRange(hsv, lower_pink, upper_pink)
  res = cv2.bitwise_and(frame,frame, mask= mask)

  #find color in original frame
  colorcnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

  #draw box around color
  if len(colorcnts) > 0:
      color_area = max(colorcnts, key=cv2.contourArea)
      (xg,yg,wg,hg) = cv2.boundingRect(color_area)
      cv2.rectangle(frame,(xg,yg),(xg+wg, yg+hg),(0,255,0),2)

  #display colors
  if frame is not None:
    cv2.imshow("preview", frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
  rval, frame = vc.read()

  #press q to quit program
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break