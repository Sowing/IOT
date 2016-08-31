import mraa
import time
import sys

buzz_pin_number=6

buzz = mraa.Gpio(buzz_pin_number)
buzz.dir(mraa.DIR_OUT)
buzz.write(1)
time.sleep(2)
buzz.write(0)

sys.exit()
