README.md 
ESP-CAM-Micropython

This project uses version esp32-cam-micropython-2022/ at: https://github.com/shariltumin/esp32-cam-micropython-2022/tree/main/X23/esp32-aiThinker/firmwares/wifi%2Bssl with uMail found at: https://github.com/shawwwn/uMail and a modification found here: shawwwn/uMail#2 by pm4r to send an alarm to a local ESP32 server and then to send the image to Gmail.

Taking a good snapshot proved to be quite difficult until I found this thread: https://github.com/espressif/esp32-camera/issues/314 and down near the bottom it was suggested to take 5-10 frames ignoring the first 4 or 9.
 
You need to do a system reset at the start, if doing a CTRL-C or the camera will not be properly initialised.

Found a camera.init() that waits for completion. https://github.com/shariltumin/esp32-cam-micropython-2022/blob/main/webcam.py

I also found that some cameras need a full poweron_reset to stop `camera probe fails`  See ESP32_CAM_poweron.pdf

Be aware that GPIO2, GPIO4 and GOI13, on boards that have a SD card feature, may be 47K pullups on them.  
