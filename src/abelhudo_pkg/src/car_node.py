#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2021, Tictor's Lab, Inc.
# All rights reserved.

""" Codigo teorico independente da GPIO do Raspberry, apenas trabalhando com ROS """

import sys
import math
import rospy
import numpy as np
import time as delay
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from sensor_msgs.msg import Range
from package_test.msg import Servo
from random import randint
from random import seed
seed(2) # teste 2

from sonar_node import SonarProp
from motor_node import MotorProp
from servo_node import ServoProp

GPIO.setwarnings(False)


''' PINOS '''
motorDIR1  = 40
motorDIR2  = 38
motorPWM   = 36
servoPIN   = 3
triggerPIN = 7
echoPIN    = 11
encoderPIN = 13

''' INICIANDO NODES '''
rospy.init_node("node_test")

sonar_array = SonarProp(gpio_trigger = triggerPIN,
                        gpio_echo    = echoPIN,
                        range_min    = 0.05,
                        range_max    = 3)

motor_array = MotorProp(gpio_dir1 = 0,
                        gpio_dir2 = 0,
                        gpio_dir3 = motorDIR1,
                        gpio_dir4 = motorDIR2,
                        gpio_pwm1 = 0,
                        gpio_pwm2 = motorPWM,
                        use_m1 = False,
                        use_m2 = True)

servo_array = ServoProp(gpio_signal = servoPIN)


''' CALLBACKS '''
def callback_sonar(data):
    global dist
    dist = round(data.range,2)


''' VARIAVEIS GLOBAIS '''
motor1      =  1
motor2      =  2
antihorario = -1
parar       =  0
horario     =  1
pwm         =  0
dist        =  0
good_dist   =  False


''' FUNCOES '''
#motor_array.direcao(horario, motor2)
#motor_array.potencia(pwm, motor2)
#servo_array.angulo(0-90)
#sonar_array.scan()

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


# --- CODIGO SONAR - SEGUIDOR ---
def seguidor():
    global state
    global dist_anterior
    global flag_once_sonar
    global dir_sonar
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
        if (dist > MIN_DIST and dist_anterior > MIN_DIST):
            angle = randint(15, 75)
            flag_once_sonar = True
    # Estado de objeto detectado, esperando a distancia detectada ser maior que MIN_DIST
    elif (state == "locked"):
        if (dist > MIN_DIST and dist_anterior > MIN_DIST):
            if check == 0: # Variavel para checar quatro vezes antes de sair do estado "locked"
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

    dist_anterior = dist # Variavel para checar duas vezes uma mesma distancia

    return



if __name__ == '__main__':
    rospy.Subscriber("/ModCar/sonar", Range, callback_sonar)
    rospy.loginfo("Carro iniciado.")
    rate = rospy.Rate(150) # ---------------- RATE ----------------

    # Configuracoes iniciais
    GPIO.setup(encoderPIN, GPIO.IN)
    motor_array.direcao(horario, motor2)
    servo_array.angulo(45)

    # Variaveis Encoder
    count = 0
    dir = horario
    flag_0 = False
    flag_1 = False
    flag_once = True
    estado_anterior = 0

    # Variaveis Sonar
    state = "searching"
    dist_anterior = 0
    flag_once_sonar = True
    dir_sonar = horario
    MIN_DIST = 0.2
    angle = 45
    check = 0

    while not rospy.is_shutdown():
        #state, dist_anterior, flag_once_sonar,  dir_sonar, angle, check = seguidor(state, dist_anterior, flag_once_sonar,  dir_sonar, angle, check)
        #seguidor()
        rate.sleep()

        '''
        # --- CODIGO ENCODER ---
               # Frente
        if dir == horario:
            if count < 18: # count Frente x 0.9 = count Re ... Uma volta da roda = 18 count Frente/ 20 count Re
                if flag_once == True:
                    motor_array.direcao(horario, motor2)
                    motor_array.potencia(50, motor2)
                    flag_once = False
            else:
                motor_array.potencia(0, motor2)
                flag_once = True
                count = 0
                if (dir == horario):
                    dir = antihorario
                else:
                    dir = horario
                delay.sleep(2)

               # Re
        elif dir == antihorario:
            if count < 20:
                if flag_once == True:
                    motor_array.direcao(antihorario, motor2)
                    motor_array.potencia(50, motor2)
                    flag_once = False
            else:
                motor_array.potencia(0, motor2)
                flag_once = True
                count = 0
                if (dir == horario):
                    dir = antihorario
                else:
                    dir = horario
                delay.sleep(2)

               # Checagem dupla do encoder
        estado_atual = GPIO.input(encoderPIN)
        if (estado_atual == 0 and estado_anterior == 0):
            if flag_0 == False:
                count += 1
            flag_0 = True
            flag_1 = False
        elif (estado_atual == 1 and estado_anterior == 1):
            if flag_1 == False:
                count += 1
            flag_1 = True
            flag_0 = False
        estado_anterior = estado_atual

        rate.sleep()
        '''


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
    rospy.loginfo("Interrompido.")

