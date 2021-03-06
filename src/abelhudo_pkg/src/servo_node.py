#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2021, Tictor's Lab, Inc.
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

# Variaveis Globais / Pinos
servoPIN   = 3
angle = -1 # 0 -> 90


''' CALLBACKS '''
def callback_servo(data):
    global angle
    angle = data.angle


class ServoProp():
    def __init__(self,
            gpio_signal,
            ):

        self.servo_array = []

        #rospy.loginfo("Iniciando servo...")
        servo = Servo(gpio_signal)
        self.servo_array.append(servo)
        rospy.loginfo("Servo configurado!")

        # Subscribers
        rospy.Subscriber("/Abelhudo/Servo", Servo_msg, callback_servo)

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
    # Inicializacao
    rospy.loginfo("Iniciando node do servo...")
    rospy.init_node("servo_node")
    servo_array = ServoProp(gpio_signal = servoPIN)
    rate = rospy.Rate(150) # --------------- RATE ---------------
    angle = 45
    # Loop
    while not rospy.is_shutdown():
        servo_array.angulo(angle)
    GPIO.cleanup()
    rospy.loginfo("Interrompendo: servo_node.")
