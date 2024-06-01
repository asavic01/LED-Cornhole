from machine import Pin, ADC
import time
import os
from neopixel import Neopixel

# Setting up pins
# Ultrasound
trigger = Pin(0, Pin.OUT)
echo = Pin(1, Pin.IN)

# Photoresistor
photo_pin = ADC(28)

# Vibration
vibration1 = ADC(26)
vibration2 = ADC(27)

# IR
reciever = Pin(2, Pin.IN)
emitter = Pin(3, Pin.OUT)

#LED
numpix = 300
strip = Neopixel(numpix, 0, 3, "GRB")
strip.brightness(200)

off = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
colors = [red, orange, yellow, green, blue, indigo, violet]


# ultrasound
# Determines how far away an object is using an ultrasound sensor
# Arguments: None
# Returns: None
#def ultrasound():
#    # Send out signal to trigger
#    trigger.low()
#    time.sleep(0.01)
#    trigger.high()
#    time.sleep(0.05)
#    trigger.low()
#    
#    # Determine how far away the object is
#    while echo.value() == 0:
#        signaloff = time.ticks_us()
#    while echo.value() == 1:
#        signalon = time.ticks_us()
#    timepassed = signalon - signaloff
#    distance = (timepassed * 0.0343) / 2
#    print("The distance from object is ",distance,"cm")

# photoresitor
# Determines how dark it is using the analog voltage value due to a photoresistor
# Arguments: None
# Returns: a boolean representing if sensor is triggered or not
def photoresitor():
    value = photo_pin.read_u16()
    
    if(value > 64000):
        return True
    else:
        return False;

# vibration
# Determines if there is vibration occuring 
# Arguments: None
# Returns: a boolean representing if sensor is triggered or not
def vibration():
    vibration1_val = (vibration1.read_u16())
    vibration2_val = (vibration2.read_u16())
    
    if (vibration1_val > 1000):
        return True
    elif (vibration2_val > 1000):
        return True
    else:
        return False
        

# IR
# Determines the IR receiver is picking up signals from the IR emitter
# Arguments: None
# Returns: a boolean representing if sensor is triggered or not
def IR():
    signal = reciever.value()
    if signal:
        return False
    else:
        return True
    
def LED_check(dark, vibrated, IR_blocked):
    
    if dark and vibrated: 
        LED_dark_vibrated()
    elif dark and IR_blocked:
        LED_dark_IR()
    elif dark:
        LED_dark()
    elif vibrated:
        LED_vibrated()
    elif IR_blocked:
        LED_IR()
    else:
        strip.fill(off)
        
    strip.show()
    
def LED_dark_vibrated():
    strip.brightness(200)
    t_end = time.time() + 3
    counter = 1
    while time.time() < t_end:
        strip.set_pixel_line_gradient(0, 99, blue, violet)
        strip.set_pixel_line_gradient(100, 199, blue, violet)
        strip.set_pixel_line_gradient(200, 299, blue, violet)
        strip.rotate_left(counter)
        counter += 8
        strip.show()

def LED_dark_IR():
    strip.brightness(200)
    t_end = time.time() + 3
    counter = 1
    while time.time() < t_end:
        strip.set_pixel_line_gradient(0, 99, red, blue)
        strip.set_pixel_line_gradient(100, 199, red, blue)
        strip.set_pixel_line_gradient(200, 299, red, blue)
        strip.rotate_left(counter)
        counter += 8
        strip.show()

def LED_dark():
    strip.brightness(200)
    strip.fill(yellow)

def LED_vibrated():
    strip.brightness(200)
    t_end = time.time() + 5
    counter = 1
    brightness = 200
    while time.time() < t_end:
        strip.set_pixel_line_gradient(0, 99, blue, violet)
        strip.set_pixel_line_gradient(100, 199, blue, violet)
        strip.set_pixel_line_gradient(200, 299, blue, violet)
        
        strip.rotate_right(counter)
        counter += 5
        
        if (t_end - time.time() < 3):
            brightness -= 10
            strip.brightness(brightness)  
        
        strip.show()

def LED_IR():
    strip.brightness(200)
    t_end = time.time() + 3
    counter = 1
    while time.time() < t_end:
        strip.set_pixel_line_gradient(0, 99, orange, violet)
        strip.set_pixel_line_gradient(100, 199, orange, violet)
        strip.set_pixel_line_gradient(200, 299, orange, violet)
        strip.rotate_right(counter)
        counter += 8
        strip.show()
    
    
# Main loop
# Runs contantly runs the sensor functions to pick up information on sensors
while True:
    dark = photoresitor()
    vibrated = vibration()
    IR_blocked = IR()
    LED_check(dark, vibrated, IR_blocked)
    time.sleep(0.005)
    