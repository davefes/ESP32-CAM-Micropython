#  to config ESP32_CAM_Micropython

from machine import Pin


#  enable/disable debugging in my_uMail
debug = False

#  in wifi_function.py
gateway = '192.168.8.1'
hotspot = 'HUAWEI-E8231-7bd5'
password = 'xyz'
WiFi_device = '192.168.8.80'

host = '192.168.8.75'
port = 8090

poweron_reset = Pin(12, Pin.OUT) #  poweron_reset drive
