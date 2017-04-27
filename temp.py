#!/usr/bin/python3

import re
import subprocess
import time
#import winsound # beeps
import os

# Check if the directory exists.
# Then set the pwm file including path.
check_dir = os.path.isdir('/sys/devices/platform/asus-nb-wmi/hwmon/hwmon1')
if check_dir == True:
 pwm1 = '/sys/devices/platform/asus-nb-wmi/hwmon/hwmon1/pwm1'
else:
 pwm1 = '/sys/devices/platform/asus-nb-wmi/hwmon/hwmon2/pwm1'

# current pwm
# Assume that current pwm starts at 85.
# From then on, assume that current pwm is
# whatever value is currently saved into 
# global variable current_pwm.
current_pwm = 85
current_temp = 0

def n():
 global current_pwm, current_temp
 output = subprocess.check_output("sensors", shell=True)
 m = re.search('temp1:\s+\+(\d+)', output.decode('utf-8')) # Change output from bytes into string
  ###print (m.group(1))
 t = int(m.group(1))
 current_temp = t
 if t >= 54 and current_pwm < 255: # Max is 255 ... probably ...
  too_hot()
 elif t <= 48 and current_pwm > 85: # Bring down if above 85 and cooler than 46
  too_loud()
 # Now wait 20 seconds before starting again. 
 time.sleep(20)
 return n()
 #
 #else: # Wait for awhile and then start over.

def too_loud():
 ''' The fan is too loud. And it is unnecessary to cool
     the machine. The machine is cool enough.
 '''
 global current_pwm, current_temp, pwm1
 current_pwm -= 10
 print('Temp is '+str(current_temp)+'. Decreasing pwm to ' + str(current_pwm))
 output = subprocess.check_output("echo " + str(current_pwm) +" > "+ pwm1, shell=True)
 return
 
def too_hot(): # Cool down :)
 ''' The command that shall be run is e.g.:
     echo 140 > pwm1
 '''
 # Increase global variable current_pwm
 global current_pwm, current_temp, pwm1
 current_pwm += 10
 print('Temp is '+str(current_temp)+'. Increasing pwm to ' + str(current_pwm))
 output = subprocess.check_output("echo " + str(current_pwm) +" > "+ pwm1, shell=True)
 #print('Returned:' + str(output))
 # Make a ding :)
 print('\a')
#Freq = 2500 # Set Frequency To 2500 Hertz
 #Dur = 1000 # Set Duration To 1000 ms == 1 second
 #winsound.Beep(Freq,Dur)
 return


if __name__ == "__main__":
 n()
