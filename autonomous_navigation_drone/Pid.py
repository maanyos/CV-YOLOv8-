import numpy as np

# memory
prev_dest = [0.0, 0.0, 0.0, 0.0]

# Init PID parameters
kp = 0.4
ki = 0.2
kd = 0.1

# Init variables
prev_error_x = 0
prev_error_y = 0
integral_x = 0
integral_y = 0

# init tt
tt = None
tt_flight = None
tt_camera = None

# takes in [x, y, w, h] from destination and calculate the coordinate of the centre
# destination is dynamic xywh
def calculateCentre(destination):
    x, y, width, height = destination
    center_x = x + width / 2
    center_y = y + height / 2
    return center_x, center_y

# drone rotates clockwise - yaw 
def standby():
    print('standby mode')
    # changing yaw
    return [0, 0, 0, 45]

# drone fly forward - pitch
def ramForward():
    print('ram mode')
    # changing pitch
    return [0, 100, 0, 0]

def approachWindow(destination):
    print('approach mode')

    target_x, target_y = calculateCentre(destination)
    frame_center_x = 0.5
    frame_center_y = 0.5

    # calculate error relative to the center of frame
    error_x = target_x - frame_center_x
    error_y = target_y - frame_center_y

    # calculate PID terms
    proportional_x = kp * error_x
    proportional_y = kp * error_y
    integral_x += ki * error_x
    integral_y += ki * error_y
    derivative_x = kd * (error_x - prev_error_x)
    derivative_y = kd * (error_y - prev_error_y)

    # calculate PID output
    pid_output_x = proportional_x + integral_x + derivative_x
    pid_output_y = proportional_y + integral_y + derivative_y

    # limit PID output
    pid_output_x = np.clip(pid_output_x, -100, 100)
    pid_output_y = np.clip(pid_output_y, -100, 100)

    # update preivous error
    prev_error_y = error_x
    prev_error_y = error_y

    # update prev_dest
    prev_dest = destination 

    # roll, pitch, throttle, yaw
    # roll - left / right
    # throttle - up / down
    return [pid_output_x, 50, pid_output_y, 0]

def pid(windowId, destination):
    try: 
        if(windowId > 0):
            return approachWindow(destination)
        elif(windowId == 0):
            return ramForward()
        elif(windowId == -1):
            return standby()
    except Exception as e:
        print("an exception has ocurred: ", e)
        return None