import numpy as np
import cv2

import time


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def empty(a):
    pass

while True:
    time.sleep(3)
    _, background = cap.read()
    break

cv2.namedWindow('TrackBar')
cv2.resizeWindow('TrackBar', 640, 240)

cv2.createTrackbar('Hue Min', 'TrackBar', 50, 179, empty)
cv2.createTrackbar('Hue Max', 'TrackBar', 136, 179, empty)
cv2.createTrackbar('Sat Min', 'TrackBar', 104,  255, empty)
cv2.createTrackbar('Sat Max', 'TrackBar', 255,  255, empty)
cv2.createTrackbar('Val Min', 'TrackBar', 46,  255, empty)
cv2.createTrackbar('Val Max', 'TrackBar', 255,  255, empty)

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

while True:
    # success, img = cap.read()
    ret, img = cap.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos('Hue Min', 'TrackBar')
    h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
    S_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
    S_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
    V_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
    V_max = cv2.getTrackbarPos('Val Max', 'TrackBar')
    img = cv2.GaussianBlur(img, (5, 5), 0)
    lower = np.array([h_min, S_min, V_min])
    upper = np.array([h_max, S_max, V_max])
    
    mask = cv2.inRange(imgHSV, lower, upper)
    kernel = np.ones((3, 3), np.uint8) 

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)    
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    with_Blue = cv2.bitwise_and(img, img, mask = mask)
    
    img_back = cv2.bitwise_not(with_Blue)
    
    img = cv2.bitwise_and(img_back, img)

    without_Blue = cv2.bitwise_and(background, background, mask = mask)

    img_new = cv2.bitwise_or(img, without_Blue)
    
    cv2.imshow('stacked Images', img_new)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break