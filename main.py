# The MIT License (MIT)
#
# Copyright (c) 2024 David Festing
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


#  30 June 2024

from machine import Pin, lightsleep
import machine
import time
import config
import esp32
import camera
from my_sender import send_alarm
from mail_image import send_mail
from wifi_functions import connect, disconnect


wake_source = Pin(13, Pin.IN)  # setting wake up pin
esp32.wake_on_ext0(pin = wake_source, level = esp32.WAKEUP_ANY_HIGH)  # initialising wake up
big_flash = Pin(15, Pin.OUT, value=1)  # inverted logic

if machine.reset_cause() ==  machine.SOFT_RESET:
    print('doing a machine.reset()')
    time.sleep_ms(5)
    machine.reset()

print('wait 2 seconds to allow a CTRL-C')
time.sleep(2)

pix = const(17)
frame = const(18)

# PIXEL FORMAT
PIXFORMAT = {
    'RGB565':1,    # 2BPP/RGB565
    'YUV422':2,    # 2BPP/YUV422
    'YUV420':3,    # 1.5BPP/YUV420
    'GRAYSCALE':4, # 1BPP/GRAYSCALE
    'JPEG':5,      # JPEG/COMPRESSED
    'RGB888':6,    # 3BPP/RGB888
    'RAW':7,       # RAW
    'RGB444':8,    # 3BP2P/RGB444
    'RGB555':9,    # 3BP2P/RGB555
}

# FRAME SIZE
FRAMESIZE = {
     '96X96':1,   # 96x96
     'QQVGA':2,   # 160x120
     'QCIF':3,    # 176x144
     'HQVGA':4,   # 240x176
     '240X240':5, # 240x240
     'QVGA':6,    # 320x240
     'CIF':7,     # 400x296
     'HVGA':8,    # 480x320
     'VGA':9,     # 640x480
     'SVGA':10,   # 800x600
     'XGA':11,    # 1024x768
     'HD':12,     # 1280x720
     'SXGA':13,   # 1280x1024
     'UXGA':14,   # 1600x1200
     'FHD':15,    # 1920x1080
     'P_HD':16,   # 720x1280
     'P_3MP':17,  # 864x1536
     'QXGA':18,   # 2048x1536
}

n = PIXFORMAT.get('JPEG')
s = FRAMESIZE.get('UXGA')

import camera  # do this after the above machine.reset()

camera.conf(pix, n)    # set pixelformat
camera.conf(frame, s)  # set framesize


def main():
    while True:
        print ('going to lightsleep')
        time.sleep_ms(5)

        big_flash.init(hold=True)

        lightsleep()  # FOREVER

        big_flash.init(hold=False)

      # wait for camera ready
        for i in range(5):
            cam = camera.init()
            print("Camera ready?: ", cam)
            if cam:
                break
            else:
                time.sleep(1)
        else:
            print('Timeout, doing a machine.reset()')
            time.sleep_ms(5)

            machine.reset()

      # other settings after camera.init()
        camera.quality(5)

        big_flash.off()  # inverted logic
        time.sleep_ms(100)  # wait for flash to warm-up

      # take 5 to 10 frames, rejecting the first 4 or 9!!
        for x in range(5):
            img = camera.capture()
            time.sleep_ms(50)

        print('picture taken')
        time.sleep_ms(10)

        big_flash.on()  # inverted logic

        camera.deinit()

      # save image
        with open('image.jpeg', 'wb') as outfile:
            outfile.write(img)

      # valid jpeg ending
        valid_jpeg = b'\xff\xd9'

      # now check for the correct ending
        with open('image.jpeg', 'rb') as file:
            try:
                file.seek(-2, 2)
                while file.read(1) != b'\n':
                    file.seek(-2, 1)
            except Exception as e:
                file.seek(0)

            last_line = file.readline()

        last_chars = last_line[-2:]
#        print (f'Last 2 characters : {last_chars}')
        time.sleep_ms(5)

        if (last_chars == valid_jpeg):
#            print ('you got a jpeg image')
            time.sleep_ms(5)

            gc.collect()

            connect()
            time.sleep(1)

            print ('send alarm')
            time.sleep_ms(5)

            send_alarm (config.host, config.port)
            time.sleep(1)

            print ('send image')
            time.sleep_ms(5)

            send_mail({'to': 'xyz@gmail.com', 'subject': 'Message from gate camera', 'text': 'check this out'}, {'bytes' : img, 'name' : 'img.jpeg'})

            disconnect()

            print('image sent')
            time.sleep_ms(5)

        else:
            print ('not a valid jpeg file')
            time.sleep_ms(5)

            machine.reset()

  # end of while loop
  
            
if __name__ == '__main__':
    main()
