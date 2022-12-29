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

##  Simple software WDT implementation
#  thanks to mkiotdev
#  https://forum.micropython.org/viewtopic.php?f=16&t=5517&hilit=simple+software+WDT&start=10


import machine
import utime
import config


wdt_counter = 0

def wdt_callback():
    global wdt_counter
    wdt_counter += 1
    if (wdt_counter >= 80): #  80 seconds
        epoch = utime.time()
        local_time = utime.localtime(epoch)
        seconds = local_time[5]
        minutes = local_time[4]
        hours = local_time[3]
        day = local_time[2]

        time = str(hours) + ':' + str(minutes) + ':' + str(seconds)

        try:
            with open('errors.txt', 'a') as outfile:
                outfile.write(str(day) + ' ' + time + '\n')
                outfile.write('had a wdt event' + '\n')
        except OSError:
            pass

        config.poweron_reset.on()

def wdt_feed():
    global wdt_counter
    wdt_counter = 0

wdt_timer = machine.Timer(3) #  hardware timer for ESP32
wdt_timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=lambda t:wdt_callback())
## END Simple software WDT implementation
