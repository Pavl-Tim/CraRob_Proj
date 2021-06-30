import threading
import time
from RPi._GPIO import PWM

from time import sleep
from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

D_w = 1
# Pin to relay "Turn On/Off"
On = 13

# Signal Button
signal = 0
# check position
state = 0
next_state = 5

# Positions of servo
pos_servo1 = 6
pos_servo2 = 6

cpu = None
# Detector distance
GPIO_TRIGGER = 15
GPIO_ECHO = 18

# Right motors
b_right1 = 2
b_right2 = 3
f_right1 = 20
f_right2 = 21

# Left motors
b_left1 = 9
b_left2 = 10
f_left2 = 26
f_left1 = 19

distance = 0

lock = threading.Lock()


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(b_right1, GPIO.OUT)
    GPIO.setup(b_right2, GPIO.OUT)
    GPIO.output(b_right1, GPIO.LOW)
    GPIO.output(b_right2, GPIO.LOW)
    GPIO.setup(f_left2, GPIO.OUT)
    GPIO.setup(f_left1, GPIO.OUT)
    GPIO.output(f_left2, GPIO.LOW)
    GPIO.output(f_left1, GPIO.LOW)
    GPIO.setup(b_left1, GPIO.OUT)
    GPIO.setup(b_left2, GPIO.OUT)
    GPIO.output(b_left1, GPIO.LOW)
    GPIO.output(b_left2, GPIO.LOW)
    GPIO.setup(f_right2, GPIO.OUT)
    GPIO.setup(f_right1, GPIO.OUT)
    GPIO.output(f_right2, GPIO.LOW)
    GPIO.output(f_right1, GPIO.LOW)
    GPIO.setup(signal, GPIO.OUT)
    GPIO.output(signal, GPIO.LOW)
def stand_cam():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    p = GPIO.PWM(27, 50)  # type: PWM
    p.start(2.5)
    p.ChangeDutyCycle(7.5)
    time.sleep(0.2)
    GPIO.cleanup(27)
    GPIO.setup(17, GPIO.OUT)
    p = GPIO.PWM(17, 50)  # type: PWM
    p.start(2.5)
    p.ChangeDutyCycle(8.8)
    time.sleep(0.2)
    GPIO.cleanup(17)
stand_cam()
main()

def calculate_distance():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.output(GPIO_TRIGGER, True)

    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    sleep(0.01)
    if D_w == 1:
        return distance




def Forward():
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(2, GPIO.LOW)
    GPIO.output(3, GPIO.HIGH)
    GPIO.output(9, GPIO.LOW)
    GPIO.output(10, GPIO.HIGH)
    GPIO.output(26, GPIO.HIGH)
    GPIO.output(19, GPIO.LOW)
