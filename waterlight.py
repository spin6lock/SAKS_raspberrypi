#encoding:utf8

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

DS = 6
SHCP = 19
STCP = 13

LIGHTS = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
def init():
  GPIO.setup(DS, GPIO.OUT)
  GPIO.setup(SHCP, GPIO.OUT)
  GPIO.setup(STCP, GPIO.OUT)

  GPIO.output(DS, GPIO.LOW)
  GPIO.output(SHCP, GPIO.LOW)
  GPIO.output(STCP, GPIO.LOW)

def writeBit(data):
  GPIO.output(DS,data)
  GPIO.output(SHCP,GPIO.LOW)
  GPIO.output(SHCP,GPIO.HIGH)

def writeByte(data):
  for i in range(0,8):
    writeBit((data>>i) & 0x01)
  GPIO.output(STCP,GPIO.LOW)
  GPIO.output(STCP,GPIO.HIGH)

try:
  init()
  while True:
    for light in LIGHTS:
      writeByte(light)
      time.sleep(0.1)
    for light in reversed(LIGHTS):
      writeByte(light)
      time.sleep(0.1)
    writeByte(0xff)
    time.sleep(0.5)
except KeyboardInterrupt:
  writeByte(0x00)
  GPIO.cleanup()
