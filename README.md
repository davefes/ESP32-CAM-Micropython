README.md 
ESP-CAM-Micropython

This project uses the latest firmware version of esp32-cam-micropython-2022 at:
https://github.com/shariltumin/esp32-cam-micropython-2022/tree/main/firmware-20221203
with uMail found at:
https://github.com/shawwwn/uMail
and a modification found here:
https://github.com/shawwwn/uMail/issues/2 by pm4r
to send an alarm to a local ESP32 server and then to send the image to Gmail.

Capturing an image takes significant time (1/2 to 1 second) if you initialise the camera and change some of it’s settings, after starting a trigger.
It was found that doing camera.init() and changing any camera settings that you could go to lightsleep(), waiting for a trigger, and when woken-up the picture would be taken within 10-100ms.  
On the ESP32-CAM board the standby current was about 150mA, with the camera initialised.  Initialising the camera, going to lightsleep() and removing the 3V3 regulator got that current down to around 25mA.
Two 18650 Li-ion cells and a 5W 6V PV panel is probably adequate for remote use.
I found that trying to increase framesize and/or improve the quality could result in poor images, some of the time.

You need to do a umachine.reset() at the start or the camera will not be properly initialised.

Have also included a schematic for a IR receiver and the poweron_reset circuits.  Forget about using poweron_reset, use umachine.reset() instead.

Do not need to import wdt_callback().  Also, as soon as you import wdt_feed the watchdog starts running.
 
