from ultralytics import YOLO
import numpy as np
import cv2 
import cvzone
from matplotlib import pyplot as plt
import threading
import time
import serial
import keyboard

def comuniction_setup():
    port = 'COM6'
    baund_rate = 115200
    global esp
    esp = serial.Serial(port,baund_rate,timeout=1)

def send_data(nunmber):
    command = f"{nunmber}\n"
    esp.write(command.encode('utf-8'))
    print('data send')

def receve_data():
    line =0
    while True:
        line= esp.readline().decode('utf-8').strip()
        print(line)
        if line == '69':
            break
        time.sleep(1)
    print('data reaceved')
##############################################################
def camera_setup():
    global img_width
    global img_height
    img_height = 540
    img_width = 960
    start_time = time.time() 
    global model
    global cap
    model = YOLO('yolov8n.pt')
    cap=cv2.VideoCapture(0) #capture video from webcam
    cap.set(3,img_width)
    cap.set(4,img_height)
    end_time = time.time()
    print('setup done in:',end_time - start_time)

def read_data_fom_cam():
    print('datacomming ja boy')
    print('X=',x1,'Y=',y1,'W=',x2,'H=',y2)

def process_data_fom_cam():
    print(cls)
    if cls >-1:
        center_x,center_y = x1+(x2/2),y1+(y2/2)
        distance = img_height-y2
        center_line = int(img_width/2)# x coordinates of image center
        object_deviation = center_line-center_x
        print("distance",distance,"object deviation ",object_deviation )
        print('X=',x1,'Y=',y1,'W=',x2,'H=',y2)
        #send_data()
        #receve_data()
    if cls ==-1:
        print('no objects found')
        #send_data(2)#sends data to move robot to the next position 
        #receve_data()

def cam_read_test():
    counter = 0
    start_time = time.time() 
    while(counter<60):
        sucess, img = cap.read()
        counter = counter+1
        print(counter)
    end_time = time.time()
    print('in:',end_time - start_time)

def cam_read():
    global img
    while(True):
        sucess, img = cap.read()

def use_model():
    results = model(img, stream = True)
    for r in results:
        boxes = r.boxes
        global cls
        cls = -1
        for box in boxes:    
                cls = int(box.cls[0])
                global x1
                global x2
                global y1
                global y2
                x1,y1,x2,y2 = box.xyxy [0] #x1 je pozice leveho horniho rohu objektu v ose x, x2 je velikost objektu v ose x v px 
                x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)#prevedeni hodnot na int pro lepsi praci s nima 
                #center_x,center_y = x1+(x2/2),y1+(y2/2)#vypocet stredu objektu pro lepsi lokalizaci medveda 
                #center_x,center_y = int(center_x), int(center_y)#prevede hodnoty na int aby se dali pouzit ve funkci ukazujici stred 
                #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)#nakresli box okolo detekovane veci 
                conf = box.conf[0]#jistota modelu 
                conf = float(conf*100)
                rounded_conf = int(conf)#zaokrouhli jistotu modelu na dve desetina mista 

def getting_cam_data():
    print('thread started')
    while True:
        global img
        sucess, img = cap.read()
        results = model(img, stream = True)
        for r in results:
            boxes = r.boxes
            global cls
            cls = -1
            for box in boxes:    
                cls = int(box.cls[0])
                global x1
                global x2
                global y1
                global y2
                x1,y1,x2,y2 = box.xyxy [0] #x1 je pozice leveho horniho rohu objektu v ose x, x2 je velikost objektu v ose x v px 
                x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)#prevedeni hodnot na int pro lepsi praci s nima 
                #center_x,center_y = x1+(x2/2),y1+(y2/2)#vypocet stredu objektu pro lepsi lokalizaci medveda 
                #center_x,center_y = int(center_x), int(center_y)#prevede hodnoty na int aby se dali pouzit ve funkci ukazujici stred 
                #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)#nakresli box okolo detekovane veci 
                conf = box.conf[0]#jistota modelu 
                conf = float(conf*100)
                rounded_conf = int(conf)#zaokrouhli jistotu modelu na dve desetina mista 
                #print('confidence:',rounded_conf)
                #class names 
                #cv2.circle(img, (center_x,center_y),10, (255,0,255), thickness=-1)     
        #cv2.imshow('image',img)
        #key=cv2.waitKey(1)#delay takze to vyhodnocuje jen jeden frame za sekundu pro odlehceni 
        #if key==ord('q'):#pokud se zmackne klavesa q while true se brejkne 
        break
##################################################################################################################################################### niga       
#comuniction_setup()
camera_setup()
threading.Thread(target = cam_read).start()
time.sleep(5)
results = model(img, stream = True)
print('start')
time.sleep(10)
use_model()
process_data_fom_cam()
#start_time = time.time() 
#getting_cam_data()
#end_time = time.time()
#print('setup done in:',end_time - start_time)
#keyboard.wait("s")
#send_data(420)#sends command to go thrue esko
#receve_data()#waits until its done and 69 comes back 
#process_data_fom_cam()
#time.sleep(4)
#send_data(420)#sends command to go thrue esko
#receve_data()#waits until its done and 69 comes back 
#print('program done')
#cv2.imshow('image',img)
#cv2.waitKey(10)#delay takze to vyhodnocuje jen jeden frame za sekundu pro odlehceni 
#cam_read_test()

#todo
#jak se budou cislovat komandy 