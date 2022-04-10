from machine import Pin, PWM
import time

class RGBLED:
    def __init__(self,red_pin, green_pin, blue_pin):
        # set pin and pwm
        self.red = PWM(Pin(red_pin))
        self.green = PWM(Pin(green_pin))
        self.blue = PWM(Pin(blue_pin))
        
        # set frequency
        self.red.freq(1000)
        self.green.freq(1000)
        self.blue.freq(1000)
        
        # reset
        self.red.duty_u16(0)
        self.green.duty_u16(0)
        self.blue.duty_u16(0)
        
    def reset(self):
        self.red.duty_u16(0)
        self.green.duty_u16(0)
        self.blue.duty_u16(0)
        
    def convert_rgb(self, var, in_min, in_max, out_min, out_max): 
        return int((var - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
        
    def color(self, red, green, blue):
        self.reset()
        
        self.red.duty_u16(self.convert_rgb(red, 0, 255, 0, 65535)) 
        self.green.duty_u16(self.convert_rgb(green, 0, 255, 0, 65535)) 
        self.blue.duty_u16(self.convert_rgb(blue, 0, 255, 0, 65535))
        
    def breathe(self,red,green,blue):
        self.reset()
        
        self.color(red,green,blue)
        
        # brigther
        for i in range(0,65536,8):
            if red > 0:
                self.red.duty_u16(i)
            if green > 0:
                self.green.duty_u16(i)
            if blue > 0:
                self.blue.duty_u16(i)
            time.sleep(0.001) 
        
        # darker
        for i in range(65535, -1, -8):
            if red > 0:
                self.red.duty_u16(i)
            if green > 0:
                self.green.duty_u16(i)
            if blue > 0:
                self.blue.duty_u16(i)
            time.sleep(0.001)
        
if __name__ == "__main__":
    rgb = RGBLED(15,14,13)
    
    rgb.color(255,0,0)
    time.sleep(1)
    rgb.color(0,255,0)
    time.sleep(1)
    rgb.color(0,0,255)
    time.sleep(1)
    
    rgb.breathe(1,1,1)