#!/usr/bin/python
import RPi.GPIO as GPIO
import time

""" Codigo responsavel por controlar a GPIO do motor pela Ponte H L298"""
class Motor():

    def __init__(self, gpio_dir1, gpio_dir2, gpio_dir3, gpio_dir4, gpio_pwm1, gpio_pwm2, use_m1, use_m2):

        GPIO.setmode(GPIO.BOARD)

        if (use_m1):
            self._gpio_dir1 = gpio_dir1
            self._gpio_dir2 = gpio_dir2
            self._gpio_pwm1 = gpio_pwm1

            GPIO.setup(gpio_dir1, GPIO.OUT)
            GPIO.setup(gpio_dir2, GPIO.OUT)
            GPIO.setup(gpio_pwm1, GPIO.OUT)

            pwm_m1 = GPIO.PWM(gpio_pwm1,100) # (pin, freq(Hz)))
            self._pwm_m1 = pwm_m1
            pwm_m1.start(0)  # (dutycycle(%))

        if (use_m2):
            self._gpio_dir4 = gpio_dir3
            self._gpio_dir3 = gpio_dir4
            self._gpio_pwm2 = gpio_pwm2

            GPIO.setup(gpio_dir3, GPIO.OUT)
            GPIO.setup(gpio_dir4, GPIO.OUT)
            GPIO.setup(gpio_pwm2, GPIO.OUT)

            pwm_m2 = GPIO.PWM(gpio_pwm2,100)
            self._pwm_m2 = pwm_m2
            pwm_m2.start(0)


    def set_direction(self, dir, motor):
        # dir = -1: counterclockwise; dir = 0: brake, dir = 1: clockwise
        # motor = 1: left motor; motor = 2: right motor 
        if (dir == -1 and motor == 1):
            GPIO.output(self._gpio_dir1, GPIO.HIGH)
            GPIO.output(self._gpio_dir2, GPIO.LOW)
        if (dir == -1 and motor == 2):
            GPIO.output(self._gpio_dir3, GPIO.HIGH)
            GPIO.output(self._gpio_dir4, GPIO.LOW)
        if (dir == 0 and motor == 1):
            GPIO.output(self._gpio_dir1, GPIO.LOW)
            GPIO.output(self._gpio_dir2, GPIO.LOW)
        if (dir == 0 and motor == 2):
            GPIO.output(self._gpio_dir3, GPIO.LOW)
            GPIO.output(self._gpio_dir4, GPIO.LOW)
        if (dir == 1 and motor == 1):
            GPIO.output(self._gpio_dir1, GPIO.LOW)
            GPIO.output(self._gpio_dir2, GPIO.HIGH)
        if (dir == 1 and motor == 2):
            GPIO.output(self._gpio_dir3, GPIO.LOW)
            GPIO.output(self._gpio_dir4, GPIO.HIGH)


    def set_dutycycle(self, dc, motor):
        if (motor == 1):
            self._pwm_m1.ChangeDutyCycle(dc)
        if (motor == 2):
            self._pwm_m2.ChangeDutyCycle(dc)

