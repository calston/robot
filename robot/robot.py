from __future__ import division
import time
from smbus2 import SMBus
import Adafruit_PCA9685
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Servos(object):
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40, i2c_interface=SMBus)
        self.pwm.set_pwm_freq(60)

        self.centers = (380, 380, 500, 600)

        self.smin = (150, 280, 280, 500)
        self.smax = (650, 690, 700, 620)

        for i in range(4):
            self.pwm.set_pwm(i, 0, self.centers[i])

    def set_servo_pulse(self, chan, pulse):
        pulse_length = 1000000    # 1,000,000 us per second
        pulse_length //= 60       # 60 Hz
        #print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096     # 12 bits of resolution
        #print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        self.pwm.set_pwm(chan, 0, pulse)

    def center(self, chan=None):
        if not chan:
            for i in range(4):
                self.pwm.set_pwm(i, 0, self.centers[i])
        else:
            self.pwm.set_pwm(chan, 0, self.centers[chan])

    def _map_servo(self, chan, v):
        return int(self.smin[chan] + ((self.smax[chan] - self.smin[chan]) * v))

    def rotateServo(self, chan, deg):
        if not (180 >= deg > 0):
            raise Exception('Bad angle')
        # Rotate base to deg
        v = self._map_servo(chan, deg / 180.0)
        print chan, v
        self.pwm.set_pwm(chan, 0, v)


class Motor(object):
    m1a = 6
    m1b = 13
    m2a = 19
    m2b = 26

    def __init__(self):
        self.trackLeft = 0
        self.trackRight = 0

        GPIO.setup(self.m1a, GPIO.OUT)
        GPIO.setup(self.m1b, GPIO.OUT)
        GPIO.setup(self.m2a, GPIO.OUT)
        GPIO.setup(self.m2b, GPIO.OUT)

        self.set_state(0, 0, 0, 0)
    
    def set_state(self, a, b, c, d):
        GPIO.output(self.m1a, a)
        GPIO.output(self.m1b, b)
        GPIO.output(self.m2a, c)
        GPIO.output(self.m2b, d)

    def forward(self):
        self.set_state(1, 0, 1, 0)

    def reverse(self):
        self.set_state(0, 1, 0, 1)

    def left(self):
        self.set_state(1, 0, 0, 1)

    def right(self):
        self.set_state(0, 1, 1, 0)

    def stop(self):
        self.set_state(0, 0, 0, 0)
