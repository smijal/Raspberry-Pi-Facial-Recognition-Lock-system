# Raspberry Pi Facial Recognition Lock system
#
# Uses OpenCV libraries for face detection, LBPH Face Recognizer. Another options were using EigenFaces, FisherFaces or manually build a model.
# Idea is taken from Muhammad Aqib https://maker.pro/raspberry-pi/projects/how-to-create-a-facial-recognition-door-lock-with-raspberry-pi.
# Some chunks of are code are taken from the original author. 
# Most of the code is edited and adjusted for this project. 
#
# Hardware used: 
# 1. Raspberry Pi - any version (requires audio jack for voice prompts/ can be taken out)
# 2. Raspberry Pi camera module
# 3. Solenoid lock (secure)/Servo (for demonstration) (GPIO PIN 18)
# 4. LEDs (Red=GPIO PIN 23, Green=GPIO PIN 24)
# 5. Push buttons for input ("Help/Main menu switch = GPIO PIN 12, "Unlock/Start recording = GPIO PIN 25)
# 6. Output speaker (Audio jack)
# 7. Additional >=6V power supply for the servo / lock (external)
# 8. Wires 
#
# Scripts description:
# script_executor.py -> script to run on startup, waits for trigger events (GPIO high/ switch press to execute the right command)
# face_detector.py -> creates directories of the autorized person saves pictures of his/her face
# face_recognizer.py -> reads saved images, creates labels for each person/ trains a LBPH model and saves it as a .yml file
# final.p -> loads the trained data/labels , starts the recording and waits for face match, trigers the servo/lock to open for few seconds and close back
# voice_generator.py -> to generate prerecorded messages for audio user prompts
#
# Other ideas and conclusion:
# To be very reliable and actually used as a lock system, needs another option in case facial recognition fails.
# Requires good light for easy face detaction
# Trained model might not be the best, it is always a better option to train own model if possible
# Option to leave a voice mail through email or save in memory is a good feature to have
# I will upload additional code if, I decide to add other things in the future
