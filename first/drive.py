#!/usr/bin/env python3

from math import pi, sin, cos, tan, radians
from time import sleep
import pandas as pd
import generate_map as generate_map
try:
    #for real ev3
    from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
    from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
    from ev3dev2.led import Leds
    from ev3dev2.sound import Sound
    from ev3dev2.motor import LargeMotor, SpeedPercent, MoveTank, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent
    from ev3dev2.wheel import EV3Tire
    ev3_in_sim = False
except:
    #for simulator
    from ev3dev2._platform.ev3 import INPUT_1, INPUT_4, INPUT_2, INPUT_3
    from ev3dev2.sensor.lego import UltrasonicSensor
    from ev3dev2.motor import OUTPUT_A, OUTPUT_D, LargeMotor, MoveTank, SpeedPercent
    from ev3dev2.wheel import EV3Tire, EV3EducationSetTire
    ev3_in_sim = True

class ev3robot:
    
    step = 10 # cm
    robot_width = 120 # distance between right wheel and left wheel

    def __init__(self, LargeMotor_port_1 = OUTPUT_A, LargeMotor_port_2 = OUTPUT_D, UltrasonicSensor_port = INPUT_3):
        self.ev3_engine = MoveTank(LargeMotor_port_1, LargeMotor_port_2)
        self.ev3_tire = EV3EducationSetTire()
        self.ev3_eye = UltrasonicSensor(UltrasonicSensor_port)
        self.ev3_map = pd.read_csv('./arena.csv',header=None)
        self.ev3_position = [2700,1300,-90]

    def ev3_walk(self, robot_direction = "forward", distance = step*10, robot_speed = SpeedPercent(50)):
        motor_rotating_amount = (self.step / self.ev3_tire.circumference_mm)*distance
        if robot_direction == "forward":
            self.ev3_engine.on_for_rotations(robot_speed,robot_speed, motor_rotating_amount)
            self.ev3_position_update(distance)
        elif robot_direction == "backward":
            self.ev3_engine.on_for_rotations(-1 * robot_speed,-1 * robot_speed, motor_rotating_amount)
            self.ev3_position_update(-1*distance)
        self.ev3_engine.wait_until_not_moving()

    def ev3_run(self, robot_direction, distance, robot_speed = SpeedPercent(50)):
        # just run without cross-checking the robot position.
        pass

    def ev3_position_update(self, distance):
        self.ev3_position[0] += distance * sin(radians(self.ev3_position[2]))
        self.ev3_position[1] += distance * cos(radians(self.ev3_position[2]))

    def ev3_turn(self, direction = "left", angle = 90, robot_speed = SpeedPercent(50)):
        motor_rotating_amount = ((self.robot_width * pi * 0.25) / self.ev3_tire.circumference_mm) * angle/90
        if direction ==  "left":
            self.ev3_engine.on_for_rotations(-1 * robot_speed,robot_speed, motor_rotating_amount)
            self.ev3_position[2] -= angle
        elif direction == "right":
            self.ev3_engine.on_for_rotations(robot_speed,-1 * robot_speed, motor_rotating_amount)
            self.ev3_position[2] += angle
        self.ev3_engine.wait_until_not_moving()
    
    def ev3_search(self):
        barrier_position = [-1,-1]
        safe_distance = self.ev3_eye.distance_centimeters*10
        try:
            barrier_position[0] = self.ev3_position[0] + safe_distance * sin(radians(self.ev3_position[2]))
            barrier_position[1] = self.ev3_position[1] + safe_distance * cos(radians(self.ev3_position[2]))
            self.ev3_map.iloc[round(barrier_position[1]/10)-1,round(barrier_position[0]/10)-1] = 0
            print((round(barrier_position[0]/10)-1)*10, (round(barrier_position[1]/10)-1)*10)
        except:
            pass

    def main(self):
        #robot code goes here
        self.ev3_search()
        for i in range(7):
            self.ev3_turn("left",45)
            sleep(1)
            self.ev3_search()
        self.ev3_map.to_csv('arena.csv', encoding='utf-8', index=False, header=False)


if __name__ == '__main__':
    generate_map.making_map()
    ev3robot = ev3robot()
    ev3robot.main()