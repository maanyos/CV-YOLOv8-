import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)
while cap.isOpened():
    if (cv2.waitKey(1) == 27):
        break
    success, frame = cap.read()
    if success:
        results = model.track(source=frame, device=0, show=True, persist=True, verbose=False, conf=0.2)
        for r in results:
            print(r.boxes.cls.numpy())
        # # send_UART(state)
    else:
        break

cap.release()
cv2.destroyAllWindows()