def Back():
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)
    GPIO.output(2, GPIO.HIGH)
    GPIO.output(3, GPIO.LOW)
    GPIO.output(9, GPIO.HIGH)
    GPIO.output(10, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(19, GPIO.HIGH)
def Right():
    GPIO.output(b_right1, GPIO.HIGH)
    GPIO.output(b_right2, GPIO.LOW)
    GPIO.output(f_right1, GPIO.HIGH)
    GPIO.output(f_right2, GPIO.LOW)
    # Left motors start
    GPIO.output(f_left2, GPIO.HIGH)
    GPIO.output(f_left1, GPIO.LOW)
    GPIO.output(b_left1, GPIO.LOW)
    GPIO.output(b_left2, GPIO.HIGH)
def Left():
    GPIO.output(f_left2, GPIO.LOW)
    GPIO.output(f_left1, GPIO.HIGH)
    GPIO.output(b_left1, GPIO.HIGH)
    GPIO.output(b_left2, GPIO.LOW)
    # Right motors start
    GPIO.output(b_right1, GPIO.LOW)
    GPIO.output(b_right2, GPIO.HIGH)
    GPIO.output(f_right1, GPIO.LOW)
    GPIO.output(f_right2, GPIO.HIGH)
def Stop():
    GPIO.output(b_right1, GPIO.LOW)
    GPIO.output(b_right2, GPIO.LOW)
    GPIO.output(f_left2, GPIO.LOW)
    GPIO.output(f_left1, GPIO.LOW)
    GPIO.output(b_left1, GPIO.LOW)
    GPIO.output(b_left2, GPIO.LOW)
    GPIO.output(f_right2, GPIO.LOW)
    GPIO.output(f_right1, GPIO.LOW)


@app.route('/Check')
def check():
    return 'true'


@app.route('/Forward')
def Forward1():
    set_next_state(1)
    return 'data'
@app.route('/Back')
def Back1():
    set_next_state(2)
    return 'data'
@app.route('/Right')
def Right1():
    set_next_state(3)
    return 'data'
@app.route('/Left')
def Left1():
    set_next_state(4)
    return 'data'
@app.route('/Stop')
def Stop1():
    set_next_state(5)
    return 'data'


@app.route('/Distance')
def get_d():
    global D_w
    return str(int(distance))


@app.route('/Status')
def status_server():
    return 'true'

@app.route('/Turn_On')
def Turn_on():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(On, GPIO.OUT)
    GPIO.output(On, GPIO.LOW)
    GPIO.output(On, GPIO.HIGH)
    print("qwe")

    return 'set on'


@app.route('/Turn_Off')
def Turn_off():
    GPIO.cleanup(On)
    return 'set off'


@app.route('/Cam_up')
def Cam_up():
    global pos_servo2
    GPIO.setup(17, GPIO.OUT)
    p = GPIO.PWM(17, 50)  # type: PWM
    p.start(2.5)
    p.ChangeDutyCycle(pos_servo2 - 1)
    time.sleep(0.3)
    GPIO.cleanup(17)
    pos_servo2 = pos_servo2 - 1
    return 'up'
@app.route('/Cam_down')
def Cam_down():
    global pos_servo2
    GPIO.setup(17, GPIO.OUT)
    p = GPIO.PWM(17, 50)  # type: PWM
    p.start(2.5)
    p.ChangeDutyCycle(pos_servo2 + 1)
    time.sleep(0.3)
    GPIO.cleanup(17)
    pos_servo2 = pos_servo2 + 1
    return 'down'
@app.route('/Cam_right')
def Cam_right():
    global pos_servo1
    GPIO.setup(27, GPIO.OUT)
    p = GPIO.PWM(27, 50)  # type: PWM
    p.start(2.5)
    p.ChangeDutyCycle(pos_servo1 - 1)
    time.sleep(0.25)
    GPIO.cleanup(27)
    pos_servo1 = pos_servo1 - 1
    return 'right'
@app.route('/Cam_left')
def Cam_left():
    global pos_servo1
    GPIO.setup(27, GPIO.OUT)
    p = GPIO.PWM(27, 50)  # type: PWM
    p.start(2.5)
    p.ChangeDutyCycle(pos_servo1 + 1)
    time.sleep(0.25)
    GPIO.cleanup(27)
    pos_servo1 = pos_servo1 + 1
    return 'left'


@app.route('/Signal')
def Signal():
    global signal
    GPIO.setup(signal, GPIO.OUT)
    GPIO.output(signal, GPIO.LOW)
    GPIO.output(signal, GPIO.HIGH)
    time.sleep(1)
    GPIO.cleanup(signal)
    return "signal"


@app.route('/Kill_sensor_d')
def KillSensorD():
    global D_w
    D_w = 0
    return 'kill_sen_d'


@app.route('/On_sensor_d')
def OnSensorD():
    global D_w
    D_w = 1
    return "on_sen_d"


# Main Controls

def Fun_Tr():
    global next_state, state

    while True:
        if state == next_state:
            continue

        state = next_state
        if state == 1:
            Forward()
        elif state == 2:
            Back()
        elif state == 3:
            Right()
        elif state == 4:
            Left()
        elif state == 5:
            Stop()


# Write distance to data
def sensor_d():
    global distance
    global D_w
    while True:
        if D_w == 0:
            continue
        else:
            try:
                distance = calculate_distance()
                sleep(0.09)
            except:
                GPIO.cleanup()


# If distance == 35cm get stop and back
def sen_ch_stop():
    global state, next_state
    while True:
        if D_w == 0:
            continue
        if next_state == 2 or next_state == 3 or next_state == 4 or next_state == 5:
            continue
        if distance <= 50:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(signal, GPIO.OUT)
            GPIO.output(signal, GPIO.LOW)
            GPIO.output(signal, GPIO.HIGH)
            time.sleep(0.08)
            GPIO.output(signal, GPIO.LOW)
            time.sleep(0.08)
            GPIO.output(signal, GPIO.HIGH)
            time.sleep(0.08)
            GPIO.output(signal, GPIO.LOW)
            time.sleep(0.08)
            GPIO.output(signal, GPIO.HIGH)
            time.sleep(0.08)
            GPIO.cleanup(signal)
            Back()
            time.sleep(1)
            Stop()
            set_next_state(5)
        time.sleep(0.25)


def set_next_state(value):
    global next_state
    lock.acquire()
    next_state = value
    lock.release()


if __name__ == "__main__":
    # All Treads
    t2 = threading.Thread(target=Fun_Tr, args=[])
    t2.start()
    t3 = threading.Thread(target=sensor_d, args=[])
    t3.start()
    t4 = threading.Thread(target=sen_ch_stop, args=[])
    t4.start()
    app.run(host='192.168.0.36', port='4444')