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
from abelhudo_pkg.msg import Encoder_msg

# Desabilita Avisos da GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Variaveis Globais / Pinos
encoderPIN = 13
estado_anterior = 0 # 0 ou 1
flag_0 = True       # Flag para contar apenas uma vez a transicao para 0
flag_1 = True       # Flag para contar apenas uma vez a transicao para 1

class EncoderProp():
    def __init__(self,
            gpio_encoder
            ):

        self.encoder_array = []
        self.pub_array   = []

        #rospy.loginfo("Iniciando encoder...")
        #encoder = Encoder(gpio_encoder)
        #self.encoder_array.append(encoder)
        GPIO.setup(encoderPIN, GPIO.IN)
        rospy.loginfo("Encoder configurado!")

        # Publishers
        topic_name = "/Abelhudo/Encoder"
        pub = rospy.Publisher(topic_name, Encoder_msg, queue_size=5)
        self.pub_array.append(pub)
        rospy.loginfo("Publicando recepcao do encoder em /Abelhudo/Encoder")

        message = Encoder_msg()
        self._message  = message

    def read(self, estado_anterior, flag_0, flag_1):
        estado_atual = GPIO.input(encoderPIN)
        # Checagem dupla do encoder
        if (estado_atual == 0 and estado_anterior == 0):
            if flag_0 == True:
                self._message.estado = estado_atual
                self.pub_array[0].publish(self._message)
            flag_0 = False
            flag_1 = True
        elif (estado_atual == 1 and estado_anterior == 1):
            if flag_1 == True:
                self._message.estado = estado_atual
                self.pub_array[0].publish(self._message)
            flag_1 = False
            flag_0 = True
        estado_anterior = estado_atual
        return(estado_anterior, flag_0, flag_1)

if __name__ == '__main__':
    # Inicializacao
    rospy.loginfo("Iniciando node do encoder...")
    rospy.init_node("encoder_node")
    encoder_array = EncoderProp(gpio_encoder = encoderPIN)
    rate = rospy.Rate(150) # --------------- RATE ---------------
    # Loop
    while not rospy.is_shutdown():
        estado_anterior, flag_0, flag_1 = encoder_array.read(estado_anterior, flag_0, flag_1)
    GPIO.cleanup()
    rospy.loginfo("Interrompendo: encoder_node.")
