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
    port = 'COM8'
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
    model = YOLO('yolov8s.pt')
    cap=cv2.VideoCapture(0) #capture video from webcam
    cap.set(3,img_width)
    cap.set(4,img_height)
    end_time = time.time()
    print('setup done in:',end_time - start_time)

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
    global distance
    global deviation
    results = model(img, stream = True)
    for r in results:
        boxes = r.boxes
        #print(boxes)
        for box in boxes:    
                cls = int(box.cls[0])
                if cls == 77:
                    x1,y1,x2,y2 = box.xyxy [0] #x1 je pozice leveho horniho rohu objektu v ose x, x2 je velikost objektu v ose x v px 
                    x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)#prevedeni hodnot na int pro lepsi praci s nima 
                    confidence = box.conf[0]#jistota modelu 
                    confidence = float(confidence)
                    confidence = round(confidence,2)
                    cv2.rectangle(img, (x1,y1),(x2,y2),(0,255,255),5)
                    distance = img_height-y2
                    center_x = int((x1+x2)/2)
                    center_line = int(img_width/2)# x coordinates of image center
                    deviation = -(center_line-center_x)
                    cv2.line(img, (0,y2),(img_width,y2),(0,255,0), thickness=2)
                    cv2.line(img, (480,540),(480,0),(255,0,0),thickness=2)
                    cv2.line(img, (center_x,540),(center_x,0),(255,0,0),thickness=2)
                    print(distance)
                    print(deviation)
                
                


##################################################################################################################################################### niga       
#comuniction_setup()
camera_setup()
threading.Thread(target = cam_read).start()
time.sleep(10)
sucess, obr = cap.read()
results = model(obr)
print('test done')
time.sleep(1)
distances=[]
deviations=[]
for i in range(15):
    #receve_data()
    use_model()
    cv2.imshow('image',img)
    if distance >100:
        cm_dis = 1.0052*np.exp(0.0117*distance)+35.7412
    if distance <=100:
        cm_dis = 0.15873015873015872*distance + 18.73015873015873
    print("distamce to object:",cm_dis,"cm")
    deviation_angle = np.sin(deviation/(((distance+118)**2 + deviation**2)**0.5)) 
    print("deviation angle:",np.rad2deg(deviation_angle),"°")
    distances.append(distance)
    deviations.append(deviation)
    cv2.waitKey(8000)
    #send_data(1)
print(distances)
print(deviations)
cv2.destroyAllWindows()
