#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2021, Tictor's Lab, Inc.
# All rights reserved.

""" Codigo teorico independente da GPIO do Raspberry, apenas trabalhando com ROS """

# Importando Bibliotecas
import sys
import math
import rospy
import numpy as np
import time as delay
import RPi.GPIO as GPIO
from random import seed
from random import randint
import matplotlib.pyplot as plt
# Importando Mensagens ROS
from sensor_msgs.msg import Range
from abelhudo_pkg.msg import Servo_msg
from abelhudo_pkg.msg import Motor_msg
from abelhudo_pkg.msg import Encoder_msg
# Desabilita Avisos da GPIO
GPIO.setwarnings(False)

''' PINOS '''
motorDIR1  = 40
motorDIR2  = 38
motorPWM   = 36
servoPIN   = 3
triggerPIN = 7
echoPIN    = 11
encoderPIN = 13

''' INICIANDO NODE '''
rospy.init_node("abelhudo_node")

''' CALLBACKS '''
def callback_sonar(data):
    global dist
    global dist_ant
    global dist_ant_2
    dist_ant_2 = dist_ant
    dist_ant = dist
    dist = round(data.range,2)

def callback_encoder(data):
    global estado_encoder
    global count_encoder
    count_encoder += 1
    estado_encoder = data.estado

''' PUBLISHERS '''
def servo_angle(angle):
    global pub_servo
    global message_servo
    message_servo.angle = angle
    pub_servo.publish(message_servo)

def motor_prop(pwm, dir, motor):
    global pub_motor
    global message_motor
    message_motor.pwm = pwm
    message_motor.dir = dir
    message_motor.motor = motor
    pub_motor.publish(message_motor)

''' VARIAVEIS GERAIS '''
motor1      =  1
motor2      =  2
antihorario = -1
parar       =  0
horario     =  1

''' Variaveis Globais '''
# Variaveis Encoder
dir = horario          # Direcao do motor
count_encoder = 0      # Contagem do numero de transicoes do infravermelho do encoder
estado_encoder = 0     # Estado recebido por subscriber do encoder_node
flag_once_motor = True # Variavel para setar a potencia do motor apenas uma vez

# Variaveis Sonar
flag_once_sonar = True # Variavel para setar o angulo do servo apenas uma vez
dir_sonar = horario    # Direcao de giro do servo
state = "searching"    # Estado do sonar
dist_ant_2 = 1.0       # Variavel para fazer verificacao tripla do sonar
dist_ant = 1.0         # Variavel para fazer verificacao dupla do sonar
MIN_DIST = 0.2         # Constante da distancia minima do estado locked (20 cm)
angle = 45             # Angulo do servo
check = 0              # Variavel para checar quatro vezes antes de sair do estado locked
dist =  0              # Distancia global recebida pelo subscriber do sonar_node

''' FUNCOES '''

def pol2cart(theta, r):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return(x, y)

def plot(theta, r):
    for i in range(len(r)):
        if r[i] > 1.5:
            np.delete(r,i,i-1)
            np.delete(theta,i,i-1)
    x, y = pol2cart(theta, r)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position(('data', 0.0))
    ax.spines['bottom'].set_position(('data', 0.0))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.grid(True)
    ax.set_title("Mapa", va='bottom')

    plt.scatter(x,y) #(x, y, 'b-', 0, 0, 'ro')
    plt.scatter(0,0)
    plt.savefig('/home/pi/teste_ws/src/package_test/scripts/foo.png')
    plt.close()

def start_mapa():
    global dist
    global dist_ant
    global dist_ant_2
    mapa = []
    # Olha para a direita
    for i in range 5:
        servo_angle(1)
    delay.sleep(0.2)
    mean_dist = round((dist + dist_ant + dist_ant_2) / 3)
    if (dist < 1.5):
        mapa.append((0,mean_dist*100))
    # Olha para a esquerda
    for i in range 5:
        servo_angle(89)
    delay.sleep(0.2)
    mean_dist = round((dist + dist_ant + dist_ant_2) / 3)
    if (dist < 1.5):
        mapa.append((0,-mean_dist*100))
    return mapa

