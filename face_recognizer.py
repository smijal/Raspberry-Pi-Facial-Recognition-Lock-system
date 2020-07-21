import os
import numpy as np
from PIL import Image
import cv2
import pickle

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer1 = cv2.face.createLBPHFaceRecognizer()

baseDir = os.path.dirname(os.path.abspath(__file__))
imageDir = os.path.join(baseDir,"images")

###############Convert image to numpy array else return empty array#########################
def convertNumpy(file, currentId, labelIds):
    print(file)
    if file.endswith("jpg"):
        path = os.path.join(root,file)
        label = os.path.basename(root)
        print(label)
        if not label in labelIds:
            labelIds[label] = currentId
            print(labelIds)
            currentId+=1
        id_ = labelIds[label]
        pilImage = Image.open(path).convert("L")
        imageArray = np.array(pilImage, "uint8")
        return imageArray, currentId, id_
    else:
        return np.array([]), currentId, id_
        
#############################################
currentId = 1
labelIds = {}
yLabels = []
xTrain = []

#perform an os walk and convert all the images to numpyArray, save the labels
for root, dirs, files in os.walk(imageDir):
    print(root, dirs, files)
    for file in files:
        imageArray, currentId, id_=convertNumpy(file, currentId, labelIds)
        if(imageArray.size!=0):
            faces = faceCascade.detectMultiScale(imageArray,scaleFactor = 1.1, minNeighbors=5)
            for(x,y,w,h) in faces:
                roi = imageArray[y:y+h, x:x+w]
                xTrain.append(roi)
                yLabels.append(id_)
with open("labels","wb") as f:
    pickle.dump(labelIds, f)
    f.close()

recognizer1.train(xTrain, np.array(yLabels)) #train the recognizer with the trainData and labels
recognizer1.save("trainer1.yml") #save as .yml file

print(labelIds)

