import serial
import time 

arduino = serial.Serial(port='COM9', baudrate=9600, timeout=.1) 
def write_read(x): 
	arduino.write(bytes(x, 'utf-8')) 
	time.sleep(0.05) 

while True:
    num = input("Enter a number: ")
    value  = write_read(num)