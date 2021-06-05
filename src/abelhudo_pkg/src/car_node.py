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
#good_dist   =  False

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
"servo_angle(angle)"
"motor_prop(pwm, dir, motor)"

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
    ax.set_title("Sonar cature plot", va='bottom')

    plt.scatter(x,y) #(x, y, 'b-', 0, 0, 'ro')
    plt.scatter(0,0)
    plt.savefig('/home/pi/teste_ws/src/package_test/scripts/foo.png')
    plt.close()

'''
# --- CODIGO SONAR SEGUIDOR ---
seed(3)
def seguidor():
    global flag_once_sonar
    global dist_ant
    global dir_sonar
    global state
    global angle
    global check

    # Sonar ativado e a distancia de retorno eh armazenada em "dist"
    sonar_array.scan()
    # Estado de procura de objetos a uma distancia menor que MIN_DIST
    if (state == "searching"):
        if (dist < MIN_DIST):
            angle = angle
            flag_once_sonar = True # Flag que permite mandar posicao angular para o Servo
            state = "locked"
        if (dist > MIN_DIST and dist_ant > MIN_DIST):
            angle = randint(15, 75)
            flag_once_sonar = True
    # Estado de objeto detectado, esperando a distancia detectada ser maior que MIN_DIST
    elif (state == "locked"):
        if (dist > MIN_DIST and dist_ant > MIN_DIST):
            if check == 0:
                if (dir_sonar == horario):
                    angle += 20
                    # Se o angulo estiver muito na borda, muda a direcao de giro do Servo
                    if angle > 90:
                        dir_sonar = antihorario
                        angle -= 40
                elif (dir_sonar == antihorario):
                    angle -= 20
                    # Se o angulo estiver muito na borda, muda a direcao de giro do Servo
                    if angle < 0:
                        dir_sonar = horario
                        angle += 40
                check += 1
                flag_once_sonar = True
            elif check == 1:
                if (dir_sonar == horario):
                    angle -= 35
                elif (dir_sonar == antihorario):
                    angle += 35
                check += 1
                flag_once_sonar = True
            elif check == 2:
                if (dir_sonar == horario):
                    angle += 25
                elif (dir_sonar == antihorario):
                    angle -= 25
                check += 1
                flag_once_sonar = True
            elif check == 3:
                if (dir_sonar == horario):
                    angle -= 30
                elif (dir_sonar == antihorario):
                    angle += 30
                check += 1
                flag_once_sonar = True
            elif check == 4:
                state = "searching"
                check = 0
        if (dist < MIN_DIST):
            if check == 1 or check == 3: # Se apos checar a primeira/terceira vez no mesmo sentido o objeto for detectado, volta para check = 0
                check = 0
            if check == 2 or check == 4: # Se apos checar a segunda/quarta vez no sentido oposto o objeto for detectado, muda de sentido
                if dir_sonar == horario:
                    dir_sonar = antihorario
                else:
                    dir_sonar = horario
                check = 0
    if angle > 90:
        angle = 180 - angle
    elif angle < 0:
        angle = -angle
    if flag_once_sonar:
        servo_array.angulo(angle) # Manda a posicao angular para o servo (0-90)
        flag_once_sonar = False

    dist_ant = dist # Variavel para checar duas vezes uma mesma distancia

    return

# --- CODIGO ENCODER ---
def encoder():
    global dir
    global count
    global flag_0
    global flag_1
    global flag_once_motor
    global estado_anterior

    # Frente
    if dir == horario:
        if count < 18: # count Frente x 0.9 = count Re ... Uma volta da roda = 18 count Frente/ 20 count Re (Aprox. 25cm)
            if flag_once_motor == True:
                motor_array.direcao(horario, motor2)
                motor_array.potencia(50, motor2)
                flag_once_motor = False
        else:
            motor_array.potencia(0, motor2)
            flag_once_motor = True
            count = 0
            if (dir == horario):
                dir = antihorario
            else:
                dir = horario
            delay.sleep(2)

    # Re
    elif dir == antihorario:
        if count < 20:
            if flag_once_motor == True:
                motor_array.direcao(antihorario, motor2)
                motor_array.potencia(50, motor2)
                flag_once_motor = False
        else:
            motor_array.potencia(0, motor2)
            flag_once_motor = True
            count = 0
            if (dir == horario):
                dir = antihorario
            else:
                dir = horario
            delay.sleep(2)

    # Checagem dupla do encoder
    estado_atual = GPIO.input(encoderPIN)
    if (estado_atual == 0 and estado_anterior == 0):
        if flag_0 == True:
            count += 1
        flag_0 = False
        flag_1 = True
    elif (estado_atual == 1 and estado_anterior == 1):
        if flag_1 == True:
            count += 1
        flag_1 = False
        flag_0 = True
    estado_anterior = estado_atual

    return
'''

def reta1(set_motor_prop_once, count_encoder_estados): # forwards
    global count_encoder
    global dist_ant_2
    global dist_ant
    global dist
    estado = "reta1"
    if (dist > 0.35 and dist_ant > 0.35 and dist_ant_2 > 0.35):
        if (set_motor_prop_once):
            motor_prop(50, horario, motor2) #pwm, dir, motor
            rospy.loginfo("Motor 2 em 50 pwm, sentido horario.")
            set_motor_prop_once = False
    if (dist < 0.35 and dist_ant < 0.35 and dist_ant_2 < 0.35):
        if (set_motor_prop_once == False):
            motor_prop(0, parar, motor2) #pwm, dir, motor
            rospy.loginfo("Motor 2 em 0 pwm, parando.")
            set_motor_prop_once = True
            count_encoder_estados = count_encoder
            estado = "reta2"
            count_encoder = 0
            delay.sleep(0.8)
    return(estado, set_motor_prop_once, count_encoder_estados)

def reta2(set_motor_prop_once, count_encoder_estados): #backwards
    global count_encoder
    estado = "reta2"
    if (count_encoder < count_encoder_estados):
        if (set_motor_prop_once):
            motor_prop(50, antihorario, motor2) #pwm, dir, motor
            rospy.loginfo("Motor 2 em 50 pwm, sentido antihorario.")
            set_motor_prop_once = False
    else:
        if (set_motor_prop_once == False):
            motor_prop(0, parar, motor2) #pwm, dir, motor
            rospy.loginfo("Motor 2 em 0 pwm, parando.")
            set_motor_prop_once = True
    return(estado, set_motor_prop_once, count_encoder_estados)



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
    set_motor_prop_once = True   # Variavel para setar o motor apenas uma vez
    count_encoder_estados = 0    # Variavel para contagem do numero de passos do encoder entre estados
    # Transformar num array ^^^^
    estado = "reta1"

    while not rospy.is_shutdown():
        if (estado == "reta1"):
            estado, set_motor_prop_once, count_encoder_estados = reta1(set_motor_prop_once, count_encoder_estados)
        elif (estado == "reta2"):
            estado, set_motor_prop_once, count_encoder_estados = reta2(set_motor_prop_once, count_encoder_estados)
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

