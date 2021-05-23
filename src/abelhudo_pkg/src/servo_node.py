#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2009, Tictor's Lab, Inc.
# All rights reserved.

""" Codigo teorico independente da GPIO do Raspberry, apenas trabalhando com ROS"""

# Importando Bibliotecas
import sys
import math
import rospy
import time as delay
import RPi.GPIO as GPIO
# Importando Mensagens ROS
from abelhudo_pkg.msg import Servo_msg
# Importando GPIO Local
from servo import Servo

# Desabilita Avisos da GPIO
GPIO.setwarnings(False)

# Variaveis Globais
angle = -1

''' CALLBACKS '''
def callback_servo(data):
    global angle
    angle = data.angle


class ServoProp():
    def __init__(self,
            gpio_signal,
            ):

        self.servo_array = []

        rospy.loginfo("Iniciando servo...")
        servo = Servo(gpio_signal)
        self.servo_array.append(servo)
        rospy.loginfo("Servo configurado!")

        # Subscribers
        rospy.Subscriber("/Abelhudo/Servo", Servo_msg, callback_servo)

    def angulo(self, angle):
        # From 0 to 90
        self.servo_array[0].set_angle(angle)
        rospy.loginfo("Servo setado com %s graus" % angle)

    def subscriber(self):
        global angle
        while angle < 0:
            pass
        self.servo_array[0].set_angle(angle)
        rospy.loginfo("Servo setado com %s graus" % angle)
        angle = -1

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

'''
if __name__ == '__main__':
    rospy.loginfo("Iniciando node do servo...")
    rospy.init_node("node_test")
    servo_array = ServoProp(gpio_signal = servoPIN)
    servo_array.run()
'''