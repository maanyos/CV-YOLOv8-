import cv2
import robomaster
from robomaster import robot
from ultralytics import YOLO

robomaster.config.LOCAL_IP_STR = "192.168.10.2"
tt = robot.Drone()
tt.initialize()

tt_camera = tt.camera
tt_camera.start_video_stream(display=False) #mp4
tt_camera.set_fps("high") #30fps
tt_camera.set_resolution("low") #480p
tt_camera.set_bitrate(6)

model = YOLO('models/default/yolov8m.pt')

while True:
    try:
        frame = tt_camera.read_cv2_image()
    except:
        continue
    result = model.track(source=frame, show=True, persist=True)
    if (cv2.waitKey(1) == 27): # break with escape key
        break

cv2.destroyAllWindows()
tt_camera.stop_video_stream()
tt.close()