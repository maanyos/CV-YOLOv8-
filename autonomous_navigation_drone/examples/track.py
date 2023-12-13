from ultralytics import YOLO
import cv2

model = YOLO('models/default/yolov8m.pt')


# method 1: track with stream=false is easier to use but accumulates RAM
# exit by pressing Q
model.track(source='https://youtu.be/Zgi9g1ksQHc', show=True)


# # method 2: track with stream=true needs a few more lines 
# # but does not accumulate RAM and allows more configuring
# # exit by pressing ESC
# for result in model.track(source='https://youtu.be/Zgi9g1ksQHc', stream=True):
#     cv2.imshow('ESC to quit', result.plot())
#     if cv2.waitKey(1) == 27: # break with ESC key
#         break
# cv2.destroyAllWindows()