#!/usr/bin/env python3

from time import sleep
try:
    #for real ev3
    from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
    from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
    from ev3dev2.led import Leds
    from ev3dev2.sound import Sound
    from ev3dev2.motor import LargeMotor, SpeedPercent, MoveTank, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent
    from ev3dev2.wheel import EV3Tire
    from ev3dev2.button import Button
    ev3_in_sim = False
except:
    #for simulator
    from ev3dev2._platform.ev3 import INPUT_1, INPUT_4, INPUT_2, INPUT_3
    from ev3dev2.sensor.lego import UltrasonicSensor
    from ev3dev2.motor import OUTPUT_A, OUTPUT_D, LargeMotor, MoveTank, SpeedPercent
    from ev3dev2.wheel import Wheel, EV3EducationSetTire
    from ev3dev2.led import Leds
    ev3_in_sim = True

if ev3_in_sim == True:
    robot_tire_diameter = EV3EducationSetTire().diameter_mm
    robot_balance = [1,1]
    robot_width = 120 
    #####config#####

else:
    robot_tire_diameter = 68.6 # must be accurate (mm)
    robot_balance = [1,1] # left and right motor output has to be same. must be lower than 1
    robot_width = 120 # distance between right wheel and left wheel (mm)
rotate_speed = SpeedPercent(50)
small = False


# init process
ev3_engine = MoveTank(OUTPUT_A, OUTPUT_D)
ev3_tire = Wheel(robot_tire_diameter,36)
ev3_eye = UltrasonicSensor(INPUT_3)
ev3_command = []

if ev3_in_sim == False:
    btn = Button()
my_leds = Leds()
# Do something when state of any button changes:


def fin():
    ev3_engine.wait_until_not_moving()
    sleep(1)
    my_leds.set_color('LEFT', 'GREEN')

def left(state):
    my_leds.set_color('LEFT', 'RED')
    if state:
        print('Left button pressed')
        sleep(1)
        ev3_engine.on_for_seconds(-1*robot_balance[0]*rotate_speed,robot_balance[1]*rotate_speed,1)
        ev3_command.append("left")
    else:
        print('Left button released')
    fin()

def right(state):
    my_leds.set_color('LEFT', 'RED')
    if state:
        print('right button pressed')
        sleep(1)
        ev3_engine.on_for_seconds(robot_balance[0]*rotate_speed,-1*robot_balance[1]*rotate_speed,1)
        ev3_command.append("right")
    else:
        print('right button released')
    fin()
    
def up(state):
    my_leds.set_color('LEFT', 'RED')
    if state:
        print('up button pressed')
        sleep(1)
        ev3_engine.on_for_seconds(robot_balance[0]*rotate_speed,robot_balance[1]*rotate_speed,1)
        ev3_command.append("up")
    else:
        print('up button released')
    fin()
    
def down(state):
    my_leds.set_color('LEFT', 'RED')
    if state:
        print('down button pressed')
        sleep(1)
        ev3_engine.on_for_seconds(-1*robot_balance[0]*rotate_speed,-1*robot_balance[1]*rotate_speed,1)
        ev3_command.append("down")
    else:
        print('down button released')
    fin()
    
def enter(state):
    global rotate_speed,small
    if state:
        print('enter button pressed')
        if small == False:
            rotate_speed = rotate_speed * 0.5
            my_leds.set_color('RIGHT', 'AMBER')
            small = True
        else:
            rotate_speed = rotate_speed*2
            my_leds.set_color('RIGHT', 'AMBER')
            small = False
        ev3_command.append("enter")
    else:
        print('enter button released')


f = open("./ev3command", 'r')
while True:
    line = f.readline()
    if not line: break
    print(line)
    if line == "left\n":
        left(True)
    elif line == "right\n":
        right(True)
    elif line == "up\n":
        up(True)
    elif line == "down\n":
        down(True)
    elif line == "enter\n":
        enter(True)
f.close()