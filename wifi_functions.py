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


import network
import utime
import config
from machine import Pin


sta_if = network.WLAN(network.STA_IF)


def connect():
    count = 0


    sta_if.active(True)

 #  seems more reliable to start with a fresh connect()
    if sta_if.isconnected():
        sta_if.disconnect()
        print (f'started in the connected state, but now disconnected')
    else:
        print (f'started in the disconnected state')

    utime.sleep(0.1)

    if not sta_if.isconnected():
        print (f'connecting to hotspot...')
        utime.sleep(0.1)

        try:
            sta_if.connect(config.hotspot, config.password)
            sta_if.ifconfig((config.WiFi_device, '255.255.255.0', config.gateway, '8.8.8.8'))
        except OSError as error:
#            pass
            try:
                with open('errors.txt', 'a') as outfile:
                    outfile.write(str(error) + '\n')
            except OSError:
                pass

        sta_if.config(pm=sta_if.PM_NONE)

        while (count < 10):
            count += 1

            if (sta_if.isconnected()):
                count = 0

                print (f'network config: {sta_if.ifconfig()}')

                break

            print (f'. ')
            utime.sleep(1)


    if (count == 10):
        try:
            with open('errors.txt', 'a') as outfile:
                outfile.write('failed to connect after 5 tries' + '\n')
        except Exception as e:
            pass

        disconnect() # or you could get errors
        print (f'poweron reset')
        utime.sleep(0.1)

        config.poweron_reset.on() #  start from scratch


    rssi = sta_if.status('rssi')
    print (f'RSSI =  {rssi} dBm')
    utime.sleep(0.1)

    if ((rssi < -95) or (rssi == 0)):
        print (f'signal level is below -95dBm')
        utime.sleep(0.1)

        disconnect() # or you could get errors
        print (f'poweron reset')
        utime.sleep(0.1)

        config.poweron_reset.on() #  start from scratch


def disconnect():

    sta_if.disconnect()
    sta_if.active(False)
