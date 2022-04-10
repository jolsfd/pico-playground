from rgb import RGBLED
from machine import Pin, Timer
import time, random

# Debug light
led = Pin(25, Pin.OUT)

led.on()
print("Raspberry Pi Pico is booting...")
time.sleep(1.5)
led.off()

# init timer
timer = Timer()

# init RGBs
rgb_0 = RGBLED(15,14,13)
rgb_1 = RGBLED(18,17,16)

# check leds
print("Checking RGBs...")
rgb_0.color(255,255,255)
rgb_1.color(255,255,255)

time.sleep(2)

rgb_0.reset()
rgb_1.reset()

def random_color(timer):
    rgb_0.color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
if __name__ == "__main__":
    print("Mainloop...")
    
    timer.init(freq=0.5, mode=Timer.PERIODIC, callback=random_color)
    
    while True:
        rgb_1.breathe(random.randint(0,1),random.randint(0,1),random.randint(0,1))