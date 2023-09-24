from ultralytics import YOLO
import numpy as np
import cv2 
import cvzone
from matplotlib import pyplot as plt
import threading
import time
import serial

def comuniction_setup():
    port = 'COM5'
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
    img_height = 480
    img_width = 720
    start_time = time.time() 
    global model
    global cap
    model = YOLO('bearbest.pt')
    cap=cv2.VideoCapture(0) #capture video from webcam
    cap.set(3,img_width)
    cap.set(4,img_height)
    end_time = time.time()
    print('setup done in:',end_time - start_time)

def read_data_fom_cam():
    print('datacomming ja boy')
    print('X=',x1,'Y=',y1,'W=',x2,'H=',y2)



def process_data_fom_cam():
    center_x,center_y = x1+(x2/2),y1+(y2/2)
    distance = img_height-y2
    center_line = int(img_width/2)# x coordinates of image center






def getting_cam_data():
    print('thread started')
    while True:
        sucess, img = cap.read()
        results = model(img, stream = True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
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
        #  break
#####################################################################################################################################################        
camera_setup()
comuniction_setup()
threading.Thread(target=getting_cam_data).start()#args=(5,) vstup do funkce ta carka tam musi bit
send_data(1)#sends command to go thrue esko
receve_data()#waits until its done and 69 comes back 
process_data_fom_cam()