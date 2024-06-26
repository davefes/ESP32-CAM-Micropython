README.md 
ESP-CAM-Micropython

This project uses version esp32-cam-micropython-2022 at:
https://github.com/shariltumin/esp32-cam-micropython-2022/tree/main/firmware-20221203
with uMail found at:
https://github.com/shawwwn/uMail
and a modification found here:
https://github.com/shawwwn/uMail/issues/2 by pm4r
to send an alarm to a local ESP32 server and then to send the image to Gmail.

It was found that if you do lightsleep you have to do camera.init(), change any camera settings and wait for those changes to take place first. Then go to lightsleep(), wait for a trigger, and when woken-up the picture would be taken within 10-100ms.  

On the ESP32-CAM board the standby current was about 150mA, with the camera initialised.  Initialising the camera, going to lightsleep() and removing the 3V3 regulator got that current down to around 25mA. Two 18650 Li-ion cells and a 5W 6V PV panel is probably adequate for remote use.

You need to do a system reset at the start, if doing a CTRL-C or the camera will not be properly initialised.

Found a camera.init() that waits for completion.
https://github.com/shariltumin/esp32-cam-micropython-2022/blob/main/webcam.py

I am not convinced that a machine.reset() is adequate to properly init the camera when lightsleep() is involved.
