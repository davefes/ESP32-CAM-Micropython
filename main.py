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


# ESP32-CAM using a normal camera

# - take two unwanted pictures, wait a total of 100ms
#   and then take the real picture

# 14 Oct 2024 D. Festing


from machine import Pin
import machine
import time
import config
from my_sender import send_alarm
from mail_image import send_mail
from wifi_functions import connect, disconnect
import gc


gc.collect()

trigger = Pin(13, Pin.IN)  # setting trigger pin

if machine.reset_cause() == machine.SOFT_RESET:
    print('doing a poweron_reset()')
    time.sleep_ms(5)
    config.poweron_reset.on()

print('wait 2 seconds to allow a CTRL-C')
time.sleep(2)

if config.watchdog is True:
    from watchdog import wdt_init, wdt_feed

  # SW/WDT set for 90 seconds
    wdt_init(90)
    wdt_feed()

pix = const(17)
frame = const(18)

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

# wait for camera ready
for i in range(5):
    cam = camera.init()
    print("Camera ready?: ", cam)
    if cam:
        break
    else:
        time.sleep(1)
else:
    # probably safer to the following before any resets
    camera.deinit()

    print('Timeout, doing a poweron_reset()')
    time.sleep_ms(5)

    config.poweron_reset.on()

# other settings after camera.init()
camera.quality(5)
camera.brightness(-2)

config.cam_state = True


def main():
    while True:
        if trigger.value() == 1:
            print('taking a picture')
            time.sleep_ms(10)

          # throw-away two images, this sets
          # the camera up for a proper picture
            unwanted_img = camera.capture()

            time.sleep_ms(100)

            unwanted_img = camera.capture()

            time.sleep_ms(100)

            img = camera.capture()

            print('picture taken')
            time.sleep_ms(10)

            camera.deinit()

            config.cam_state = False

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
#            print (f'Last 2 characters : {last_chars}')
            time.sleep_ms(5)

            if (last_chars == valid_jpeg):
#                print ('you got a jpeg image')
                time.sleep_ms(5)

                gc.collect()

                if config.watchdog is True:
                    wdt_feed()

                connect()
                time.sleep(1)

                config.wifi_state = True

#                print ('send alarm')
#                time.sleep_ms(5)

#                send_alarm (config.host, config.port)
#                time.sleep(1)

                if config.watchdog is True:
                    wdt_feed()

                print ('send image')
                time.sleep_ms(5)

                send_mail({'to': 'chrisfigg35@gmail.com', 'subject': 'Message from day camera', 'text': 'check this out'}, {'bytes' : img, 'name' : 'img.jpeg'})

                disconnect()

                config.wifi_state = False

                if config.watchdog is True:
                    wdt_feed()

                print('image sent and waiting 30 seconds')
                time.sleep(30)

              # after every picture
                print('doing a poweron_reset()')
                time.sleep_ms(5)

                config.poweron_reset.on()

            else:
                print ('not a valid jpeg file')
                time.sleep_ms(5)

                print('doing a poweron_reset()')
                time.sleep_ms(5)

                config.poweron_reset.on()

        else:
            print('looping')
            time.sleep_ms(10)

            if config.watchdog is True:
                wdt_feed()


if __name__ == '__main__':
    main()
