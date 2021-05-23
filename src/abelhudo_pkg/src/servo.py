#!/usr/bin/python
from __future__ import division
import RPi.GPIO as GPIO
import time

""" Codigo responsavel por controlar a GPIO do Servo """

def mapa(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Servo():

    def __init__(self, gpio_signal):

        GPIO.setmode(GPIO.BOARD)

        self._gpio_signal = gpio_signal
        GPIO.setup(gpio_signal, GPIO.OUT)

        pwm_servo = GPIO.PWM(gpio_signal,50) # (pin, freq(Hz)))
        self._pwm_servo = pwm_servo
        pwm_servo.start(7.5) # (dutycycle(%))


    def set_angle(self, angle):
        dc_servo = round(mapa(angle, 0, 90, 5, 10), 2)
        self._pwm_servo.ChangeDutyCycle(dc_servo)
        time.sleep(0.2)
        self._pwm_servo.ChangeDutyCycle(0)
        time.sleep(0.3)

