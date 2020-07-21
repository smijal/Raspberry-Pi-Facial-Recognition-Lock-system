import numpy as np
import cv2
import os
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import time

############Camera setup######################
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640,480))
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

########Directory creation####################
name = input("Enter name: >")
dirName = "./images/" + name
print(dirName)
if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory " + dirName + " created")
else:
    print("Name already exists")
    print("Exiting...")
    sys.exit()
####################Detect Face function###############################
def detectFace(frame, count):
    if count > 89: #takes 90 pictures of a person
        return -1
    frame = frame.array 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
    for(x,y,w,h) in faces:
        roiGray = gray[y:y+h, x:x+w]
        filename = dirName + "/" + name + str(count) + ".jpg"
        cv2.imwrite(filename, roiGray)
        cv2.imshow("face", roiGray) #show detected face
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        count+=1
    cv2.imshow('frame', frame) #show every frame
    return count
###################################################
count = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    count=detectFace(frame,count) #for every frame detect face
    if(count==-1):
        break
    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key==ord('q'):
        break
cv2.destroyAllWindows()
    




