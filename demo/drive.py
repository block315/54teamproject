#!/usr/bin/env python3

'''ev3dev 가 작동하는지 확인'''
from time import sleep
from ev3dev2.motor import LargeMotor, SpeedPercent, MoveTank, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

# robot speaking test : tts "hello world!"
speaking = Sound()
speaking.speak('Hello world')

# robot moving test : 2 sec forward
moving = MoveTank(OUTPUT_A, OUTPUT_B)
moving.on_for_seconds(10,10,2)

# robot sensing test : touch, color, distance
touching = TouchSensor(INPUT_1)
color_checking = ColorSensor(INPUT_2)
dist_checking = UltrasonicSensor(INPUT_3)
leds = Leds()

while True:
    if touching.is_pressed:
        leds.set_color("LEFT", "GREEN")
        leds.set_color("RIGHT", "GREEN")
    elif color_checking.color == ColorSensor.COLOR_BLACK:
        leds.set_color("LEFT", "BLACK")
        leds.set_color("RIGHT", "BLACK")
    elif dist_checking.distance_centimeters < 3.5:
        leds.set_color("LEFT","ORANGE")
        leds.set_color("RIGHT","ORANGE")
    else:
        leds.set_color("LEFT", "RED")
        leds.set_color("RIGHT", "RED")
    # don't let this loop use 100% CPU
    sleep(0.01)

