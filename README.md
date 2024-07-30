README.md 
ESP-CAM-Micropython

This project uses version esp32-cam-micropython-2022 at:
https://github.com/shariltumin/esp32-cam-micropython-2022/tree/main/firmware-20221203
with uMail found at:
https://github.com/shawwwn/uMail
and a modification found here:
https://github.com/shawwwn/uMail/issues/2 by pm4r
to send an alarm to a local ESP32 server and then to send the image to Gmail.

This project uses version esp32-cam-micropython-2022/ at: https://github.com/shariltumin/esp32-cam-micropython-2022/tree/main/X23/esp32-aiThinker/firmwares/wifi%2Bssl with uMail found at: https://github.com/shawwwn/uMail and a modification found here: shawwwn/uMail#2 by pm4r to send an alarm to a local ESP32 server and then to send the image to Gmail.

Taking a good snapshot proved to be quite difficult until I found this thread: https://github.com/espressif/esp32-camera/issues/314 and down near the bottom it was suggested to take 5-10 frames ignoring the first 4 or 9.
 
You need to do a system reset at the start, if doing a CTRL-C or the camera will not be properly initialised.

Found a camera.init() that waits for completion. https://github.com/shariltumin/esp32-cam-micropython-2022/blob/main/webcam.py

This script uses lightsleep as I thought it would wake up and take the image in less time then a full re-boot fron deepsleep. Lightsleep to image capture is about 1.5 seconds.  Deepsleep takes about 2 seconds.  Lightsleep current is about 15mA and deepsleep current is about 7mA.

Freezing the application might help to reduce this delay.
