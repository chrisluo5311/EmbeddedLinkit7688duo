import serial
import time

def setup():
    global s
    s = serial.Serial("COM8",9600)

def loop():
    s.write(1)
    time.sleep(1)

    s.write("0")
    time.sleep(1)

if __name__ == '__main__':
    setup()
    while True:
        loop()