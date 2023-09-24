from ultralytics import YOLO
import numpy as np
import cv2 
import cvzone
import time
import matplotlib.pyplot as plt
import keyboard
import math

global cap
cap = cv2.VideoCapture(0)#inicialize camera 
cap.set(3,640)#img width
cap.set(4,480)#img height


def LoadImageStorage(image):
    global img 
    img = cv2.imread(image)#loads the picture into variable 
    global img_height
    global img_width
    global img_channels
    img_height,img_width,img_channels = img.shape# gets some info from given picture
    print('image load sucess')

def LoadImageCamera():
    global img
    sucess, img = cap.read()#reads frame from camera
    global img_height
    global img_width
    global img_channels 
    img_height,img_width,img_channels = img.shape# gets some info 
    print('image load sucess')

def UseModel(image,model):
    global objects_centers
    global objects_ids
    global distances
    objects_ids = []#list for ids of found objects 
    objects_centers = []#list for objects centers 
    distances = []
    results = model(image)#applies model on the image 
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if cls ==0:
                print(cls)
                x1,y1,x2,y2 = box.xyxy [0] #x1 je pozice leveho horniho rohu objektu v ose x, x2 je velikost objektu v ose x v px 
                x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)#prevedeni hodnot na int pro lepsi praci s nima 
                print('X=',x1,'Y=',y1,'W=',x2,'H=',y2)#vypisuje velikost objektu a jeho polohu v px 
                center_x,center_y = x1+(x2/2),y1+(y2/2)#vypocet stredu objektu pro lepsi lokalizaci medveda 
                center_x,center_y = int(center_x-x1/2), int(center_y-y1/2)#prevede hodnoty na int aby se dali pouzit ve funkci ukazujici stred 
                center = center_x,center_y
                print('center:',center_x,center_y)#vypise udaje 
                conf = box.conf[0]#jistota modelu 
                conf = float(conf*100)
                rounded_conf = int(conf)#zaokrouhli jistotu modelu na dve desetina mista 
                print('confidence:',rounded_conf)
                objects_ids.append(cls)#zapisovani hodnot do listu
                objects_centers.append(center)#zapisovani hodnot do listu
                distance = img_height-y2
                print(distance)
                distances.append(distance)
          

def ProcesData():
    a = objects_ids.index(0)#in list object_ids search for specific number and returns index of the number
    print(a)#prints the index 
    x,y=objects_centers[0]#in list finds values for given index
    print('object centers:',x,y)#prints the values 
    center_line = int(img_width/2)# x coordinates of image center
    object_deviation = center_line-x # deviation of object from center of the screen 
    print('deviation = ',object_deviation) 
    #measuring distances 
    d=distances[a] # for given index finds distance of the object in px 
    print(d) # prints object distance in px
    #calculator from px to cm 
    #if distance in px is larger than 240 px use this equation
    if d>240:
        distance_cm = 0.001894930772332081 * (d- 62.49315340028377 )**2+ 41.845975945942605
    #if distance in px is smaller than 240 px use this equation
    if d<240:
        distance_cm = np.exp( 3.486047002894599 )*np.exp(0.0045*d)
    print('distance:',distance_cm,'cm')# prints the value in cm
    #angle calculating 
    angle = math.atan(object_deviation/d)
    print(np.rad2deg(angle),'°')
    #way lenght 
    w = distance_cm/(math.cos(abs(angle)))
    print('distance to target:',w,'cm')


model = YOLO('bearbest.pt')#loads the model 
LoadImageStorage('test3.png')
UseModel(img,model)
ProcesData()
print('finished')
