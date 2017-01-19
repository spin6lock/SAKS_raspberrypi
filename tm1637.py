#encoding:utf8
import RPi.GPIO as GPIO
import time

DI = 25
CLK = 5
ADDR_AUTO = 0x40
ADDR_FIX = 0x44
DIGIT_CODE = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f, 0x00, 0x40]
ADDR_CODE = [0xc0, 0xc1, 0xc2, 0xc3]
MAX_BRIGHTNESS = 0x8f
MIN_BRIGHTNESS = 0x80
CHAR_MAP = {
    'L':0x38,
    'O':0x3f,
    'V':0x3f,
    'E':0x3e,
}

GPIO.setmode(GPIO.BCM)

class TM1637:
  def __init__(self, clk_pin=CLK, di_pin=DI):
    self.clk = clk_pin
    self.di = di_pin
    GPIO.setup(self.clk, GPIO.OUT)
    GPIO.setup(self.di, GPIO.OUT)

  def bus_delay(self):
    time.sleep(0.001)

  def low_di(self):
    GPIO.output(self.di, GPIO.LOW)
    self.bus_delay()

  def high_di(self):
    GPIO.output(self.di, GPIO.HIGH)
    self.bus_delay()

  def low_clk(self):
    GPIO.output(self.clk, GPIO.LOW)
    self.bus_delay()

  def high_clk(self):
    GPIO.output(self.clk, GPIO.HIGH)
    self.bus_delay()

  def writeBit(self, data):
    self.low_clk()
    GPIO.output(self.di, data)  #send 1 bit
    self.high_clk()

  def writeByte(self, data):
    for i in xrange(0,8):
      self.writeBit((data >> i) &0x01)
    #wait for ack
    self.low_clk()
    self.high_di()
    self.high_clk()
    GPIO.setup(self.di, GPIO.IN)
    while GPIO.input(self.di):
        print "still high, wait for ack"
        time.sleep(0.1)
        self.high_clk()
    print "ack:", data
    GPIO.setup(self.di, GPIO.OUT)

  def start_sending(self):
    self.high_clk()
    self.high_di()
    self.low_di() 	#di 1->0
    self.low_clk()

  def end_sending(self):
    self.high_clk()
    self.low_di()
    self.high_di()

  def set_command(self, command):
    self.start_sending()
    self.writeByte(command)
    self.start_sending()

  def set_data(self, addr, data):
    self.start_sending()
    self.writeByte(addr)
    self.writeByte(data)
    self.start_sending()

  def show_fix(self, data):
    self.current_data = data
    self.set_command(ADDR_FIX) #try fix address
    for i in range(0, 4):
        digit = int(data[i])
        print "digit:", digit
        digit_code = DIGIT_CODE[digit]
        addr_code = ADDR_CODE[i]
        self.set_data(addr_code, digit_code)
    self.set_command(MAX_BRIGHTNESS)

  def show_auto(self, data):
    self.set_command(ADDR_AUTO)
    for i in range(0, 4):
        digit = int(data[i])
        print "digit:", digit
        digit_code = DIGIT_CODE[digit]
        self.writeByte(digit_code)
    self.set_command(MAX_BRIGHTNESS)

  def clear(self):
    self.set_command(MIN_BRIGHTNESS)

  def show(self, data):
    self.set_command(ADDR_AUTO)
    for i in range(0, 4):
      char = data[i]
      if char.isdigit():
        digit = int(data[i])
        digit_code = DIGIT_CODE[digit]
        self.writeByte(digit_code)
      elif char == "#":
        digit = 11
        digit_code = DIGIT_CODE[digit]
        self.writeByte(digit_code)
      elif CHAR_MAP.get(char, None):
        digit_code = CHAR_MAP[char]
        self.writeByte(digit_code)
    self.set_command(MAX_BRIGHTNESS)

if __name__ == "__main__":
    obj = TM1637(CLK,DI)
    obj.show_fix("1234")
    raw_input("Press Enter to continue...")
    obj.clear()
