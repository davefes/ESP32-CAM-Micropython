# The MIT License (MIT)
#
# Copyright (c) 2022 David Festing
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


# V1 29 Dec 2022



#  get a buffer protocol required error if you don't do a umachine.reset()
#  uncomment all the watchdog stuff if you want an extra layer of reliability


import camera
from umachine import Pin, WDT, lightsleep
import umachine
import utime
import gc
import config
from my_sender import send_alarm
from mail_image import send_mail
from wifi_functions import connect
from wifi_functions import disconnect
import esp32
#from watchdog_timer import wdt_callback
#from watchdog_timer import wdt_feed


wake_source = Pin(13, Pin.IN) #  setting wake up pin
esp32.wake_on_ext0(pin = wake_source, level = esp32.WAKEUP_ANY_HIGH)  #  initialising wake up
flash_light = Pin(4,Pin.OUT)
flash_light.off()



#  Software WDT set for 80 seconds
#wdt_callback() #  set up for 80 seconds
#wdt_feed()
#  system WDT set for 100 seconds
#wdt = WDT(timeout = 100000)  # enable it with a 100 second timeout
#wdt.feed()


def main():

    gc.collect()

    camera.init()

 #  can NOT have any delays in here??

 #  framesize 14, quality 10 and speffect 2 seems OK, most of the time

 #  camera settings
    camera.pixformat(0) #  0:JPEG, 1:Grayscale (2bytes/pixel), 2:RGB565
    camera.framesize(10) #  1:96x96, 2:160x120, 3:176x144, 4:240x176, 5:240x240
                         #  6:320x240, 7:400x296, 8:480x320, 9:640x480, 10:800x600
                         #  11:1024x768, 12:1280x720, 13:1280x1024, 14:1600x1200
                         #  15:1920x1080, 16:720x1280, 17:864x1536, 18:2048x1536
    camera.quality(5) #  [0,63] lower number means higher quality
#    camera.contrast(0) #  [-2,2] higher number higher contrast
#    camera.saturation(0) #  [-2,2] higher number higher saturation. -2 grayscale
#    camera.brightness(0) #  [-2,2] higher number higher brightness. 2 brightest
    camera.speffect(2) #  0:,no effect 1:negative, 2:black and white, 3:reddish,
                       #  4:greenish, 5:blue, 6:retro
#    camera.whitebalance(0) #  0:default, 1:sunny, 2:cloudy, 3:office, 4:home
#    camera.aelevels(0) #  [-2,2] AE Level: Automatic exposure
#    camera.aecvalue(0) #  [0,1200] AEC Value: Automatic exposure control
#    camera.agcgain(0)  #  [0,30] AGC Gain: Automatic Gain Control

    print ('waiting 5 seconds so you can do a CTRL-C')
    utime.sleep(5)


    while True:
        print (f'going to lightsleep for 60 seconds')
        utime.sleep_ms(50)

#        wdt.feed()
#        wdt_feed()

        lightsleep(60000)

#        wdt.feed()
#        wdt_feed()

        if (wake_source.value() == 1):
            print ('you got a valid trigger')
            utime.sleep_ms(50)


            flash_light.on()
            utime.sleep_ms(100) #  takes more than 50ms for the flash to come up

            img = camera.capture()

            flash_light.off()

            camera.deinit()

#            print (f'{len(img)}') #  see notes

         #  save image
            with open('image.jpeg', 'wb') as outfile:
                outfile.write(img)

         #  valid jpeg ending
            valid_jpeg = b'\xff\xd9'

         #  now check for the correct ending
            with open('image.jpeg', 'rb') as file:
                try:
                    file.seek(-2, 2)
                    while file.read(1) != b'\n':
                        file.seek(-2, 1)
                except Exception as e:
                    file.seek(0)

                last_line = file.readline()

            last_chars = last_line[-2:]
            print (f'Last 2 characters : {last_chars}')


            if (last_chars == valid_jpeg):
                print (f'you got a jpeg image')
                utime.sleep(0.1)
                
                gc.collect()

                print ('send alarm and image')
                utime.sleep(0.1)

#                wdt_feed()
#                wdt.feed()
                connect()
                utime.sleep(1)
                send_alarm (config.host, config.port)
                utime.sleep(1)
                send_mail({'to': 'dave.festing@gmail.com', 'subject': 'Message from camera', 'text': 'check this out'}, {'bytes' : img, 'name' : 'img.jpeg'})
                disconnect()

              # start all over again
                umachine.reset()

            else:
                print (f'not a valid jpeg file')
                utime.sleep(5)

             #  start all over again
                umachine.reset()

        else: #  pat the dogs
            print ('pat the dogs')
            utime.sleep(0.1)

#            wdt_feed()
#            wdt.feed()

 #  end of while loop

 #  if it gets out of the loop
    umachine.reset()


if __name__ == '__main__':
    main()
