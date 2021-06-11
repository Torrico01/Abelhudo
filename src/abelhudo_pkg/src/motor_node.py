#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2009, Tictor's Lab, Inc.
# All rights reserved.

""" Codigo teorico independente do GPIO do Raspberry, apenas trabalhando com ROS"""

# Importando Bibliotecas
import sys
import math
import rospy
import time as delay
import RPi.GPIO as GPIO
# Importando Mensagens ROS
from abelhudo_pkg.msg import Motor_msg
# Importando GPIO Local
from motor import Motor

# Desabilita Avisos da GPIO
GPIO.setwarnings(False)

# Variaveis Globais / Pinos
motorDIR1  = 40
motorDIR2  = 38
motorPWM   = 36
pwm   = 0  # 0 -> 100
dir   = 0  # 1 (horario), 0 (parando), ou -1 (antihorario)
motor = 0  # 1 ou 2

''' CALLBACKS '''
def callback_motor(data):
    global pwm
    global dir
    global motor
    pwm = data.pwm
    dir = data.dir
    motor = data.motor

class MotorProp():
    def __init__(self,
            gpio_dir1,
            gpio_dir2,
            gpio_dir3,
            gpio_dir4,
            gpio_pwm1,
            gpio_pwm2,
            use_m1,
            use_m2
            ):

        self.motor_array = []

        #rospy.loginfo("Iniciando motor...")
        motor = Motor(gpio_dir1, gpio_dir2, gpio_dir3, gpio_dir4, gpio_pwm1, gpio_pwm2, use_m1, use_m2)
        self.motor_array.append(motor)
        rospy.loginfo("Motor configurado!")

        # Subscribers
        rospy.Subscriber("/Abelhudo/Motor", Motor_msg, callback_motor)

    def direcao(self, dir, motor):
        # dir = -1: counterclockwise; dir = 0: brake, dir = 1: clockwise
        # motor = 1: left motor; motor = 2: right motor
        self.motor_array[0].set_direction(dir, motor)
        if (dir == -1):
            rospy.loginfo_throttle(1, "Motor %d setado em anti-horario"%motor)
        if (dir == 0):
            rospy.loginfo_throttle(1, "Motor %d setado para parar"%motor)
        if (dir == 1):
            rospy.loginfo_throttle(1, "Motor %d setado em horario"%motor)

    def potencia(self, dc, motor):
        self.motor_array[0].set_dutycycle(dc, motor)
        rospy.loginfo_throttle(1, "Motor %s com ducycycle de %s%%" % (motor,dc))

    def run(self):
        #--- Set the control rate
        rate = rospy.Rate(1)

        rospy.loginfo("Motor operando...")
        while not rospy.is_shutdown():
            self.direcao(1, 2)
            self.potencia(100, 2)
            rate.sleep()
        GPIO.cleanup()
        rospy.loginfo("Interrompido.")

if __name__ == '__main__':
    # Inicializacao
    rospy.loginfo("Iniciando node do motor...")
    rospy.init_node("motor_node")
    motor_array = MotorProp(gpio_dir1 = 0,
                            gpio_dir2 = 0,
                            gpio_dir3 = motorDIR1,
                            gpio_dir4 = motorDIR2,
                            gpio_pwm1 = 0,
                            gpio_pwm2 = motorPWM,
                            use_m1 = False,
                            use_m2 = True)
    rate = rospy.Rate(150) # --------------- RATE ---------------
    # Loop
    while not rospy.is_shutdown():
        motor_array.direcao(dir, motor)
        motor_array.potencia(pwm, motor)
    GPIO.cleanup()
    rospy.loginfo("Interrompendo: motor_node.")
