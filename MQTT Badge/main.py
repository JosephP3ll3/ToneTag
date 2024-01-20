# import launcher  # noqa F401
from machine import Pin
import time
led = Pin("LED", Pin.OUT)


led.toggle()
#     time.sleep(1)

import Tone_Tag