def plot_mapa(mapa):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position(('data', 0.0))
    ax.spines['bottom'].set_position(('data', 0.0))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.grid(True)
    ax.set_title("Sonar capture plot", va='bottom')
    plt.scatter(0,0)
    plt.scatter(*zip(*mapa))
    plt.savefig('/home/pi/abelhudo_ws/src/abelhudo_pkg/src/foo.png')
    plt.close()
    return

def get_length(count_encoder_estados): # forwards
    global count_encoder
    global dist_ant_2
    global dist_ant
    global dist
    estado = "reta1"
    if (dist > 0.35 and dist_ant > 0.35 and dist_ant_2 > 0.35):
        motor_prop(70, antihorario, motor2) #pwm, dir, motor
    if (dist < 0.35 and dist_ant < 0.35 and dist_ant_2 < 0.35):
        motor_prop(0, parar, motor2) #pwm, dir, motor
        count_encoder_estados = count_encoder
        estado = "reta2"
        count_encoder = 0
        delay.sleep(1)
    return(estado, count_encoder_estados)

def backwards(count_encoder_estados): #backwards
    global count_encoder
    estado = "reta2"
    servo_angle(89)
    if (count_encoder < count_encoder_estados):
        motor_prop(70, horario, motor2) #pwm, dir, motor
    else:
        motor_prop(0, parar, motor2) #pwm, dir, motor
    return(estado, count_encoder_estados)

def record(mapa):
    global dist
    
    return mapa


if __name__ == '__main__':

    ''' Subscribers '''
    rospy.Subscriber("/Abelhudo/Sonar", Range, callback_sonar)
    rospy.Subscriber("/Abelhudo/Encoder", Encoder_msg, callback_encoder)

    ''' Publishers '''
    pub_servo = rospy.Publisher("/Abelhudo/Servo", Servo_msg, queue_size=1) # Queue size: tamanho do armazenamento do sinal enviado ate que o subscriber consiga ler (1 eh bom para sensores instantaneos)
    rospy.loginfo("Publicando angulo do servo em /Abelhudo/Servo")
    message_servo = Servo_msg()
    pub_motor = rospy.Publisher("/Abelhudo/Motor", Motor_msg, queue_size=3) # Queue size: tamanho do armazenamento do sinal enviado ate que o subscriber consiga ler (1 eh bom para sensores instantaneos)
    rospy.loginfo("Publicando propriedades do motor em /Abelhudo/Motor")
    message_motor = Motor_msg()

    ''' Inicializacao '''
    rospy.loginfo("Carro iniciado.")
    servo_angle(45)
    rate = rospy.Rate(150) # ---------------- RATE ----------------

    ''' Variaveis locais '''
    count_encoder_estados = 0    # Variavel para contagem do numero de passos do encoder entre estados
    # Transformar num array ^^^^
    estado = "reta1"
    mapa = start_mapa()
    plot_mapa()

    while not rospy.is_shutdown():
        #if (estado == "reta1"):
        #    estado, count_encoder_estados = get_length(count_encoder_estados)
        #elif (estado == "reta2"):
        #    estado, count_encoder_estados = backwards(count_encoder_estados)
        #    mapa = record(mapa)

        rate.sleep()


    ''' --- CODIGO SONAR EM COORD POLAR ---
    # Angle Range
    angles = np.arange(0,100,10)
    # Conversionto Radians
    theta = np.radians(np.arange(-45,55,10))
    r = []

    for angle in angles:
        servo_array.angulo(angle) #angle
        #delay.sleep(1)
        while (good_dist == False):
            sonar_array.scan()
            if (dist[len(dist)-1] == dist[len(dist)-2] and dist[len(dist)-2] == dist[len(dist)-3]):
                good_dist = True
                pass
        r.append(dist[len(dist)-1])
        dist = [0,10,100]
        good_dist = False

    plot(theta, r)
    '''

    GPIO.cleanup()
    rospy.loginfo("Interrompendo: car_node.")

