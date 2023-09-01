#imports 
from ultralytics import YOLO
import numpy as np
import cv2 
import cvzone
import time
import matplotlib.pyplot as plt
import keyboard

#loads coco.names into list classNames 
classesfile='coco.names'
classNames=[]
with open(classesfile,'rt') as f:
    classNames=f.read().rstrip('\n').split('\n')
print('Classes loaded successfully!')

searched_object = 'pottedplant' #name of object I want to find
object_id = classNames.index(searched_object)# gets id of the object I want to find  
print(object_id)

model = YOLO('yolov8n.pt')#loads the model 


def image_capture():
    #capturing image
    cap = cv2.VideoCapture(0)#inicialize camera 
    cap.set(3,640)#img width
    cap.set(4,480)#img height
    sucess, img = cap.read()#reads frame from camera 
    img_height,img_width,img_channels = img.shape# gets some info 
    print('width',img_width,'Px')#width
    print('height',img_height,'Px')#height 
    print('channels',img_channels)#colour channels 

def model_apply():
    results = model(img)#applies model on the image 
    objects_ids = []#list for ids of found objects 
    objects_centers = []#list for objects centers 
    objects_heights = []# list for objects height, used for calculating distance of the objects 
    for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])#gets the object id 
                print(classNames[cls])#prints the object class 
                print(cls) #prints the object id 
                #bounding boxes
                x1,y1,x2,y2 = box.xyxy [0] #x1 je pozice leveho horniho rohu objektu v ose x, x2 je velikost objektu v ose x v px 
                x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)#prevedeni hodnot na int pro lepsi praci s nima 
                print('X=',x1,'Y=',y1,'W=',x2,'H=',y2)#vypisuje velikost objektu a jeho polohu v px 
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)#nakresli box okolo detekovane veci 
                #object center 
                center_x,center_y = x1+(x2/2),y1+(y2/2)#vypocet stredu objektu pro lepsi lokalizaci medveda 
                center_x,center_y = int(center_x-x1/2), int(center_y-y1/2)#prevede hodnoty na int aby se dali pouzit ve funkci ukazujici stred 
                center = center_x,center_y
                print('center:',center_x,center_y)#vypise udaje 
                cv2.circle(img, (center_x,center_y),10, (255,0,255), thickness=-1)
                #model confidence
                conf = box.conf[0]#jistota modelu 
                conf = float(conf*100)
                rounded_conf = int(conf)#zaokrouhli jistotu modelu na dve desetina mista 
                print('confidence:',rounded_conf)
                #box on bounding box s nazvem claasy a confidence modelu 
                cvzone.putTextRect(img, f'{classNames[cls]}{rounded_conf}',(max(0,x1), max(35,y1)))#vykresli nazev classy objektu spolecne s confidence do videa 
                objects_ids.append(cls)#zapisovani hodnot do listu
                objects_centers.append(center)#zapisovani hodnot do listu
                objects_heights.append(y2)
    cv2.line(img,(int(img_width/2),0),(int(img_width/2),img_height),(255,0,255),thickness=2 )#vykresli na video primku stredem videa 
    print(objects_ids)
    print(objects_centers)
    print(objects_heights)
 
keyboard.add_hotkey('s',image_capture)
keyboard.wait('s')
model_apply()

