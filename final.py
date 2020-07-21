import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import pickle
import RPi.GPIO as GPIO
from time import sleep
import time
from gtts import gTTS
import vlc

#audio output function
def say(filename):
    filename = "/home/pi/Desktop/SMART_LOCK_PROJECT/"+filename
    p = vlc.MediaPlayer(filename)
    p.play()

t0 = time.time()

#GPIO pins setup
pinRed = 23
pinGreen = 24
servoPin = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinRed, GPIO.OUT)
GPIO.output(pinRed,1)
GPIO.setup(pinGreen, GPIO.OUT)
GPIO.output(pinGreen,0)
#Servo setup
GPIO.setup(servoPin, GPIO.OUT)
servo = GPIO.PWM(servoPin, 50)
servo.start(0)
time.sleep(2)
duty=2

#load labels from labels file
with open('/home/pi/Desktop/SMART_LOCK_PROJECT/labels','rb') as f:
    dicti = pickle.load(f)
    f.close()

#camera setup
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640,480))

#face classifier
faceCascade = cv2.CascadeClassifier("/home/pi/Desktop/SMART_LOCK_PROJECT/haarcascade_frontalface_default.xml")
recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.load("/home/pi/Desktop/SMART_LOCK_PROJECT/trainer1.yml") #load trained data instead of training it every time

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    if(time.time()-t0>30): #if time>30 seconds and no face is detected or it is an unknown face, shut down  script
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
    if(len(faces)==0):
        print("No faces detected")
    else:
        voiceName = ""
        for (x,y,w,h) in faces:
            roiGray = gray[y:y+h, x:x+w]
            id_, conf = recognizer.predict(roiGray)
            print("Confidence: " + str(conf))
            for name, value in dicti.items():
                if value == id_:
                    print(name)
                    voiceName = name
                else:
                    print("unknown")
            
            if conf<=63: #if confidence less than 63 unlock the door (less confidence means better)
                GPIO.output(pinRed, 0)
                GPIO.output(pinGreen, 1)
                servo.ChangeDutyCycle(12)
                sleep(0.3)
                say("unlocked.mp3")
                sleep(3)
                say(voiceName+".mp3")
                sleep(10)
                GPIO.output(pinRed, 1)
                GPIO.output(pinGreen, 0)
                servo.ChangeDutyCycle(2)
                sleep(0.3)
                say("locked.mp3")
                sleep(4)
                exit()
            
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key == ord('q'):
        break
    
cv2.destroyAllWindows()
    