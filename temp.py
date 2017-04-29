#!/usr/bin/python3
"""Usage: `sudo ./temp.py`.

Description: Checks temperature. When temperature is above 54C,
increases PWM by 10. When temperature is below 48C, decreases
PWM by 10. After this, sleep for 20 seconds before again
checking the temperature.
"""

import re
import subprocess
import time
import os

# Check if the directory exists.
# Then set the pwm file including path.
check_dir = os.path.isdir('/sys/devices/platform/asus-nb-wmi/hwmon/hwmon1')
if check_dir == True:
 pwm1 = '/sys/devices/platform/asus-nb-wmi/hwmon/hwmon1/pwm1'
else:
 pwm1 = '/sys/devices/platform/asus-nb-wmi/hwmon/hwmon2/pwm1'

# Current pwm.
# Assume that current pwm starts at 85.
# From then on, assume that current pwm is
# whatever value is currently saved into
# global variable current_pwm.
current_pwm = 85
current_temp = 0

# Set these values.
# Max hot and min cold.
MAX_HOT = 50
MIN_COLD = 46

def n():
 """An infinite loop which checks CPU temperature, optionally changes PWM, and then sleeps."""
 global current_pwm, current_temp, MAX_HOT, MIN_COLD
 while True:
  output = subprocess.check_output("sensors", shell=True)
  # Change output from bytes into string
  m = re.search('temp1:\s+\+(\d+)', output.decode('utf-8'))
  t = int(m.group(1))
  current_temp = t
  if t >= MAX_HOT and current_pwm < 255:
   # Max is 255... probably.
   too_hot()
  elif t <= MIN_COLD and current_pwm > 85:
   # Bring down if above 85 and cooler than 46
   too_loud()
  # Now wait 20 seconds before starting again. 
  time.sleep(20)

def too_loud():
 """The fan is too loud.

 It is unnecessary to cool the machine. The machine is cool enough.
 """
 global current_pwm, current_temp, pwm1
 current_pwm -= 10
 print('Temp is '+str(current_temp)+'. Decreasing pwm to ' + str(current_pwm))
 output = subprocess.check_output(
  "echo " + str(current_pwm) +" > "+ pwm1,
  shell=True)
 return
 
def too_hot():
 """Cool down.

 The command that is run is: echo 140 > pwm1.
 Increases global variable current_pwm.
 """
 global current_pwm, current_temp, pwm1
 current_pwm += 10
 print('Temp is '+str(current_temp)+'. Increasing pwm to ' + str(current_pwm))
 output = subprocess.check_output(
  "echo " + str(current_pwm) +" > "+ pwm1,
  shell=True)
 # Make a ding.
 print('\a')
 return

if __name__ == "__main__":
 print('Heat control is on.')
 n()
