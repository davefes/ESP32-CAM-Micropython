#  29 Dec 2022 D. Festing


import network
import utime
import config
import machine


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
            sta_if.ifconfig((config.WiFi_device, '255.255.255.0', config.gateway, '8.8.8.8'))
            sta_if.connect(config.hotspot, config.password)
        except OSError as error:
            try:
                with open('errors.txt', 'a') as outfile:
                    outfile.write(str(error) + '\n')
            except OSError:
                pass

        while (count < 5):
            count += 1

            if (sta_if.isconnected()):
                count = 0

                print (f'network config: {sta_if.ifconfig()}')

                break

            print (f'. ')
            utime.sleep(1)


    if (count == 5):
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
