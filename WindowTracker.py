import cv2
from ultralytics import YOLO
from time import sleep

# represents the ratio of target in frame to switch to ram mode
# larger value means drone switch from pid to ram when closer to target
# between 0 and 1
RAM_THRESHOLD = 0.7

# change the model accordingly to the type of target
model = YOLO('models/default/yolov8m.pt')

# prints the center of bbox
def printBox(box):
    id = box.id.numpy()
    box = box.xyxyn.numpy()
    print(id,
        (box[0][0] + box[0][2]) / 2, 
        (box[0][1] + box[0][3]) / 2)

# extracts bbox of windowId
def filterWindow(results, windowId):
    for result in results:

        # no detections
        if result.boxes is None:
            print('no targets detected')
            return False, False, [0] * 4

        for box in result.boxes:
            # matching target found
            if box.id != None and box.id.numpy()[0] == windowId:
                # printBox(box)
                bbox = box.xywhn.numpy()[0]
                if bbox[2] > RAM_THRESHOLD or bbox[3] > RAM_THRESHOLD:
                    print('preparing to ram')
                    return True, True, bbox
                return True, False, bbox
        # no matching target found
        print('lost track of target')
        return False, False, [0] * 4


# use windowId to determine the drone state:
# -1 for standby,
# >0 for approach window's center, 
# 0 for fly straight ahead at full speed
def trackWindows(frame):
    results = model.track(source=frame, show=True, persist=True, verbose=False)
    return results