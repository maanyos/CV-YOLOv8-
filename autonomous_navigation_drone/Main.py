import WindowTracker
import Pid
import robomaster
from robomaster import robot
import cv2
import threading
from queue import LifoQueue
from time import sleep

windowId = -1

requestInput = threading.Event()
userInput = LifoQueue()

def getUserInput():
    def getInput():
        try:
            id = int(input('Enter window ID: '))
            if id >= 0:
                userInput.put(id)
                requestInput.clear()
                print('Approaching window', id)
                return
        except:
            pass
        print('Invalid input: window ID should be int')
        getInput()

    requestInput.set()
    t = threading.Thread(target=getInput)
    t.start()

def setupTello():
    # verify localhost ip
    robomaster.config.LOCAL_IP_STR = "192.168.10.3"
    tt = robot.Drone()
    tt.initialize()

    # setup tello video stream
    tt_camera = tt.camera
    tt_camera.start_video_stream(display=False) #mp4
    tt_camera.set_fps("medium") # high(30fps), medium(??fps), low(??fps)
    tt_camera.set_resolution("low") # high(720p), low(480p)
    tt_camera.set_bitrate(6)
    print('Tello video stream setup successful')

    # setup tello flight control
    tt_flight = tt.flight
    print('Tello flight control setup successful')

    return tt, tt_camera, tt_flight

def run(tt_camera, tt_flight):
    getUserInput()

    while True:
        global windowId
        # read frame and track
        frame = tt_camera.read_cv2_image()
        results = WindowTracker.trackWindows(frame)

        if windowId > 0:
            match, near, bbox = WindowTracker.filterWindow(results, windowId)
            if near is True:
                bbox = [0] * 4
                windowId = 0
            elif match is False:
                bbox = [0] * 4
                windowId = -1


                getUserInput()
                # requestInput.set()
        elif windowId == 0:
            print('Ram mode')
            sleep(3)
            break
        elif windowId == -1:
            if not requestInput.is_set():
                windowId = userInput.get()
        else:
            windowId = -1
            requestInput.set()
            print('Invalid window ID')


        # pid disabled for testing, uncomment these two lines to use pid
        # pid = Pid.pid(windowId, bbox)
        # tt_flight.rc(pid[:])



        # if (cv2.waitKey(1) == 27): # break with escape key
        #     break


if __name__ == "__main__":
    tt, tt_camera, tt_flight = setupTello()

    run(tt_camera, tt_flight)

    tt_camera.stop_video_stream()
    cv2.destroyAllWindows()
    print('Tracker stopped')
    
    tt.close()
    print('End of delivery')