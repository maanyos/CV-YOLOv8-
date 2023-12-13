from ultralytics import YOLO
import cv2
import serial
import time 

arduino = serial.Serial(port='COM9', baudrate=9600, timeout=.1) 
model = YOLO('customn.pt')
# model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)

# APU, ATARM, SEATBELT
# OFF, ON
APU = False
ATARM = True
SEATBELT = False

def send_UART(x): 
    # print(x)
	arduino.write(bytes(x, 'utf-8')) 
	time.sleep(0.05) 

while cap.isOpened():
    if (cv2.waitKey(1) == 27):
        break
    success, frame = cap.read()
    if success:
        results = model.track(source=frame, device=0, show=True, persist=True, verbose=False, conf=0.4)
        for r in results:
            try:
                for i in r.boxes.cls.numpy():
                    match int(i):
                        case 0: #APU_OFF
                            if APU == True:
                                APU = False
                                send_UART('d')
                        case 1: #APU_ON
                            if APU == False:
                                APU = True
                                send_UART('c')
                        case 2: #ATARM_OFF
                            if ATARM == True:
                                ATARM = False
                                send_UART('a')
                        case 3: #ATARM_ON
                            if ATARM == False:
                                ATARM = True
                                send_UART('b')
                        case 4: #SEATBELT_OFF
                            if SEATBELT == True:
                                SEATBELT = False
                                send_UART('f')
                        case 5: #SEATBELT_ON
                            if SEATBELT == False:
                                SEATBELT = True
                                send_UART('e')
            except:
                pass
    else:
        break

cap.release()
cv2.destroyAllWindows()

# model = YOLO('yolov8n.pt')
# if __name__ == '__main__':
#     model.train(data='data.yaml', epochs=50, patience=25, device=0)