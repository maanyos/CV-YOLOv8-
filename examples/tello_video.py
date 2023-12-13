import cv2
import robomaster
from robomaster import robot

# this is your computer's IP address on the tello's network
robomaster.config.LOCAL_IP_STR = "192.168.10.2"
tt = robot.Drone()
tt.initialize()

tt_camera = tt.camera
tt_camera.start_video_stream(display=False) #mp4
tt_camera.set_fps("high") #30fps
tt_camera.set_resolution("high") #720p
tt_camera.set_bitrate(6)


while True:
    img = tt_camera.read_cv2_image()
    cv2.imshow("Tello", img)
    if (cv2.waitKey(1) == 27): # break with escape key
        break

cv2.destroyAllWindows()
tt_camera.stop_video_stream()

tt.close()