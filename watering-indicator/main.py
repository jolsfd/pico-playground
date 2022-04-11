import time
from machine import Pin, ADC

# Scala
SENSOR_MAX = 5600
SENSOR_MIN = 0

# Time interval in s
DELAY = 10 # 1 hour = 3600

#=====ONLY=CHNAGE=THIS========
# Humidity values in percent 
OPTIMAL_MIN = 50
OPTIMAL_MAX = 80
#=============================

# Water sensor
sensor_power = Pin(28,Pin.OUT)
sensor = ADC(Pin(27))

# Temperature sensor
sensor_temp = ADC(4)
CONVERSION_FACTOR = 3.3 / (65535)

# Leds
led_pico = Pin(25,Pin.OUT)
led_red = Pin(0,Pin.OUT)
led_green = Pin(1,Pin.OUT)
led_yellow = Pin(2,Pin.OUT)

# Functions
def smooth_reading():
    avg = 0
    _AVG_NUM = 100
    for _ in range(_AVG_NUM):
        avg += sensor.read_u16()
    avg /= _AVG_NUM
    return(avg)

def leds_off():
    led_green.value(0)
    led_red.value(0)
    led_yellow.value(0)
    
def leds_on():
    led_green.value(1)
    led_red.value(1)
    led_yellow.value(1)

# Loop
while True:
    # Turn led on
    led_pico.value(1)
    
    # Sensor on
    sensor_power.value(1)
    
    # Water measurement
    analog_val = smooth_reading()
    HUMIDITY = round(((analog_val - SENSOR_MIN) / (SENSOR_MAX - SENSOR_MIN)) * 100)
    
    # Sensor off
    sensor_power.value(0)
    
    # Temperature  measurement
    reading = sensor_temp.read_u16() * CONVERSION_FACTOR
    temperature = 27 - (reading - 0.706)/0.001721
    
    # Turn led off
    time.sleep(1)
    led_pico.value(0)
    
    # Print values
    print('Analog Value: ' + str(analog_val))
    print('Humidity: ' + str(HUMIDITY) + '%')
    print('Temperature: ' + str(temperature) + '°C\n')
    
    # Turn leds on/off
    if OPTIMAL_MIN <= HUMIDITY <= OPTIMAL_MAX:
        leds_off()
        led_green.value(1)
        
    elif HUMIDITY > OPTIMAL_MAX:
        leds_off()
        led_red.value(1)
        
    else:
        leds_off()
        led_yellow.value(1)
    
    # Sleep
    time.sleep(DELAY)
