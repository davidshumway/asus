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
PWM_OVER_70 = 255 # 255 is maximum but it is loud.
PWM_OVER_60 = 220 # This says 60 but is actually ...
PWM_OVER_50 = 110 # Actually goes down to 48.
TIME_TO_SLEEP = 1
# Tend toward three settings.
# High: If it is 55+,   go toward 255 until it is below 55
# Mid:  If it is 50-55, go toward 120 (medium).
# Low:  If it is -49,   go toward 85 (min).

def n():
 """An infinite loop which checks CPU temperature, optionally changes PWM, and then sleeps.
 
 Always wait an additional 4 seconds when cooling down.
 """
 global current_pwm, current_temp
 global MAX_HOT, MIN_COLD, MAX_PWM, TIME_TO_SLEEP
 global PWM_OVER_70
 global PWM_OVER_60
 global PWM_OVER_50
 while True:
  output = subprocess.check_output("sensors", shell=True)
  # Change output from bytes into string
  m = re.search('temp1:\s+\+(\d+)', output.decode('utf-8'))
  t = int(m.group(1))
  current_temp = t
  if   t > 70  and current_pwm <  PWM_OVER_70:
   too_hot()
  elif t <= 70 and current_pwm >= PWM_OVER_70:
   too_loud()
   time.sleep(2)
  elif t > 60  and current_pwm <  PWM_OVER_60: #62
   too_hot()
  elif t <= 60 and current_pwm >= PWM_OVER_50:
   too_loud()
   time.sleep(2)
  elif t > 48  and current_pwm <  PWM_OVER_50:
   too_hot()
  elif t <= 48 and current_pwm >= 80:
   too_loud()
   time.sleep(2)
  # Now wait 20 seconds before starting again. 
  time.sleep(TIME_TO_SLEEP)

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
 ## Make a ding.
 ## print('\a')
 return

if __name__ == "__main__":
 print('Heat control is on.')
 n()
