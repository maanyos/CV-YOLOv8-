import cv2
import robomaster
from robomaster import robot
from time import sleep

# this is your computer's IP address on the tello's network
robomaster.config.LOCAL_IP_STR = "192.168.10.3"
tt = robot.Drone()
tt.initialize()

tt_flight = tt.flight

tt_flight.takeoff().wait_for_completed()

# tt_flight.forward(distance=50).wait_for_completed()
# tt_flight.backward(distance=50).wait_for_completed()

# tt_flight.go(x=100, y=0, z=0, speed=30).wait_for_completed()
# tt_flight.go(x=-100, y=0, z=0, speed=100).wait_for_completed()

# tt_flight.rotate(angle=180).wait_for_completed()
# tt_flight.rotate(angle=-180).wait_for_completed()

tt_flight.rc(a=-10, b=0, c=0, d=10)
sleep(3)
tt_flight.rc(a=0, b=0, c=0, d=0)


tt_flight.land().wait_for_completed()

tt.close()