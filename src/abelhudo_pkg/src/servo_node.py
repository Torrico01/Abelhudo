#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2009, Tictor's Lab, Inc.
# All rights reserved.

""" Codigo teorico independente da GPIO do Raspberry, apenas trabalhando com ROS"""

import sys
import math
import rospy
import time as delay
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

from servo import Servo

# Pinos
#servoPIN = 3

class ServoProp():
    def __init__(self,
            gpio_signal,
            ):

        self.servo_array = []

        rospy.loginfo("Iniciando servo...")
        servo = Servo(gpio_signal)
        self.servo_array.append(servo)
        rospy.loginfo("Servo configurado!")

    def angulo(self, angle):
        # From 0 to 90
        self.servo_array[0].set_angle(angle)
        rospy.loginfo("Servo setado com %s graus" % angle)

    def run(self):
        #--- Set the control rate
        rate = rospy.Rate(0.25)

        rospy.loginfo("Servo operando...")
        ang = 45
        while not rospy.is_shutdown():
            self.angulo(1)
            self.angulo(89)
            rate.sleep()
        GPIO.cleanup()
        rospy.loginfo("Interrompido.")

if __name__ == '__main__':
    rospy.loginfo("Iniciando node do servo...")
    rospy.init_node("node_test")
    servo_array = ServoProp(gpio_signal = servoPIN)
    servo_array.run()
