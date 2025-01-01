#!/usr/bin/env python3

import time
import json
from picamera2 import Picamera2

picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.start()
time.sleep(1)
picam2.switch_mode_and_capture_file(capture_config, "test.jpg")