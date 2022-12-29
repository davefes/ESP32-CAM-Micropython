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
