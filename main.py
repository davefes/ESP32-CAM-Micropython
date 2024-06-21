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


# V2 21 June 2024

#  get a buffer protocol required error if you don't do a machine.reset()
#  or a poweron_reset()
#  flash_light disconnected as putting 4V or 3V3 on the line down the edge
#  of the board caused 80mA pulses of current.  That 3V3 line is right close
#  to the UART TX line and maybe some form of oscillation was taking place
#  not on the 2nd board

#  21 June 2024 D. Festing


import camera
from machine import Pin, WDT, lightsleep
import machine
import time
import gc
import config
from my_sender import send_alarm
from mail_image import send_mail
from wifi_functions import connect, disconnect
import esp32
#from watchdog import wdt_init, wdt_feed


gc.collect()

wake_source = Pin(13, Pin.IN)  # setting wake up pin
esp32.wake_on_ext0(pin = wake_source, level = esp32.WAKEUP_ANY_HIGH)   # initialising wake up
flash_light = Pin(4,Pin.OUT, hold=False)
big_flash_light = Pin(15, Pin.OUT, hold=False)
poweron_reset = Pin(2, Pin.OUT,  hold=False)

flash_light.off()
big_flash_light.off()
poweron_reset.off()

# SW/WDT set for 90 seconds
#wdt_init(90)
#wdt_feed()

# system WDT set for 100 seconds
#wdt = WDT(timeout = 100000)

if machine.reset_cause() == machine.SOFT_RESET:
    print('doing a poweron_reset(), ignore Brownout msg')

    poweron_reset.on()

print('waiting 2 seconds so that I can do a CTRL-C')
time.sleep(2)


def main():
#    wdt_feed()
#    wdt.feed()

    gc.collect()

    camera.init()

  # camera settings
    camera.pixformat(0)   # 0:JPEG, 1:Grayscale (2bytes/pixel), 2:RGB565
    camera.framesize(11)  # 1:96x96, 2:160x120, 3:176x144, 4:240x176, 5:240x240
                          # 6:320x240, 7:400x296, 8:480x320, 9:640x480, 10:800x600
                          # 11:1024x768, 12:1280x720, 13:1280x1024, 14:1600x1200
                          # 15:1920x1080, 16:720x1280, 17:864x1536, 18:2048x1536
    camera.quality(5)  # [0,63] lower number means higher quality
#    camera.contrast(0)  # [-2,2] higher number higher contrast
#    camera.saturation(0)  # [-2,2] higher number higher saturation. -2 grayscale
#    camera.brightness(0)  # [-2,2] higher number higher brightness. 2 brightest
#    camera.speffect(2)  # 0:,no effect 1:negative, 2:black and white, 3:reddish,
                        # 4:greenish, 5:blue, 6:retro
#    camera.whitebalance(0)  # 0:default, 1:sunny, 2:cloudy, 3:office, 4:home
#    camera.aelevels(0)  # [-2,2] AE Level: Automatic exposure
#    camera.aecvalue(0)  # [0,1200] AEC Value: Automatic exposure control
#    camera.agcgain(0)   # [0,30] AGC Gain: Automatic Gain Control

    print ('waiting 5 seconds for camera setup')
    time.sleep(5)


    while True:
        print ('going to lightsleep FOREVER')
        time.sleep_ms(5)

        flash_light.init(hold=True)
        big_flash_light.init(hold=True)
        poweron_reset.init(hold=True)

#        wdt.feed()
#        wdt_feed()

        lightsleep()

        flash_light.init(hold=False)
        big_flash_light.init(hold=False)
        poweron_reset.init(hold=False)

#        wdt.feed()
#        wdt_feed()

#        if 1 == 1:  # for testing
        if (wake_source.value() == 1):
            print ('you got a valid trigger')
            time.sleep_ms(5)

            big_flash_light.on()

            time.sleep_ms(250)  # takes more than 100ms for BIG flash to come up

            img = camera.capture()

#            time.sleep_ms(250)  # probably not needed

            big_flash_light.off()

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
            print (f'Last 2 characters : {last_chars}')
            time.sleep_ms(5)

            if (last_chars == valid_jpeg):
                print ('you got a jpeg image')
                time.sleep_ms(5)

                gc.collect()

                print ('send alarm')
                time.sleep_ms(5)

#                wdt_feed()
#                wdt.feed()
                connect()
                time.sleep(1)
                send_alarm (config.host, config.port)
                time.sleep(1)

                print ('send image')
                time.sleep_ms(5)

                send_mail({'to': 'dave.festing@gmail.com', 'subject': 'Message from camera', 'text': 'check this out'}, {'bytes' : img, 'name' : 'img.jpeg'})
                disconnect()

                print('image sent')
                time.sleep_ms(10)

              # start all over again
                print('doing a poweron_reset(), ignore Brownout msg')

                poweron_reset.on()

            else:
                print ('not a valid jpeg file')
                time.sleep(1)

              # start all over again
                print('doing a poweron_reset(), ignore Brownout msg')

                poweron_reset.on()

#        else:  # pat the dogs
#            print ('pat the dogs')
#            time.sleep_ms(5)

#            wdt_feed()
#            wdt.feed()

  # end of while loop

  # if it gets out of the loop
    poweron_reset.on()


if __name__ == '__main__':
    main()
