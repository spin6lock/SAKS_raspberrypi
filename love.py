#encoding:utf8
from tm1637 import TM1637
import time

board = TM1637()
board.show("L###")
time.sleep(0.3)
board.show("#O##")
time.sleep(0.3)
board.show("##V#")
time.sleep(0.3)
board.show("###E")
time.sleep(0.3)
board.show("LOVE")
raw_input("Press Enter to continue...")
board.clear()
