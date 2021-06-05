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
from sensor_msgs.msg import Range
# Importando GPIO Local
from sonar import Sonar

# Desabilita Avisos da GPIO
GPIO.setwarnings(False)

# Variaveis Globais / Pinos
triggerPIN = 7
echoPIN    = 11

class SonarProp():
    def __init__(self,
            gpio_trigger,
            gpio_echo,
            range_min,
            range_max
            ):

        self.sonar_array = []
        self.pub_array   = []

        #rospy.loginfo("Iniciando sonar...")
        sonar = Sonar(gpio_trigger, gpio_echo, range_min=range_min*100, range_max=range_max*100)
        self.sonar_array.append(sonar)
        rospy.loginfo("Sonar configurado!")

        # Publishers
        topic_name = "/Abelhudo/Sonar"
        pub = rospy.Publisher(topic_name, Range, queue_size=5)
        self.pub_array.append(pub)
        rospy.loginfo("Publicando recepcao do sonar em /Abelhudo/Sonar")

        message = Range()
        message.radiation_type  = 0
        message.min_range       = range_min
        message.max_range       = range_max
        self._message           = message

    def scan(self):
        range_array = []

        range_cm = self.sonar_array[0].get_range()
        range_array.append(range_cm*0.01)
        self._message.range = range_cm*0.01
        self.pub_array[0].publish(self._message)

        rospy.loginfo_throttle(0.1,"Distancia: %.2f m"%range_array[0])
        #rospy.loginfo("Distancia: %.2f m"%range_array[0])


    def run(self):
        #--- Set the control rate
        rate = rospy.Rate(10)

        rospy.loginfo("Sonar operando...")
        while not rospy.is_shutdown():
            self.scan()
            rate.sleep()
        GPIO.cleanup()
        rospy.loginfo("Interrompido.")



if __name__ == '__main__':
    # Inicializacao
    rospy.loginfo("Iniciando node do sonar...")
    rospy.init_node("sonar_node")
    sonar_array = SonarProp(gpio_trigger = triggerPIN,
                            gpio_echo    = echoPIN,
                            range_min    = 0.05,
                            range_max    = 3.5)
    rate = rospy.Rate(10) # --------------- RATE ---------------
    # Loop
    while not rospy.is_shutdown():
        sonar_array.scan()
    GPIO.cleanup()
    rospy.loginfo("Interrompendo: sonar_node.")
