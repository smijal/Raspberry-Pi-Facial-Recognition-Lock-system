import os
import RPi.GPIO as GPIO
import time
from gtts import gTTS
import vlc

#Audio otput function
def say(filename):
    filename = "/home/pi/Desktop/SMART_LOCK_PROJECT/"+filename
    p = vlc.MediaPlayer(filename)
    p.play()

#callback to execute on event trigger (Main menu audio/welcome message)
def my_callback1(ch):
    say("welcome.mp3")
    time.sleep(10)
    
#callback to execute on event trigger (run the main script final.py)
def my_callback2(ch):
    print("ON")
    say("position.mp3") #audio prompt for the user to adjust position and look at the camera 
    try:
        os.system(locker) 
    except:
        say("error.mp3") #error message
    
    
locker = 'python3 /home/pi/Desktop/SMART_LOCK_PROJECT/final.py'
email_sender = ''

#GPIO pins setup
pin = 25
pin_help = 12
print("WELCOME")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_help, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(1,GPIO.OUT)
GPIO.output(1,1)
GPIO.add_event_detect(pin_help, GPIO.RISING, callback=my_callback1, bouncetime=20000)
GPIO.add_event_detect(pin, GPIO.RISING, callback=my_callback2, bouncetime=800)
x = input("keep alive")