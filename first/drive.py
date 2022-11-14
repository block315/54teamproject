#!/usr/bin/env python3

from math import pi, sin, cos, radians
from time import sleep
import pandas as pd
import make_map

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
    from ev3dev2.wheel import Wheel, EV3EducationSetTire
    ev3_in_sim = True

class ev3robot:

    if ev3_in_sim == True:
        robot_tire_diameter = EV3EducationSetTire().diameter_mm
        robot_balance = [1,1]
        robot_width = 120 
    #####config#####
    else:
        robot_tire_diameter = 68.6 # must be accurate (mm)
        robot_balance = [1,1] # left and right motor output has to be same. must be lower than 1
        robot_width = 120 # distance between right wheel and left wheel (mm)
    robot_start_position = [2700,1350,-90] # ev3 starting position for map (mm)
    ################

    def __init__(self, LargeMotor_port_1 = OUTPUT_A, LargeMotor_port_2 = OUTPUT_D, UltrasonicSensor_port = INPUT_3):
        self.ev3_engine = MoveTank(LargeMotor_port_1, LargeMotor_port_2)
        self.ev3_tire = Wheel(self.robot_tire_diameter,36)
        self.ev3_eye = UltrasonicSensor(UltrasonicSensor_port)
        self.ev3_map = pd.read_csv('./arena.csv',header=None)
        self.ev3_position = self.robot_start_position
        self.ev3_map.iloc[round(self.ev3_position[1]/10)-1,round(self.ev3_position[0]/10)-1] = 1

    def ev3_walk(self, robot_direction = "forward", distance = 10, robot_speed = SpeedPercent(50)):
        self.ev3_engine.wait_until_not_moving()
        print("walking :",distance,"cm")
        motor_rotating_amount = (10 * distance) / self.ev3_tire.circumference_mm
        safe_distance = self.ev3_eye.distance_centimeters
        if robot_direction == "forward":
            self.ev3_engine.on_for_rotations(self.robot_balance[0]*robot_speed,self.robot_balance[1]*robot_speed, motor_rotating_amount)
            self.ev3_engine.wait_until_not_moving()
            sleep(1)
            self.ev3_position_update(safe_distance)
        elif robot_direction == "backward":
            self.ev3_engine.on_for_rotations(self.robot_balance[0]* -1 * robot_speed,self.robot_balance[0]* -1 * robot_speed, motor_rotating_amount)
            self.ev3_engine.wait_until_not_moving()
            sleep(1)
            self.ev3_position_update(safe_distance)
            self.ev3_search()

    def ev3_position_update(self, safe_distance):
        sleep(2) # robot slides...
        old_distance = safe_distance
        new_distance = self.ev3_eye.distance_centimeters
        distance = old_distance - new_distance
        self.ev3_position[0] += distance * 10 * sin(radians(self.ev3_position[2]))
        self.ev3_position[1] += distance * 10 * cos(radians(self.ev3_position[2]))
        try:
            self.ev3_map.iloc[round(self.ev3_position[1]/10)-1,round(self.ev3_position[0]/10)-1] = 1
            print("robot position - x :", self.ev3_position[0],"y :",self.ev3_position[1])
        except:
            print("error" + str(self.ev3_position))

    def ev3_turn(self, direction = "left", angle = 90, robot_speed = SpeedPercent(30)):
        self.ev3_engine.wait_until_not_moving()
        print("turning :", angle,"degree")
        motor_rotating_amount = ((self.robot_width * pi * 0.25) / self.ev3_tire.circumference_mm) * angle/90
        if direction ==  "left":
            self.ev3_engine.on_for_rotations(-1 * robot_speed,robot_speed, motor_rotating_amount)
            self.ev3_position[2] -= angle
        elif direction == "right":
            self.ev3_engine.on_for_rotations(robot_speed,-1 * robot_speed, motor_rotating_amount)
            self.ev3_position[2] += angle
        sleep(1)
        self.ev3_search()

    def ev3_search(self):
        self.ev3_engine.wait_until_not_moving()
        barrier_position = [-1,-1]
        barrier_cent_position = [-1,-1]
        safe_distance = self.ev3_eye.distance_centimeters
        print("ultrasonic sensor value :",safe_distance,"cm")
        try:
            barrier_position[0] = self.ev3_position[0] + safe_distance * 10 * sin(radians(self.ev3_position[2]))
            barrier_position[1] = self.ev3_position[1] + safe_distance * 10 * cos(radians(self.ev3_position[2]))
            barrier_cent_position[0] = round(barrier_position[0]/10)
            barrier_cent_position[1] = round(barrier_position[1]/10)
            #self.ev3_map_update(barrier_cent_position[0],barrier_cent_position[1])
            for i in range(10):
                self.ev3_map.iloc[barrier_cent_position[1]-1-i:barrier_cent_position[1]-1+i,barrier_cent_position[0]-1-i:barrier_cent_position[0]-1+i] *=1/1.07
            print("barrier position - x :",barrier_position[0],"y :", barrier_position[1])
        except:
            print('error : map is too small')
        sleep(1)

    def ev3_map_update(self,x,y,area=20,poss=1/1.05):
        x -= 1
        y -= 1
        for i in range(area):
                self.ev3_map.iloc[y-i:y+i,x-i:x+i] *= poss

    
    def ev3_localization(self):
        for i in range(8):
            self.ev3_turn("left",45)

    def export_map(self):
        self.ev3_map.to_csv('arena.csv', encoding='utf-8', index=False, header=False)

    def rotate_to(self,degree):
        while True:
            if degree%360 == self.ev3_position[2]%360:
                break
            else:
                a = (degree%360) - (self.ev3_position[2]%360)
                if (0<= a <=90)or(a<=-270):
                    self.ev3_turn("right",45)
                else:
                    self.ev3_turn("left",45)


    def go_to(self,ax,pos):
        while True:
            if ax == 'x':
                if abs(pos-self.ev3_position[0]) < 100:
                    break
                else:
                    if pos > self.ev3_position[0]:
                        self.rotate_to(90)
                        safe_distance = self.ev3_eye.distance_centimeters
                        if safe_distance > 25:
                            self.ev3_walk()
                            continue
                    elif pos < self.ev3_position[0]:
                        self.rotate_to(-90)
                        safe_distance = self.ev3_eye.distance_centimeters
                        if safe_distance > 25:
                            self.ev3_walk()
                            continue                    
                    self.rotate_to(0)
                    safe_distance = self.ev3_eye.distance_centimeters
                    if safe_distance > 25:
                        self.ev3_walk()
                    else:
                        self.rotate_to(180)
                        self.ev3_walk()
                        
            elif ax == 'y':
                if abs(pos-self.ev3_position[1]) < 100:
                    break
                else:
                    if pos > self.ev3_position[1]:
                        self.rotate_to(0)
                        safe_distance = self.ev3_eye.distance_centimeters
                        if safe_distance > 25:
                            self.ev3_walk()
                            continue
                    elif pos < self.ev3_position[1]:
                        self.rotate_to(180)
                        safe_distance = self.ev3_eye.distance_centimeters
                        if safe_distance > 25:
                            self.ev3_walk()
                            continue                    
                    self.rotate_to(90)
                    safe_distance = self.ev3_eye.distance_centimeters
                    if safe_distance > 25:
                        self.ev3_walk()
                    else:
                        self.rotate_to(270)
                        self.ev3_walk()
            else:
                print("can't find destination")

    def main(self):
        ### robot act code ###
        self.ev3_localization()
        self.go_to("x",1300)
        self.ev3_localization()
        self.go_to("y",200)
        self.ev3_localization()
        ########

if __name__ == '__main__':
    robot_map = make_map.map_for_robot()
    robot_map.make_clean_map()
    ev3active = ev3robot()
    ev3active.main()
    ev3active.export_map()